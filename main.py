#from concurrent.futures import ThreadPoolExecutor
from gc_sel import gradConnectScraper, gradConnectLogIn
from unsw_sel import unswScraper
from selenium import webdriver
import undetected_chromedriver as uc
import psycopg2

#def scrape_website(scraper_func, driver, db_connection, url):
    #scraper_func(driver, url, db_connection)

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
#options.add_argument("--headless")



driver_UNSW = uc.Chrome(options=options)


gradConnectLogIn(driver_GC, URL_LOGIN_GC, USERNAME, PASSWORD)


scrapers = [
    (gradConnectScraper, driver_GC, URL_GC),
    (unswScraper, driver_UNSW, URL_UNSW)
]

# with ThreadPoolExecutor(max_workers=len(scrapers)) as executor:
#     for scraper_func, driver, url in scrapers:
#         executor.submit(scrape_website, scraper_func, driver, connection, url)
# with ThreadPoolExecutor(max_workers=1) as executor:
#     executor.submit(scrape_website, gradConnectScraper, driver_GC, connection, URL_GC)

# with ThreadPoolExecutor(max_workers=1) as executor:
#     executor.submit(scrape_website, unswScraper, driver_UNSW, connection, URL_UNSW)

gradConnectScraper(driver_GC, URL_GC, connection)
print("Launching UNSW scraper...")
unswScraper(driver_UNSW, URL_UNSW, connection)
