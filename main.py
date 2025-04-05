from gc_sel import gradConnectScraper, gradConnectLogIn
from selenium import webdriver
import psycopg2

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="passwordofallpasswords",
    host="localhost",
    port="5432"
)

URL = "https://au.gradconnection.com/internships/computer-science/australia/"
URL_LOGIN = "https://au.gradconnection.com/login/"
USERNAME = "notascraper36@gmail.com"
PASSWORD = "@Confirmpassword123"
driver = webdriver.Chrome()


gradConnectLogIn(driver, URL_LOGIN, USERNAME, PASSWORD)
gradConnectScraper(driver, URL, connection)

