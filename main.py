from gc_sel import gradConnectScraper, gradConnectLogIn
from unsw_sel import unswScraper
from selenium import webdriver
import undetected_chromedriver as uc
import psycopg2

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread



def scrape_website(scraper_func, driver, url, connection):
    scraper_func(driver, url, connection )

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="passwordofallpasswords",
    host="localhost",
    port="5432"
)

URL_GC = "https://au.gradconnection.com/internships/computer-science/australia/"
URL_LOGIN_GC = "https://au.gradconnection.com/login/"
USERNAME = "notascraper36@gmail.com"
PASSWORD = "@Confirmpassword123"
driver_GC = webdriver.Chrome()

URL_UNSW = "https://careers.business.unsw.edu.au/search-jobs?locations=9692&study_fields=502&opportunity_types=2&defaults_applied=1"
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")


driver_UNSW = uc.Chrome(options=options)

scrapers = [
    (gradConnectScraper, driver_GC, URL_GC, connection),
    (unswScraper, driver_UNSW, URL_UNSW, connection),
]

gradConnectLogIn(driver_GC, URL_LOGIN_GC, USERNAME, PASSWORD)


with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [
        executor.submit(scrape_website, scraper_func, driver, url, db_connection)
        for scraper_func, driver, url, db_connection in scrapers
    ]
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Scraper raised an error: {e}")

driver_GC.quit()
driver_UNSW.quit()
connection.close()



