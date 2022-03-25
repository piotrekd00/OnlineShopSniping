from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
import os
import time
from playsound import playsound


def search_for_an_item():
    # a function to search for specific item
    # place your own path to the audio file in the playsound function
    login()
    while True:
        try:
            cls()
            print("Szukam dostępnego produktu...\n")
            add_item = Wait(driver, 4).until(
                ec.presence_of_element_located((By.CLASS_NAME, "btn.btn-lg.btn-primary.wybieram"))
            )
        except TimeoutException:
            driver.refresh()
        else:
            print("Znaleziono element!\n")
            playsound('###')
            add_item.click()
            Wait(driver, 60).until(ec.url_changes('https://sklep.tauron.pl/'))
            break

    shopping_cart()


def shopping_cart():
    # a function to go through the shopping cart
    driver.implicitly_wait(5)
    cart_button = driver.find_element(By.CLASS_NAME, 'btn.btn-lg.btn-primary.add_button')
    cart_button.click()

    Wait(driver, 60).until(ec.url_changes('https://sklep.tauron.pl/cart'))
    print("Tworzę zamówienie...")

    create_order()


def create_order():
    # a function to go through the process of placing an order and in case of an error repeat the process
    while True:
        first_order_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.btn-block.btn-lg')
        first_order_button.click()

        second_order_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.btn-block.btn-lg')
        second_order_button.click()

        if driver.find_element(By.CLASS_NAME, 'knefel-transfer-icon'):
            payment_method = driver.find_element(By.CLASS_NAME, 'knefel-transfer-icon')
            payment_method.click()
            time.sleep(2)
            order_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.btn-block.btn-lg')
            order_button.click()
        else:
            continue

        if driver.find_element(By.ID, 'form_summary[order_conditions][11]'):
            agreements = driver.find_element(By.ID, 'form_summary[order_conditions][11]')
            ActionChains(driver).move_to_element(agreements).click().perform()
            time.sleep(2)
            order_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.btn-block.btn-lg')
            order_button.click()
            break
        else:
            continue

    print("Złożono zamówienie!!!")


def login():
    # a function to log in to the website at the start of the whole process
    login_button = Wait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'text-bold.login-modal-link'))
    )
    login_button.click()

    # your email goes here
    email_form = driver.find_elements(By.CLASS_NAME, 'form-control.input-lg')[0]
    email_form.send_keys('###@###')

    # your password goes here
    password_form = driver.find_elements(By.CLASS_NAME, 'form-control.input-lg')[1]
    password_form.send_keys('###')

    login_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.btn-block.btn-lg')
    login_button.click()


def cls():
    # clearing the console
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    s = Service("C:\chromedriver.exe")
    options = webdriver.ChromeOptions()
    # put your local username in the place of '###'
    options.add_argument("--user-data-dir=C:\\Users\\###\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome(service=s, options=options)

    driver.get('https://sklep.tauron.pl/')
    driver.maximize_window()
    search_for_an_item()
