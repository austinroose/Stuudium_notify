from format import format_task_description
from sms.sms_sender import send_message

class Task:
    def __init__(self, subject, task_type, description): # when Object is being created initialize subject, type and description properties to it
        self.subject = subject
        self.task_type = task_type
        self.description = descriptions

def get_list_of_task_dates(driver):
    # wait until assignment panel is loaded in Stuudium while logging in first time could take some time
    tasks = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "scheduled"))
    )

    # get date strings of all days
    date_of_tasks = {}
    date_elements = tasks.find_elements_by_class_name("group_heading")
    for date in date_elements:
        date_of_tasks += date.text

    is_task_tomorrow = "homme" in date_of_tasks[0]

    tasks = get_list_of_tasks(tasks)

    if is_task_tomorrow:
        task = tasks[0] 
        send_first_task(task)

def get_list_of_tasks(container):
    tasks = {}

    tasks = container.find_elements_by_class_name("todo")
    for task_1 in tasks:
        subject = task_1.find_element_by_class_name("subject_name").text
        try:
            has_extra = EC.presence_of_element_located((By.CLASS_NAME, "scheduled-type-badge")) # if task has extra badge in UI such as "Kontrolltöö"
            type_of_task = task_1.find_element_by_class_name("scheduled-type-badge").text
        except:
            print("doesn't have extra")
        description = task_1.find_element_by_class_name("todo_content").text
        formatted_description = format_task_description(description)

        if "type_of_task" in locals():
            type_of_task = "Tunnitöö"

        task_object = Task(subject, type_of_task, description)

        tasks.append(task_object)
    
    return tasks

#send first task with all information to sms
def send_first_task(task_content):
    text = "Aine: " + task_content.subject + "\n" + "Tüüp: " + task_content.task_type + "\n" + "Sisu: " + task_content.description
    send_message(text)