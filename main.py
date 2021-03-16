from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import schedule
import os
from actions import auth


def fetch_upcoming_task():

    options = webdriver.ChromeOptions()
    options.binary_location= r"C:\Program Files\Google\Chrome\Application\chrome.exe" #path where chrome is located

    PATH = r"C:\Program Files (x86)\chromedriver.exe" # path where chrome driver is located
    driver = webdriver.Chrome(PATH, chrome_options=options)

    driver.get("https://htg.ope.ee/auth/?return=%2Fs%2F1635")

    auth.log_in(driver)

    def format_task_content(content):
        text = content.split("\n")
        return text

    try:

        tasks = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scheduled"))
        )

        date_of_first_task = tasks.find_elements_by_class_name("group_heading")[0]
        is_tommorow = "homme" in date_of_first_task.text # check if task is tomorrow
        print(is_tommorow)

        first_todo = tasks.find_elements_by_class_name("todo")[0]
        subject = first_todo.find_element_by_class_name("subject_name").text
        has_extra = EC.presence_of_element_located((By.CLASS_NAME, "scheduled-type-badge"))
        print("type of badge", has_extra)
        if has_extra:
            type_of_task = first_todo.find_element_by_class_name("scheduled-type-badge").text
        content = first_todo.find_element_by_class_name("todo_content").text
        formatted_content = format_task_content(content)

        

        todo_details = {}
        todo_details["subject"] = subject
        if type_of_task:
            todo_details["type"] = type_of_task
        todo_details["content"] = formatted_content

        time.sleep(3)

        # auth.log_out(driver)

    finally:
        driver.quit()


schedule.every(10).seconds.do(fetch_upcoming_task) # do task every 10 seconds

while True:
    schedule.run_pending()
    time.sleep(2)