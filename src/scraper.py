import os
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from module.mail.mailer import send_email

load_dotenv()

def start_browser():
    browser = webdriver.Firefox()
    return browser

def open_page(browser, url):
    browser.get(url)
    return browser

def page_navigation_by_class(browser, class_name):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, class_name))).click()

def fill_credetials(browser):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, os.getenv("TAG_LOGIN")))).send_keys(os.getenv('WEBSITE_LOGIN'))
    browser.find_element(By.ID, os.getenv("TAG_PASSWORD")).send_keys(os.getenv('WEBSITE_PASSWORD'))

def page_navigation_by_id(browser, id_name):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, id_name))).click()

def find_by_xpath(browser, xpath):
    element = browser.find_element(By.XPATH, xpath).text
    return element

def get_current_month():
    month = datetime.now().strftime("%B")
    return month

def get_calendar_month(browser):
    return find_by_xpath(browser, os.getenv("TAG_CALENDAR_XPATH")).split()[0]

def find_available_appointments(browser):
    if browser.find_elements(By.CLASS_NAME, os.getenv("TAG_HALF_BOOKABLE_DAY")) or browser.find_elements(By.CLASS_NAME, os.getenv("TAG_BOOKABLE_DAY")):
        span = browser.find_elements(By.CSS_SELECTOR, f".{os.getenv('TAG_BOOKABLE_DAY')} {os.getenv('TAG_SPAN_DAY')}, .{os.getenv('TAG_HALF_BOOKABLE_DAY')} {os.getenv('TAG_SPAN_DAY')}")
        index = len(span)
        available_days = list()
        for i in range(index):
            available_days.append(span[i].text)
            if len(available_days) == index:
                break
        body = f"Dear human,\n\nAvailable days were found in {get_calendar_month(browser)} {', '.join(available_days)} of 2022.\n\nPlease book your appointment at {os.getenv('WEBSITE_URL')}\n\nBest regards,\nYour personal assistant."
        send_email(body)
    else:
        if get_current_month() == get_calendar_month(browser):
            time.sleep(3)
            return move_to_next_month(browser)
        else:
            time.sleep(3)
            return move_to_previous_month(browser)

def move_to_next_month(browser):
    return page_navigation_by_id(browser, os.getenv("TAG_CALENDAR_NEXT_MONTH"))

def move_to_previous_month(browser):
    return page_navigation_by_id(browser, os.getenv("TAG_CALENDAR_PREVIOUS_MONTH"))

def main():
    browser = start_browser()
    open_page(browser, os.getenv('WEBSITE_URL'))
    page_navigation_by_class(browser, os.getenv("TAG_FORM_BUTTON"))
    fill_credetials(browser)
    page_navigation_by_class(browser, os.getenv("TAG_LOGIN_BUTTON"))
    page_navigation_by_id(browser, os.getenv("TAG_APPOINTMENT_BUTTON"))
    page_navigation_by_class(browser, os.getenv("TAG_EDIT_BOOKING_BUTTON"))
    while True:
        find_by_xpath(browser, os.getenv("TAG_CALENDAR_MONTH_SELECTOR"))
        find_available_appointments(browser)

main()