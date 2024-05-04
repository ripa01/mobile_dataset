import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

options = Options()

# Set the Brave browser executable path
brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
options = Options()
options.binary_location = brave_path


# Initialize the Chrome WebDriver with specified options
driver = webdriver.Chrome(options=options)


       
def scrape_data(url):
    # Send a request to the search page 
    driver.get(url)

    try:
    # Wait for the page to load 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/ul')))
    except TimeoutException:
    # If no search results found, handle the case here
        driver.quit()
    result_elements = driver.find_elements(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/ul/li')
    total_li = len(result_elements)
    print(total_li)
    data = []

    for i in range(1, total_li+1):
        print(f"Clicking on <li> element number {i}")

        li_element = driver.find_element(By.XPATH, f'//*[@id="main-content-row"]/div/div/div[1]/ul/li[{i}]')
        li_element.click()

        # Wait for elements on redirected page
        try:
            # Wait for the elements you want to scrape to be present on the redirected page 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]')))
        except TimeoutException:
            # If the elements are not found, handle the case here
            print("Elements not found on redirected page")
            continue

       
        try:
            brand = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/span[2]/a/span').text
        except:
            brand = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/span[3]/a/span').text #//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/span[3]
        price_element = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]/span')
        price = price_element.text if price_element.text else price_element.get_attribute("innerText")
        released = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[1]/strong').text
        os = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[2]/strong').text
        display = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[3]/strong').text
        camera = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]/strong').text
        ram = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[5]/strong').text
        battery = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[6]/strong').text

        # Append the scraped data to the list
        data.append({
            'Brand': brand,
            'Price': price,
            'Released': released,
            'OS': os,
            'Display': display,
            'Camera': camera,
            'RAM': ram,
            'Battery': battery
        })

        # Go back to the previous page
        driver.back()

    return data

# URL pattern for the pages
base_url = "https://www.mobiledokan.co/category/mobiles/smartphones/page/{}/"

# Create an empty list to store all data
all_data = []

# Iterate over multiple pages
for page_num in range(6,11): 
    print(f"Scraping data from page {page_num}")
    url = base_url.format(page_num)

    # Scrape data from the current page and append it to the list
    all_data.extend(scrape_data(url))
    

# Close the WebDriver
driver.quit()

# Create DataFrame from all_data
df = pd.DataFrame(all_data)

# Save DataFrame to Excel file
df.to_excel('mobile_data01.xlsx', index=False)
