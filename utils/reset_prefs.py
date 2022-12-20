from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging


def reset_prefs(uname, pword):
    chrome_driver = webdriver.Chrome()
    try:
        chrome_driver.get('https://myadcenter.google.com/controls')

        username = chrome_driver.find_element(By.NAME, "identifier")
        username.send_keys(uname)  # username here
        chrome_driver.find_element(By.ID, "identifierNext").click()

        next_button = WebDriverWait(chrome_driver, 30).until(
            EC.element_to_be_clickable((By.ID, "passwordNext"))
        )
        password = WebDriverWait(chrome_driver, 30).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password.send_keys(pword)  # password here
        chrome_driver.execute_script("arguments[0].click();", next_button)

        my_ads = WebDriverWait(chrome_driver, 30).until(
                 EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz/div/div[2]/gm-coplanar-drawer/div/div/div/ul/li[1]/span[3]/span"))
        )
        chrome_driver.execute_script("arguments[0].click();", my_ads)

        try:
            see_all_topics = WebDriverWait(chrome_driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[2]/c-wiz[1]/div/div[1]/div/div/a"))
            )
            chrome_driver.execute_script("arguments[0].click();", see_all_topics)
        except TimeoutException:
            logging.info("Ad personalization is already turned off. Nothing to do.")
            return chrome_driver

        try:
            WebDriverWait(chrome_driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[2]/div[2]/span/div/c-wiz/div/ul"))
            )
            element_list = chrome_driver.find_element(By.XPATH, "/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[2]/div[2]/span/div/c-wiz/div/ul")
            items = element_list.find_elements(By.TAG_NAME, "li")

            interests_file = open(uname + "_interests.txt", "a+")
            for item in items:
                text = item.text
                interests_file.write(text + "\n")
            interests_file.close()
        except TimeoutException:
            logging.info("No topics in profile to be recorded")
            button = WebDriverWait(chrome_driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz/div/div[2]/div/c-wiz/div/c-wiz/div/div/div[1]/c-wiz/div/gm3-tonal-button"))
            )
            chrome_driver.execute_script("arguments[0].click();", button)

            turn_off_button = WebDriverWait(chrome_driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/div[2]/div/gm3-text-button[2]/button/span[1]"))
            )
            chrome_driver.execute_script("arguments[0].click();", turn_off_button)

            got_it_button = WebDriverWait(chrome_driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/gm3-text-button/button/span[1]"))
            )
            chrome_driver.execute_script("arguments[0].click();", got_it_button)
    except Exception as e:
        logging.error("Unknown Exception ", e)
    finally:
        return chrome_driver


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    creds_file = open("creds.txt", "r")
    lines = creds_file.readlines()
    for line in lines:
        creds = line.split(",")
        driver = reset_prefs(creds[0], creds[1])
        driver.close()