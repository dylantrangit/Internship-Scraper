from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
import time

URL = "https://careers.business.unsw.edu.au/search-jobs?locations=9692&study_fields=502&opportunity_types=2&defaults_applied=1"
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)
driver.get(URL)
print(driver.title)
time.sleep(5)

links_to_visit = []

#all_lists = driver.find_elements(By.CLASS_NAME, "SearchResultsstyle__SearchResult-sc-c560t5-1 hlOmzw")/
all_lists = driver.find_elements(By.CSS_SELECTOR, "li.SearchResultsstyle__SearchResult-sc-c560t5-1.hlOmzw")
for list in all_lists:
    list_link = list.find_element(By.TAG_NAME, 'a')
    links_to_visit.append(list_link.get_attribute('href'))


for link in links_to_visit:
    driver.get(link)

    title = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    ).text
    unsw_URL = link
    company = driver.find_element(By.XPATH, "//ul[@class='breadcrumbs']/li[3]/a/span").text
    location = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[3]/div/div/div[2]/div/div/section/div[1]/section/div[1]/div/p').text
    print(location)

driver.quit()
