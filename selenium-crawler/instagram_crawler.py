import pdb
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

LOGIN_URL = 'https://www.instagram.com/accounts/login'
LOGIN_ID = 'dioscuroi'
LOGIN_PW = 'hahaha'

CRAWLING_URL = ''

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get(LOGIN_URL)
    browser.implicitly_wait(3)

    elem = browser.find_element(By.NAME, 'username')
    elem.send_keys(LOGIN_ID)

    elem = browser.find_element(By.NAME, 'password')
    elem.send_keys(LOGIN_PW + Keys.RETURN)

    browser.implicitly_wait(5)

    browser.get(CRAWLING_URL)

    time.sleep(10)