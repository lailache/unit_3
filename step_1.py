from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.furla.com/gr/en/")
print(driver.title)
driver.quit()
