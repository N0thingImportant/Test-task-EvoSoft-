from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

# Инициализация веб-драйвера (вам нужно указать путь к вашему драйверу)
driver = webdriver.Chrome()

# Шаг 1: Зайти на https://www.nseindia.com
driver.get("https://www.nseindia.com")

# Шаг 2: Навестись (hover) на MARKET DATA
market_data_menu = driver.find_element(By.LINK_TEXT, "MARKET DATA")
hover = ActionChains(driver).move_to_element(market_data_menu)
hover.perform()

# Шаг 3: Кликнуть на Pre-Open Market
pre_open_market = driver.find_element(By.LINK_TEXT, 'Pre-Open Market')
pre_open_market.click()

# Закрываем браузер
driver.quit()
