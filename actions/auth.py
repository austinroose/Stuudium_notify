import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def log_in(driver):

    username = driver.find_element_by_name("data[User][username]")
    enter_username = os.environ.get("STUUDIUM_USERNAME")
    username.send_keys(enter_username)

    password = driver.find_element_by_name("data[User][password]")
    enter_password = os.environ.get("STUUDIUM_PWD")
    password.send_keys(enter_password)

    password.send_keys(Keys.RETURN)


def log_out(driver):

    # get navigation menu button that opens hover menu
    upper_navigation = driver.find_element_by_id("stuudium-navigation")
    upper_menu_buttons = upper_navigation.find_elements_by_tag_name("span")
        for button in upper_menu_buttons:
            class_name = button.get_attribute("class")
            if class_name == "st-nav-item st-nav-item-with-menu st-nav-item_profile_tools":
                logout_hover_menu_button = button

    # move mouse to hover menu that contains logout button
    def hover_to_logout_menu(browser, menu_btn): 
        hover = ActionChains(browser).move_to_element(menu_btn)
        hover.perform()

    hover_to_logout_menu(driver, logout_hover_menu_button)

    # check within 5 seconds if logout button has appeared on screen, else raise an error
    # this is part where error is raised due to not finding element with associated class name 
    logout_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "st-nav-menu-contents-item st-nav-menu-contents-item-logout"))
    )

    def hover_to_logout_button_and_click(browser, button):
        actions = ActionChains(browser)
        actions.move_to_element(button)
        actions.perform()
    
    hover_to_logout_button_and_click(driver, logout_btn)