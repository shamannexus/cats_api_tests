# 🐱 The Cat API Test Suite

This project is a sample test suite using **Pytest** and **Requests** to validate core endpoints of [The Cat API](https://thecatapi.com/). It includes smoke, regression, and end-to-end test coverage using best practices like fixtures, environment variables, tagging, and HTML reporting.

---

## 🧰 Tech Stack

- Python 3.x
- Requests
- Pytest
- Pytest-HTML
- python-dotenv

---

## 📦 Installation

1. **Clone the repo**
```bash
git clone https://github.com/shamannexus/cats_api_tests.git
cd cats_api_tests
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set your Cat API key**
Create a `.env` file in the project root:
Open https://thecatapi.com/
Press "Get Your API KEY" button
Press "Get Free Access" button
Provide your email and ather information needed
Check your email to get API key
Paste your kay in .env file like this:
```
CAT_API_KEY=your_api_key_here
```
---

## 🚀 Running Tests

### ▶ Run All Tests
```bash
pytest
```

### 🟢 Run Smoke Tests Only
```bash
pytest -m smoke
```

### 🧪 Run Regression Tests Only
```bash
pytest -m regression
```

### 🔁 Run End-to-End Tests Only
```bash
pytest -m e2e
```

### 📝 Run Specific File or Directory
```bash
pytest tests/smoke/test_smoke_image.py
```

### 🧪 Run Example with tag and file name

```bash
pytest -m regression -k "test_get_bengal_images_with_detailed_validation"
```
---

## 📄 Generate HTML Report

By default, each test run generates an HTML report:

```bash
pytest
```

Output:
```
report.html
```


---

## 📁 Project Structure

```
cat_api_tests/
├── conftest.py         # Fixtures for auth and config
├── config.py           # API auth data
├── constants.py        # API base URLs and endpoints
├── utils.py            # Reusable helper functions
├── requirements.txt    # Python dependencies
├── pytest.ini          # Config + markers
├── .env                # API key (excluded from Git)
├── .gitignore          # data will be ignored during push to Git
├── README.md
└── tests/
    ├── smoke/
    │   └── test_smoke_image.py
    ├── regression/
    │   └── test_regression_breed_list.py
    ├── e2e/
    │   └── test_e2e_random_image_with_breed.py
```

---

## ✅ Test Case Coverage

| Type       | Description                                               |
|------------|-----------------------------------------------------------|
| Smoke      | Basic image retrieval test for API availability           |
| Regression | Validates `/breeds` returns consistent and expected data (schema and data validation)  |
| E2E        | Complete flow: retrieve breed list -> fetch image by breed |

---





