from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def gradConnectLogIn(driver, URL_LOGIN, USERNAME, PASSWORD):
    driver.get(URL_LOGIN)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(USERNAME)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(PASSWORD)
    
    # Clicking the login button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div[2]/section/div/div/div/div/div[1]/div[3]/button'))
    ).click()


def gradConnectScraper(driver, URL, connection):
    cur = connection.cursor()
    driver.get(URL)

    print(driver.title)
    time.sleep(3)

    links_to_visit = []
    job_list=[] 

    # First, collect all the links
    all_divs = driver.find_elements(By.CLASS_NAME, "box-name")
    for div in all_divs:
        div_link = div.find_element(By.TAG_NAME, 'a')
        links_to_visit.append(div_link.get_attribute('href'))


    for link in links_to_visit:
        driver.get(link) 

        
        #company_URL = gradConnectCompanyURL(driver)
        #driver.get(link)

        title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "employers-profile-h1"))
        ).text
        grad_URL = driver.current_url #change this to link? probably faster idk
        company = driver.find_element(By.CLASS_NAME, "employers-panel-title").text
        location = driver.find_element(By.XPATH, '//*[@id="app"]/span/div[3]/main/section/div[1]/div/div[2]/div/div[2]/div[2]/ul/li[4]/span/div/div').text
        deadline = driver.find_element(By.XPATH, "//li[contains(@class, 'box-content-catagories')][./strong[contains(text(), 'Closing Date:')]]").text

        data = (title, grad_URL, company, location, deadline)
        job_list.append(data)
        job_list.append((title, grad_URL, company, location, deadline))
        query = """
        INSERT INTO internships_gradconnect (title, url, company, city, deadline)
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, data)
        connection.commit()


        time.sleep(1)  # Small delay to ensure page loads

    for job in job_list:
        print(job)

    driver.quit()

def gradConnectCompanyURL(driver):
    try:
        # Wait for the "Apply" button
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-danger"))
        )
        # Click the button (opens a new tab)
        apply_button.click()
        # Wait for a new tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        # Wait for URL to load
        WebDriverWait(driver, 15).until(lambda driver: driver.current_url != "about:blank")
        company_url = driver.current_url
        # Close the new tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return company_url

    except Exception as e:
        print("Error retrieving company URL:", e)
        return None
