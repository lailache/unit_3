import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_accept_cookies_and_close_subscription(driver):
    driver.get("https://www.furla.com/gr/en/")

    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        accept_cookies_button.click()
    except TimeoutException:
        print("Кнопка принятия куки не найдена или уже принята.")

    try:
        close_subscription_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close Subscription"]'))
        )
        close_subscription_button.click()
    except TimeoutException:
        print("Кнопка закрытия подписки не найдена или уже закрыта.")


def test_search_elements(driver):
    test_accept_cookies_and_close_subscription(driver)

    element_by_class = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "footer-nav__link"))
    )
    assert element_by_class is not None, "Element not found by class"

    element_by_css = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/gr/en/online_shop.html"]'))
    )
    assert element_by_css is not None, "Element not found by CSS"

    element_by_xpath = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Bags")]'))
    )
    assert element_by_xpath is not None, "Element not found by XPath"


def test_interact_elements(driver):
    test_accept_cookies_and_close_subscription(driver)

    bags_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Bags")]'))
    )
    bags_link.click()

    WebDriverWait(driver, 10).until(EC.title_contains("Bags"))
    assert "Bags" in driver.title, "Page title does not contain 'Bags'"

    search_box = driver.find_element(By.XPATH,
                                     '//*[@id="app-main"]/div[1]/header/div[2]/div[2]/div[6]/button[1]/span/svg')

    search_box.send_keys("Camelia")
    assert search_box.text is not None

    try:
        select_element = driver.find_element(By.NAME, "sort_by")
        select = Select(select_element)
        select.select_by_visible_text("Price: Low to High")
    except NoSuchElementException:
        print("Выпадающий список не найден.")

    time.sleep(2)

    driver.execute_script("alert('Test Alert');")
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()

    driver.execute_script("prompt('Test Prompt');")
    prompt = WebDriverWait(driver, 10).until(EC.alert_is_present())
    prompt.send_keys("Some response")
    alert.dismiss()
