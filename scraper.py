from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import atexit
import requests
import os, signal
import json

def make_chrome_browser(run_headless=False, quit_on_done=False):
    options = webdriver.ChromeOptions()
    if run_headless: options.add_argument("headless")
    b = webdriver.Chrome(options=options)
    b.implicitly_wait(5)
    if quit_on_done: atexit.register(b.close)
    return b

browser = make_chrome_browser(quit_on_done=True)
def login():
    with open(os.path.join(os.path.dirname(__file__), "creds", "creds.json"), "r+") as jf:
        creds = json.load(jf)
    browser.find_element_by_class_name("SiteHeader-signInBtn").click()
    browser.find_element_by_id("username").send_keys(creds['username'])
    browser.find_element_by_id("password").send_keys(creds['password'])
    browser.find_elements_by_class_name("UIButton-wrapper")[-1].click()


def get_terms(qid):
    browser.get("https://quizlet.com/in/161425842/conectores-flash-cards/")
    login()
    item = browser.find_elements_by_class_name("SetPage-menuOption")[-1]
    item.click()
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//use[@xlink:href='#export']")))
    browser.find_element_by_xpath("//use[@xlink:href='#export']").click()

def kill_chromes():
    process = os.popen('ps aux')
    for p in process:
        if "chromedriver" in p:
            os.kill(int(list(filter(None, p.split(" ")))[1]), signal.SIGKILL)
kill_chromes()


# get_terms(161425842)

