# FLPBA - Quick Setup Guide

## 🚀 Quick Start (5 minutes)

### Step 1: Clone & Setup Environment
```bash
cd FLPBA
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Edit .env file with your credentials
nano .env

# Required fields:
# - BASE_URL: Your application URL
# - USERNAME: Login email
# - PASSWORD: Login password
```

### Step 3: Run First Test
```bash
pytest tests/member_list/test_memberlist.py -v
```

---

## 📁 Folder Structure Reference

| Folder | Purpose |
|--------|---------|
| `config/` | Configuration and settings |
| `pages/` | Page Object Models |
| `tests/` | Test files and test data |
| `utils/` | Helper functions and utilities |
| `reports/` | Test results and reports |
| `auth/` | Session storage |

---

## 🔧 Common Commands

```bash
# Run all tests
pytest

# Run specific test
pytest tests/member_list/test_memberlist.py

# Run with verbose output
pytest -v

# Run with print statements
pytest -s

# Generate HTML report
pytest --html=reports/report.html

# View Allure report (if installed)
allure serve reports/allure-results
```

---

## 📊 Output Files

After running tests, check:
- `reports/report.html` - Test results
- `reports/screenshots/` - Failed test screenshots
- `reports/traces/` - Playwright traces
- `reports/pytest.log` - Detailed logs

---

## ✅ Environment Variables Explained

| Variable | Default | Purpose |
|----------|---------|---------|
| `BASE_URL` | ❌ Required | Application URL |
| `USERNAME` | ❌ Required | Login email |
| `PASSWORD` | ❌ Required | Login password |
| `BROWSER` | chromium | Browser type |
| `HEADLESS` | false | Run headless mode |
| `SLOW_MO` | 0 | Slow motion delay (ms) |
| `TRACE_ENABLED` | true | Enable Playwright traces |
| `CHANNEL` | (empty) | Browser channel |

---

## 🐛 Troubleshooting

### Tests Won't Run
1. Check Python version: `python --version` (need 3.10+)
2. Verify virtual environment: `which python` should show `.venv`
3. Reinstall dependencies: `pip install -r requirements.txt`

### Login Fails
1. Verify credentials in `.env`
2. Check internet connection
3. Delete `auth/storage_state.json` to force re-login

### Tests are Slow
Set in `.env`:
```
HEADLESS=true
SLOW_MO=0
```

---

## 📚 Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Review [pages/base_page.py](pages/base_page.py) for available actions
3. Check [tests/member_list/test_memberlist.py](tests/member_list/test_memberlist.py) for examples
4. Create new page objects by extending `BasePage`

---

**Need help?** Check the main README.md or contact the QA team.
