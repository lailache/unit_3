from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def test_accept_cookies(driver):
    accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    assert accept_cookies_button is not None, "Кнопка принятия куки не найдена."
    accept_cookies_button.click()
    print("Кнопка принятия куки была успешно найдена и нажата.")


def test_search_elements(driver, accept_cookies, close_subscription):
    element_by_class = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "d-none d-xl-block"))
    )
    assert element_by_class is not None, "Element not found by class"

    element_by_css = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/gr/en/online_shop.html"]'))
    )
    assert element_by_css is not None, "Element not found by CSS"

    element_by_xpath = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Bags")]'))
    )
    assert element_by_xpath is not None, "Element not found by XPath"


def test_interact_elements(driver, accept_cookies, close_subscription):
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


def test_select_sort_by(driver, accept_cookies, close_subscription):
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "sort_by"))
    )
    assert select_element is not None, "Выпадающий список не найден."

    select = Select(select_element)
    select.select_by_visible_text("Price: Low to High")

    print("Выпадающий список успешно выбран.")


def test_alert(driver, accept_cookies, close_subscription):
    driver.get("https://www.furla.com/gr/en/")

    driver.execute_script("alert('Test Alert');")
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert alert is not None, "Алерт не был найден."
    alert.accept()
    print("Алерт был успешно найден и подтвержден.")


def test_prompt(driver, accept_cookies, close_subscription):
    driver.get("https://www.furla.com/gr/en/")

    driver.execute_script("prompt('Test Prompt');")
    prompt = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert prompt is not None, "Промт не был найден."
    prompt.send_keys("Some response")
    prompt.accept()
    print("Промт был успешно найден и подтвержден с вводом текста.")
