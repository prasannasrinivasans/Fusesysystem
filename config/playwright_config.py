import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:

    BASE_URL = os.getenv("BASE_URL")

    CI = os.getenv("CI", "false").lower() == "true"

    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true" or CI
    SLOW_MO = int(os.getenv("SLOW_MO", 0))

    TIMEOUT = 30000

    SCREENSHOT_PATH = Path("reports/screenshots")
    TRACE_PATH = Path("reports/traces")

    TRACE_ENABLED = os.getenv("TRACE_ENABLED", "true").lower() == "true"
    CHANNEL = os.getenv("CHANNEL", None)

    STORAGE_STATE = "auth/storage_state.json"

    @classmethod
    def ensure_dirs(cls):
        cls.SCREENSHOT_PATH.mkdir(parents=True, exist_ok=True)
        cls.TRACE_PATH.mkdir(parents=True, exist_ok=True)
        Path("auth").mkdir(exist_ok=True)

    @classmethod
    def validate(cls):
        if not cls.BASE_URL:
            raise ValueError("BASE_URL is required. Set it in your .env or environment variables.")

    @classmethod
    def browser_options(cls):
        return {
            "headless": cls.HEADLESS,
            "slow_mo": cls.SLOW_MO
        }

    @classmethod
    def context_options(cls):
        return {}

    @classmethod
    def unique_name(cls, test_name):
        """Generate unique filename for screenshots/traces"""
        timestamp = str(uuid.uuid4())[:8]
        return f"{test_name}_{timestamp}"

    @classmethod
    def unique_name(cls, name):
        return f"{name}_{uuid.uuid4().hex}"