# Python framework for Playwright
This is a python PageObject framework for Playwright. 

Read more about Playwright — https://playwright.dev/

## Requirements
Python 3.12

## Installation
1. Create new virtual environment and use package manager pip to install all requirements: ```pip install -r requirements.txt```;
2. Install Playwright dependencies: ```playwright install```
3. Follow this guide to install Allure — https://docs.qameta.io/allure/#_get_started

## Browsers
To add and use more browsers, check Playwright documentation – https://playwright.dev/docs/browsers

## Mobile Emulation
Usage: add decorator `@pytest.mark.mobile` to your test on class to use mobile emulation. 

To add more mobile devices:
1. Add new mark to `pytest.ini`;
2. Add new devices in `core/driver.py`;
3. Change `is_mobile` function in `conftest.py` — it requires new logic;

## Run your tests
Multiple threads:
- Single-thread — execute command `pytest tests/` to run all tests in 1 thread;
- Multi-thread — execute command `pytest tests/ -n 5` to run all tests in 5 threads.

Generate Allure report:
- Execute command `pytest tests/ --alluredir=./allure_results` to run all tests and generate Allure report files in directory `./allure_reports`. To run human-readable Allure report, execute command from the same directory `allure serve ./allure_results`.    
