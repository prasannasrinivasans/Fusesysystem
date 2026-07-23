from dotenv import load_dotenv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from playwright.sync_api import sync_playwright
from config.playwright_config import Config

load_dotenv()


def save_login_session():
    Config.ensure_dirs()
    Config.validate()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not username or not password:
        raise Exception("Missing USERNAME or PASSWORD in your environment or .env file")

    storage_path = Path(Config.STORAGE_STATE)
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS)
        context = browser.new_context()
        page = context.new_page()

        page.goto(f"{Config.BASE_URL}", wait_until="networkidle", timeout=30000)
        page.wait_for_selector("//input[@id='email']", timeout=20000)

        page.fill("//input[@id='email']", username)
        page.fill("//input[@id='password']", password)
        page.click("button:has-text('Sign In')")

        page.wait_for_url("**/member-search", timeout=30000)
        page.wait_for_selector("//span[contains(text(),'Member Search') or contains(text(),'member search') ]", timeout=30000)

        print("✅ Logged in URL:", page.url)

        context.storage_state(path=str(storage_path))
        browser.close()


if __name__ == "__main__":
    save_login_session()