# FLPBA - Playwright Test Automation Framework

## Project Overview

FLPBA is a comprehensive test automation framework built with **Playwright** and **Pytest** for testing web applications. It follows the Page Object Model (POM) design pattern and includes robust logging, reporting, and test data management.

---

## Project Structure

```
FLPBA/
├── config/                          # Configuration files
│   ├── __init__.py
│   └── playwright_config.py         # Playwright configuration & settings
│
├── pages/                           # Page Object Models
│   ├── __init__.py
│   ├── base_page.py                 # Base class for all page objects
│   └── memberlist.py                # Member list page object
│
├── tests/                           # Test files
│   ├── __init__.py
│   ├── data/                        # Test data
│   │   ├── __init__.py
│   │   ├── member/                  # Member-specific test data
│   │   │   └── faker_member_data.xlsx
│   │   └── fixtures/                # Test fixtures (reserved for future use)
│   └── member_list/                 # Member list tests
│       ├── __init__.py
│       └── test_memberlist.py       # Member list test cases
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── excel_reader.py              # Excel file handling utilities
│   └── login_setup.py               # Authentication & session management
│
├── reports/                         # Test output & reports
│   ├── report.html                  # HTML test report
│   ├── allure-results/              # Allure report data
│   ├── screenshots/                 # Failed test screenshots
│   └── traces/                      # Playwright traces
│
├── auth/                            # Authentication storage
│   └── storage_state.json           # Browser storage state (credentials)
│
├── conftest.py                      # Pytest configuration & fixtures
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

---

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Git
- Virtual environment manager (venv or conda)

### 2. Install Dependencies

```bash
# Clone/navigate to project directory
cd FLPBA

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Required Environment Variables:**
```
BASE_URL=https://your-app-url.example.com
USERNAME=your-email@example.com
PASSWORD=your-password
BROWSER=chromium
HEADLESS=false
SLOW_MO=0
TRACE_ENABLED=true
CHANNEL=
```

---

## Key Features

### 🔐 Authentication Management
- Automatic session storage (`auth/storage_state.json`)
- Login session reuse to speed up tests
- Credential management via environment variables

### 📊 Comprehensive Reporting
- **HTML Reports**: `reports/report.html`
- **Allure Reports**: `reports/allure-results/`
- **Screenshots**: Captured on test failures
- **Traces**: Playwright traces for debugging

### 📝 Enhanced Logging
- Structured logging with timestamps
- Color-coded log levels (INFO, WARNING, ERROR)
- Detailed action tracking in base page object

### 📈 Test Data Management
- Excel-based test data (`tests/data/member/`)
- Faker library for generating realistic data
- Easy data import/export

### 🏗️ Page Object Model (POM)
- `BasePage`: Base class with common actions
- `MemberListPage`: Specific page implementations
- Reusable locators and methods

---

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/member_list/test_memberlist.py -v
```

### Run with Custom Options
```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Run with specific marker
pytest -m "your_marker" -v

# Generate HTML report
pytest --html=reports/report.html

# Generate Allure report
pytest --alluredir=reports/allure-results
```

### View Allure Report
```bash
allure serve reports/allure-results
```

---

## Configuration

### `config/playwright_config.py`
Centralized configuration for:
- Browser settings (Chromium, Firefox, WebKit)
- Headless mode and slow motion
- Timeouts and trace settings
- Report paths and screenshot directories

### `pytest.ini`
Pytest configuration:
- Test paths
- HTML report generation
- Logging settings

### `conftest.py`
Pytest fixtures:
- `setup()`: Session fixture for authentication
- `page()`: Function fixture for browser pages
- `pytest_runtest_makereport()`: Hook for test report generation

---

## Test Data

### Generate Test Data
```python
from utils.excel_reader import generate_fake_member_data, save_excel_data

# Generate 10 fake member records
data = generate_fake_member_data(count=10)
save_excel_data("tests/data/member/members.xlsx", data)
```

### Excel Data Structure
```
| first_name | last_name | address2 | address3 | city | state | zipcode | ssn | account | gender | chcp |
```

---

## Best Practices

### ✅ Writing Tests
1. Use Page Object Model for all page interactions
2. Add descriptive assertions with meaningful messages
3. Use proper logging for debugging
4. Follow naming convention: `test_<feature>_<action>`

### ✅ Creating Page Objects
1. Extend `BasePage` class
2. Define locators as class constants
3. Create methods for user interactions
4. Add logging to track actions

### ✅ Debugging
- Check `reports/screenshots/` for failure screenshots
- Review `reports/report.html` for detailed test results
- Use `SLOW_MO` environment variable for slow animation
- Enable traces with `TRACE_ENABLED=true`

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `playwright` | Web automation library |
| `pytest` | Test framework |
| `python-dotenv` | Environment variable management |
| `openpyxl` | Excel file handling |
| `Faker` | Fake data generation |
| `pytest-html` | HTML report generation |
| `allure-pytest` | Allure report integration |
| `pytest-xdist` | Parallel test execution |

---

## Troubleshooting

### Issue: "BASE_URL is required"
**Solution**: Check `.env` file is properly configured with `BASE_URL`

### Issue: "Storage state not found"
**Solution**: First run will trigger login. Ensure `USERNAME` and `PASSWORD` are set in `.env`

### Issue: Slow test execution
**Solution**: Set `HEADLESS=true` and `SLOW_MO=0` in `.env`

### Issue: Flaky tests
**Solution**: 
- Increase timeout values
- Use explicit waits instead of implicit
- Check network conditions with `wait_for_load_state("networkidle")`

---

## Contributing

1. Create feature branch: `git checkout -b feature/test-feature`
2. Add tests following project conventions
3. Run tests locally: `pytest -v`
4. Commit with clear messages
5. Create pull request

---

## License

[Your License Here]

---

## Contact & Support

For questions or issues, please contact the QA team or create an issue in the repository.

---

**Last Updated**: July 2026
