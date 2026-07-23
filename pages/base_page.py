import logging
from pathlib import Path


class BasePage:
    """Base Page Object Model class with enhanced logging."""
    
    def __init__(self, page):
        self.page = page
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup logger for page actions."""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    #  WAIT + CHECK
    def is_visible(self, locator, timeout=10000):
        try:
            self.page.wait_for_selector(locator, timeout=timeout)
            self.logger.info(f"✓ Element visible: {locator}")
            return True
        except Exception as e:
            self.logger.warning(f"✗ Element not visible: {locator}")
            return False

    #  CLICK
    def click(self, locator):
        try:
            self.page.wait_for_selector(locator, timeout=10000)
            self.page.click(locator)
            self.logger.info(f"✓ Clicked: {locator}")
        except Exception as e:
            self.logger.error(f"✗ Failed to click: {locator} - {str(e)}")
            raise

    # TYPE
    def fill(self, locator, text):
        try:
            self.page.wait_for_selector(locator, timeout=10000)
            self.page.fill(locator, text)
            self.logger.info(f"✓ Filled: {locator} = {text[:20]}...")
        except Exception as e:
            self.logger.error(f"✗ Failed to fill: {locator} - {str(e)}")
            raise

    # GET TEXT
    def get_text(self, locator):
        try:
            self.page.wait_for_selector(locator, timeout=10000)
            text = self.page.inner_text(locator)
            self.logger.info(f"✓ Got text from {locator}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"✗ Failed to get text: {locator} - {str(e)}")
            raise

    #  NAVIGATE
    def navigate(self, url):
        try:
            self.page.goto(url)
            self.logger.info(f"✓ Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"✗ Failed to navigate to: {url} - {str(e)}")
            raise

    #  WAIT FOR URL
    def wait_for_url(self, url_part):
        try:
            self.page.wait_for_url(f"**{url_part}**")
            self.logger.info(f"✓ URL contains: {url_part}")
        except Exception as e:
            self.logger.error(f"✗ URL not found: {url_part} - {str(e)}")
            raise

    #  SCREENSHOT
    def take_screenshot(self, name="screenshot.png"):
        try:
            screenshot_path = Path("reports/screenshots") / name
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            self.page.screenshot(path=str(screenshot_path))
            self.logger.info(f"✓ Screenshot saved: {screenshot_path}")
        except Exception as e:
            self.logger.error(f"✗ Failed to take screenshot: {str(e)}")
            raise