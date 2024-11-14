from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

chrome_options = webdriver.ChromeOptions()
driver_path = "/usr/bin/chromedriver.131.0.6778.69"

driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

driver.get("https://texnique.xyz/")

try:
    print("Starting the game...")
    wait = WebDriverWait(driver, 10)
    game_window = wait.until(EC.presence_of_element_located((By.ID, "game-window")))
    print("Game window found!")
    start_button = wait.until(EC.presence_of_element_located((By.ID, "start-button-timed")))
    start_button.click()
    dynamic_text_old = ''
    while True:
        print('Processing...')
        point_text = driver.execute_script(
            "return document.querySelector('#game-window #problem-points').textContent"
        )
        print(point_text)
        problem_points = int(re.search(r'(\d+)', point_text).group(1))
        if problem_points < 10:
            driver.find_element(By.ID, "skip-button").click()
            continue

        dynamic_text = driver.execute_script(
            "return document.querySelector('#game-window div.latex .katex-mathml annotation').textContent"
        )
        print(dynamic_text)
        if dynamic_text == dynamic_text_old:
            print('No change in dynamic text')
            time.sleep(2)
            continue

        text_field = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        driver.execute_script("arguments[0].value = arguments[1];", text_field, dynamic_text)
        text_field.send_keys(' ')
        dynamic_text_old = dynamic_text
        time.sleep(2)

except Exception as e:
    print(e)
    print("An error occured. Ctrl+C to exit.")
    while True:
        continue
