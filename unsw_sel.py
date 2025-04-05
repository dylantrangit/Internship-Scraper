from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def unswScraper(driver, URL, connection):
    print("UNSW scraper started")
    cur = connection.cursor()
    driver.get(URL)
    print(driver.page_source[:500])  
    print(driver.title)
    time.sleep(5)

    links_to_visit = []

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
        deadline = driver.find_element(By.XPATH, "//span[starts-with(text(), 'Apply by')]").text


        data = (title, unsw_URL, company, location, deadline)
        query = """
        INSERT INTO internships_unsw (title, url, company, city, deadline)
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, data)
        connection.commit()
        
        


    driver.quit()
