from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import schedule
import os
from actions import auth, todos


def fetch_upcoming_task():

    options = webdriver.ChromeOptions()
    options.binary_location= r"C:\Program Files\Google\Chrome\Application\chrome.exe" #path where chrome is located

    PATH = r"C:\Program Files (x86)\chromedriver.exe" # path where chrome driver is located
    driver = webdriver.Chrome(PATH, chrome_options=options)

    driver.get("https://htg.ope.ee/auth/?return=%2Fs%2F1635")

    auth.log_in(driver)

    todos.get_list_of_task_dates(driver)

    driver.quit()


schedule.every(30).seconds.do(fetch_upcoming_task) # do task every 10 seconds

while True:
    schedule.run_pending()
    time.sleep(30)