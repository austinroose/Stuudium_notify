from . import formating
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from sms import sms_sender

class Task:
    def __init__(self, subject, task_type, description): # when Object is being created initialize subject, type and description properties to it
        self.subject = subject
        self.task_type = task_type
        self.description = description

def get_list_of_task_dates(driver):
    # wait until assignment panel is loaded in Stuudium while logging in first time could take some time
    tasks = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "scheduled"))
    )

    # get date strings of all days
    date_of_tasks = []
    date_elements = tasks.find_elements_by_class_name("group_heading")
    for date in date_elements:
        date_of_tasks += date.text

    date_of_tasks2 = ''.join(map(str, date_of_tasks))

    is_task_today = "täna" in date_of_tasks2 # 

    tasks2 = get_list_of_tasks(tasks)

    if is_task_today:
        task = tasks2[0]  # get first task
        send_first_task(task)

def get_list_of_tasks(container):
    tasks_list = []

    tasks = container.find_elements_by_class_name("todo")
    for task_1 in tasks:
        subject = task_1.find_element_by_class_name("subject_name").text
        #try:
            # has_extra = EC.presence_of_element_located((By.CLASS_NAME, "scheduled-type-badge")) # if task has extra badge in UI such as "Kontrolltöö"
            # type_of_task = task_1.find_element_by_class_name("scheduled-type-badge scheduled-type-badge-hw").text
        #except:
            #print("doesn't have extra")

        type_of_task = "Tunnitöö" # for testing purpose, later fetch type from browser

        description = task_1.find_element_by_class_name("todo_content").text
        formatted_description = formating.format_task_description(description)

        task_object = Task(subject, type_of_task, description)

        tasks_list.append(task_object)
    
    return tasks_list

#send first task with all information throguh sms
def send_first_task(task_content):
    text = "Aine: " + task_content.subject + "\n" + "Tüüp: " + task_content.task_type + "\n" + "Sisu: " + task_content.description
    sms_sender.send_message(text)