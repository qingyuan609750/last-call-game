import pytest
from playwright.sync_api import sync_playwright
from allure import attach


@pytest.fixture(scope="function")
def driver():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(driver):
    return driver
