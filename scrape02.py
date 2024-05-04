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

# Send a request to the search page 
driver.get("https://www.mobiledokan.co/category/mobiles/smartphones/")

try:
    # Wait for the page to load 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/ul')))
except TimeoutException:
    # If no search results found, handle the case here
    driver.quit()
       
# Now, you can collect all the search results 
result_elements = driver.find_elements(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/ul/li')
total_li = len(result_elements)
print(total_li)


for i in range(1, total_li+1):
    print(f"Clicking on <li> element number {i}")
    
    li_element  = driver.find_element(By.XPATH, f'//*[@id="main-content-row"]/div/div/div[1]/ul/li[{i}]').click()


    # Wait for elements on redirected page
    try:
        # Wait for the elements you want to scrape to be present on the redirected page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]')))
    except TimeoutException:
        # If the elements are not found, handle the case here
        print("Elements not found on redirected page")
        continue

    # Scrape the desired elements from the redirected page
    element1 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]/span')
    element2 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/span[2]/a/span')
    element3 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[1]/strong')
    element4 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[2]/strong')
    element5 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[3]/strong')
    element6 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]/strong')
    element7 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[5]/strong')
    element8 = driver.find_element(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[6]/strong')

    # Print or process the scraped elements
    print(element1.text)
    print(element2.text)
    print(element3.text)
    print(element4.text)
    print(element5.text)
    print(element6.text)
    print(element7.text)
    print(element8.text)

    # Go back to the previous page
    driver.back()


# Close the WebDriver
driver.quit()
