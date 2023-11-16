from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import re
import pandas as pd
import time 
import pycountry
import requests
from selenium.webdriver.common.alert import Alert
from unidecode import unidecode

geckodriver_path = 'Users\Twinkles\code\geckodriver'

driver = webdriver.Firefox(executable_path=geckodriver_path)
# driver = webdriver.Chrome()
#go ahead and open the auction url

driver.get('https://www.christies.com/calendar?mode=1&sc_lang=en&lid=1')
sleep(30)
# Wait for the button to be clickable
# wait = WebDriverWait(driver, 10)
div = driver.find_element(By.ID,"iSignUp")
form = div.find_element(By.CSS_SELECTOR,".fsu--wrapper")
div_2 = form.find_element(By.ID,"close_signup")
close_sign = div_2.find_element(By.TAG_NAME,"svg")
close_sign.click()

# privacy container
div_3 = driver.find_element(By.CLASS_NAME,"ot-sdk-container")
div_4 = div_3.find_element(By.CLASS_NAME,"ot-sdk-row")
div_5 = div_4.find_element(By.ID,"onetrust-button-group-parent")
div_6 = div_5.find_element(By.ID,"onetrust-button-group")
div_7 = div_6.find_element(By.CLASS_NAME,"banner-actions-container")
div_8 = div_7.find_element(By.TAG_NAME,"button")
div_8.click()

#Sign in button
sign_in_area = driver.find_element(By.CLASS_NAME,"container-fluid")

# div.chr-header__panel:nth-child(1) > div:nth-child(1) > div:nth-child(1)
div_9 = sign_in_area.find_element(By.CSS_SELECTOR,"div.chr-header__panel:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
div_10 = div_9.find_element(By.CSS_SELECTOR,".chr-header__user-zone")
div_11 = div_10.find_element(By.CSS_SELECTOR,".chr-header__user-zone > chr-button:nth-child(1)")
div_12 = div_11.find_element(By.CSS_SELECTOR,".chr-button--sm")
div_13 = div_12.find_element(By.CSS_SELECTOR,".chr-button--sm > span:nth-child(1)")
div_13.click()

#Access the form
sign_in_form = driver.find_element(By.TAG_NAME,"form")
#username
div_14 = sign_in_form.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[1]")
div_15 = div_14.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[1]/chr-text-input/div[1]")
div_16 = div_15.find_element(By.ID,"username")
div_16.send_keys("jacobwamanidata@gmail.com")

#password
div_17 = sign_in_form.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[2]")
div_18 = div_17.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[2]/chr-text-input")
div_19 = div_18.find_element(By.ID,"password")
div_19.send_keys("SkyisBlue@1")

# Click the button
div_20 = sign_in_form.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[4]")
div_21 = div_20.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[4]/chr-button")
div_22 = div_21.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[4]/chr-button/button")
div_23 = div_22.find_element(By.XPATH,"/html/body/div[5]/chr-modal-provider/chr-modal/div/div[2]/div/div/div/div[2]/chr-modal-login/div/chr-form/form/div[4]/chr-button/button/span")
div_23.click()

div_9 = div_8.find_element(By.CSS_SELECTOR,"div.chr-header__panel:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
div_10 = div_9.find_element(By.CSS_SELECTOR,".chr-header__user-zone")
div_11 = div_10.find_element(By.CSS_SELECTOR,".chr-header__user-zone > chr-button:nth-child(1)")
div_12 = div_11.find_element(By.CSS_SELECTOR,".chr-button--sm")
div_12.click()


# Click the button

# sleep(10)


# sleep(5)
# Close the WebDriver
# driver.quit()