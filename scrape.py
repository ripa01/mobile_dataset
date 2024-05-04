from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os


def arogga_scrape(query):
    options = Options()
    
    options.headless = False
    options.binary_location = os.environ['BROWSER']
    driver = webdriver.Chrome(options=options)
    # Cache browser data for faster scraping
    datadir = os.environ['HOME'] + "/mts/Arogga"
    options.add_argument(f"user-data-dir={datadir}")

    # Send a request to the search page 
    driver.get(f"https://www.mobiledokan.co/category/mobiles/smartphones/")

    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/div[2]/div[2]/div[1]')))
    # element.click()

    try:
        # Wait for the page to load 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/ul')))
    except TimeoutException:
        # If no search results found, handle the case here
        driver.quit()
        return []
    # Now, you can collect all the search results 
    result_elements = driver.find_elements(By.XPATH, '//*[@id="main-content-row"]/div/div/div[1]/ul/li')
    
    total_items = len(result_elements)
    print(total_items)
    
    #  Create a list to store search results
    results = []

    # # logo =  './static/boibazar.png'
    for item_id in range(1, total_items ,2):
        try:
            title = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div[{item_id}]/div[1]/div[2]/div[1]')
            author = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div[{item_id}]/div[1]/div[2]/div[2]')
            price = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div[{item_id}]/div[1]/div[2]/div[3]/span[1]')
            image = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div[{item_id}]/div[1]/div[1]/a/img').get_attribute('src')
            link = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div[{item_id}]/div[1]/div[2]/div[1]/a').get_attribute('href')

            results.append({
                "title": title.text,
                "author": author.text,
                "price": price.text,
                "image": image,
                "link": link,
                # 'logo': logo,
            })

        except Exception as e:
            print(f"Error while processing item {item_id}: {str(e)}")

    # After scraping, close the browser window
    driver.quit()

 
    return results

# Call the function with your desired query
query = "Ecosprin 75"
results = arogga_scrape(query)

# Print the results in the terminal
for idx, result in enumerate(results, start=1):
    print(f"Result {idx}:")
    print(f"Title: {result['title']}")
    print(f"Author: {result['author']}")
    print(f"Price: {result['price']}")
    print(f"Image URL: {result['image']}")
    print(f"Link: {result['link']}")
    print()  

