import os
import pytest
from playwright.sync_api import sync_playwright
from config.playwright_config import Config
from utils.login_setup import save_login_session


@pytest.fixture(scope="session", autouse=True)
def setup():
    Config.ensure_dirs()

    needs_login = False
    if not os.path.exists(Config.STORAGE_STATE):
        needs_login = True
    else:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=Config.HEADLESS)
            context = browser.new_context(storage_state=Config.STORAGE_STATE)
            page = context.new_page()

            try:
                page.goto(f"{Config.BASE_URL}/member-search", wait_until="networkidle", timeout=20000)

                if "/login" in page.url or "/sign-in" in page.url:
                    needs_login = True
                else:
                    login_page_present = page.locator("//input[@id='email']").count() > 0
                    sign_in_button_present = page.locator("button:has-text('Sign In')").count() > 0
                    if login_page_present or sign_in_button_present:
                        needs_login = True

            finally:
                context.close()
                browser.close()

    if needs_login:
        save_login_session()


@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as p:

        
        browser_type = getattr(p, Config.BROWSER)

        
        browser_launch_options = {
            "headless": Config.HEADLESS,
            "slow_mo": Config.SLOW_MO,
            "args": ["--start-maximized"]  
        }

        if Config.CHANNEL:
            browser_launch_options["channel"] = Config.CHANNEL

        browser = browser_type.launch(**browser_launch_options)

        
        context = browser.new_context(
            storage_state=Config.STORAGE_STATE,
            no_viewport=True             
        )

        
        if Config.TRACE_ENABLED:
            context.tracing.start(
                screenshots=True,
                snapshots=True,
                sources=True
            )

        
        page = context.new_page()

        
        page.set_default_timeout(Config.TIMEOUT)

        yield page

        
        if (
            hasattr(request.node, "rep_call")
            and request.node.rep_call.failed
        ):
            screenshot_file = (
                Config.SCREENSHOT_PATH /
                f"{Config.unique_name(request.node.name)}.png"
            )

            page.screenshot(
                path=str(screenshot_file),
                full_page=True
            )

        
        if Config.TRACE_ENABLED:
            trace_file = (
                Config.TRACE_PATH /
                f"{Config.unique_name(request.node.name)}.zip"
            )

            context.tracing.stop(
                path=str(trace_file)
            )

        
        context.close()
        browser.close()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)