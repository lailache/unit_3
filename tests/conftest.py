import pytest
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="session")
def base_url():
    return "https://www.furla.com/gr/en/"


@pytest.fixture(scope="session")
def driver(base_url):
    """Fixture to provide a WebDriver instance."""
    driver = webdriver.Chrome()
    driver.get(base_url)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def accept_cookies(driver):
    accept_cookies_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
    )
    accept_cookies_button.click()


@pytest.fixture(scope="session")
def close_subscription(driver):
    close_subscription_button = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close Subscription"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", close_subscription_button)

    driver.execute_script("arguments[0].click();", close_subscription_button)


@pytest.fixture(scope="function")
def delete_all_cookies(driver):
    driver.delete_all_cookies()
