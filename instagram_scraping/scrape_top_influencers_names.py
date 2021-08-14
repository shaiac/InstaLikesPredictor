import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from posts_manager import PostsManager
from instagram_scraping.objects.influencer_data import InfluencerData

names = []

driver = webdriver.Chrome('C:/Tools/Chrome Driver/chromedriver.exe')
driver.get("https://hypeauditor.com/top-instagram/")
time.sleep(2)

driver.execute_script("window.scrollTo(0,250);")

next_button = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div[2]/div/div[3]/button[2]/i")
next_button.click()

time.sleep(2)

sign_in_button = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/div/div/div[3]/a/button")
sign_in_button.click()

# Login
email = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
email.clear()
password.clear()
email.send_keys("ronr94440@gmail.com")
password.send_keys("roniron123")
log_in = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
# not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),"
#                                                                                      " 'Not Now')]"))).click()

file = open("top_influencers.txt", "w")

for _ in range(2):
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0,700);")
    names_elements = driver.find_elements_by_xpath("//*[@class='contributor__name-content']")
    for name_element in names_elements:
        try:
            name = name_element.text
            file.write(f"{name}\n")
            print(name)
            names.append(name)
        except:
            continue
    time.sleep(2)
    next_button = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div[2]/div/div[3]/div/a[4]")
    next_button.click()


file.close()
