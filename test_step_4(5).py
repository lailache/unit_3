import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    yield driver
    driver.quit()


def test_accept_cookies_and_close_subscription(driver):
    driver.get("https://www.furla.com/gr/en/")

    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
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


def test_switch_windows_and_tabs(driver):
    driver.get("https://www.furla.com/gr/en/")
    main_window = driver.current_window_handle

    driver.execute_script("window.open('https://www.furla.com/gr/en/online_shop.html', '_blank');")
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    assert "Online Shop" in driver.title, "Новая вкладка не открылась или не переключилась"

    driver.close()
    driver.switch_to.window(main_window)

    assert "Furla" in driver.title, "Не вернулись в основное окно"


def test_handle_frames(driver):
    driver.get("https://www.furla.com/gr/en/")
    test_accept_cookies_and_close_subscription(driver)

    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name='example_frame']"))
        )

        frame_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "example_id"))
        )
        frame_element.click()

        driver.switch_to.default_content()
    except TimeoutException:
        print("Фрейм или элемент внутри фрейма не найден.")
