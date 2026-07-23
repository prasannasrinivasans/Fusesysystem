from config.playwright_config import Config
from pages.base_page import BasePage
from faker import Faker
import uuid


class MemberListPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.firstname = "//input[@id='first_name']"
        self.lastname = "//input[@id='last_name']"
        self.address2 = "//input[@id='street']"
        self.address3 = "//input[@id='apartment']"
        self.city = "(//input[@id='city'])[1]"
        self.state = "//input[@id='state']"
        self.zipcode = "//input[@id='zipcode']"
        self.ssn = "//input[@id='social_security_number']"
        self.account = "//input[@id='shield_number']"
        self.gender = "//label[normalize-space()='Gender']/following::div[contains(@class,'ant-select-selector')][1] | (//div[@class='ant-select-selector'])[1]"
        self.chcp = "//label[normalize-space()='CHCP']/following::div[contains(@class,'ant-select-selector')][1] | (//div[@class='ant-select-selector'])[7]"
        self.create = "//button[@type='submit']"


    def open(self):
        self.navigate(f"{Config.BASE_URL}/member-search")
        self.page.wait_for_load_state("networkidle")

    def scroll_to_bottom(self):
        try:
            self.page.locator("//label[normalize-space()='Member End Date:']").scroll_into_view_if_needed(timeout=5000)
        except Exception:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    def add_member(self):
        self.click("//span[normalize-space()='Add Member']")

    add_memeber = add_member

    # def fill_member_details(self, first_name, last_name, address2, address3, city, state, zipcode, ssn, account):
    #     self.page.fill(self.firstname, first_name)
    #     self.page.fill(self.lastname, last_name)
    #     self.page.fill(self.address2, address2)
    #     self.page.fill(self.address3, address3)
    #     self.page.fill(self.city, city)
    #     self.page.fill(self.state, state)
    #     self.page.fill(self.zipcode, zipcode)
    #     self.page.fill(self.ssn, ssn)
    #     self.page.fill(self.account, account)
    # def select_random_gender(self):
    #     self.page.locator(self.gender).click()
    #     self.page.wait_for_timeout(1000)

    #     dropdown = self.page.locator("xpath=//div[contains(@class,'ant-select-dropdown') and not(contains(@style,'display: none'))]")
    #     options = dropdown.locator("xpath=.//div[@role='option']")
    #     count = options.count()

    #     if count == 0:
    #         raise AssertionError("No gender options were available after opening the dropdown.")

    #     fake = Faker()
    #     random_index = fake.random_int(min=0, max=count - 1)
    #     option = options.nth(random_index)

    #     selected_gender = option.get_attribute('aria-label') or option.inner_text()
    #     values = [options.nth(i).get_attribute('aria-label') or options.nth(i).inner_text() for i in range(count)]
    #     print(f"Gender dropdown options: {values}")
    #     print(f"Selected gender from dropdown: {selected_gender}")

    #     option.evaluate("el => el.click()")
    #     self.page.wait_for_timeout(500)

    #     return selected_gender

    def _get_active_dropdown(self):
        return self.page.locator(
            "xpath=//div[contains(@class,'ant-select-dropdown') and not(contains(@class,'ant-select-dropdown-hidden')) and not(contains(@style,'display: none'))]"
        )

    def _try_click_option(self, element):
        """Try click, then evaluate as fallback."""
        try:
            element.click()
        except:
            try:
                element.evaluate("el => el.click()")
            except:
                pass

    def _select_by_keyboard(self, index):
        """Select via keyboard."""
        for _ in range(index + 1):
            self.page.keyboard.press("ArrowDown")
            self.page.wait_for_timeout(80)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(500)

    def select_random_chcp(self):
        """Select a random CHCP option."""
        self.page.locator(self.chcp).click()
        self.page.wait_for_timeout(500)

        # Try multiple dropdown locators to be resilient to DOM variations
        candidates = [
            "xpath=//div[contains(@class,'ant-select-dropdown') and not(contains(@class,'ant-select-dropdown-hidden')) and not(contains(@style,'display: none'))]//div[@role='option']",
            "xpath=//div[contains(@class,'ant-select-dropdown') and not(contains(@style,'display: none'))]//div[contains(@class,'ant-select-item') and not(contains(@class,'ant-select-item-disabled'))]",
            "xpath=//ul[contains(@class,'ant-select-dropdown-menu')]//li",
            "xpath=//div[contains(@class,'ant-select-dropdown')]//div[contains(@class,'ant-select-item')]",
        ]

        options = None
        count = 0
        for cand in candidates:
            try:
                locator = self.page.locator(cand)
                count = locator.count()
                if count and count > 0:
                    options = locator
                    break
            except Exception:
                continue

        if not options or count == 0:
            # Save debug artifacts for investigation
            debug_id = str(uuid.uuid4())[:8]
            screenshot = Config.SCREENSHOT_PATH / f"no_chcp_{debug_id}.png"
            try:
                Config.SCREENSHOT_PATH.mkdir(parents=True, exist_ok=True)
                self.page.screenshot(path=str(screenshot), full_page=True)
            except Exception:
                pass

            # capture a short page HTML snippet near the CHCP locator
            try:
                field_html = self.page.locator(self.chcp).evaluate("el => el.outerHTML")
            except Exception:
                field_html = "<unable to capture field HTML>"

            raise AssertionError(
                f"No CHCP options available. Captured screenshot={screenshot} field_html={field_html}"
            )

        random_index = Faker().random_int(0, count - 1)
        option = options.nth(random_index)
        intended_selection = option.inner_text().strip()

        # Try clicking
        try:
            option.scroll_into_view_if_needed()
        except Exception:
            pass
        self._try_click_option(option)
        self.page.wait_for_timeout(200)

        # Read actual selected value from field
        try:
            actual_value = self.page.locator(self.chcp).inner_text().strip()
        except Exception:
            actual_value = ""

        # If click failed, use keyboard
        if not actual_value or actual_value.lower() in ("select", ""):
            self.page.locator(self.chcp).click()
            self.page.wait_for_timeout(300)
            self._select_by_keyboard(random_index)
            try:
                actual_value = self.page.locator(self.chcp).inner_text().strip()
            except Exception:
                actual_value = ""

        print(f"✅ CHCP selected: {actual_value} (intended: {intended_selection})")
        return actual_value
    def  click_create_button(self):
        self.click(self.create)
        self.page.wait_for_load_state("networkidle")
        