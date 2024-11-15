from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_switch_windows_and_tabs(driver, delete_all_cookies, accept_cookies, close_subscription):
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


def test_handle_frames(driver, delete_all_cookies, accept_cookies, close_subscription):
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name='example_frame']"))
    )

    frame_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example_id"))
    )
    assert frame_element.click(), "Фрейм не найден."

    driver.switch_to.default_content()
