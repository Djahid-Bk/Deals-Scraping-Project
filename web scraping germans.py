from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

def scrape_deals():
    # Set up the Selenium WebDriver service with the path to chromedriver.exe
    service = Service(executable_path="D:\Work\Coding\Web Scraping\Selenium\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # URL of the first page to scrape
    link="https://www.mydealz.de/new?page=2"
    driver.get(link)

    # Extract the last page number from the pagination
    last_page_text=driver.find_element(By.XPATH,"//*[@id='toc-target-deals']/div[1]/div[2]/nav/button[5]").text
    last_page=int(last_page_text)

    # Initialize the page counter
    page=1
    link="https://www.mydealz.de/new?page="

    # Open the CSV file for writing and write the header row
    csv_file = open("deals.csv", "w",encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Title", "Price","Rating" ,"Seller","Description","Images","Redirect Link","Link"])

    # Loop through each page
    while(page<=last_page):
        # Navigate to the current page
        driver.get(link+str(page))
        
        # Find all product links on the page
        product_links_elements=driver.find_elements(By.XPATH,"//a[contains(@class, 'cept-tt thread-link linkPlain thread-title--list js-thread-title')]")
        
        # Extract the href attribute from each link element
        product_links = []
        for links in product_links_elements:
            product_links.append(links.get_attribute("href"))
        
        # Loop through each product link
        for linker in product_links:
            driver.get(linker)
            time.sleep(0.5)
            
            # Attempt to click the cancel button, if present
            try:
                cancel=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/section/div/div/footer/button[1]/span").click()
            except:
                i=1    
            
            # Attempt to click the cookies button, if present
            try:   
                cookies=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/section/div/div/div/div/div/div[2]/div[2]/button[1]").click()
            except:
                i=1
            
            # Extract product details
            try:
                title=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[2]/div[3]/h1/span").text.strip()
            except NoSuchElementException:
                title='N/A'
            
            # Continue extracting other product details...
            try:
                price=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[2]/span/span[1]/span").text
            except NoSuchElementException:
                price = 'N/A'

            try:
                seller=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[2]/div[4]/button").text   
            except NoSuchElementException:
                seller= 'N/A'

            try:
                time.sleep(0.5)
                element = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[2]/div[5]/button")
                # Move the mouse to the element, click and hold it
                actions = ActionChains(driver)
                actions.move_to_element(element).click_and_hold().perform()
                # Move the mouse 300px to the left
                actions = ActionChains(driver)
                actions.move_by_offset(-300, 0).perform()
                # Release the mouse button
                actions = ActionChains(driver)
                actions.release().perform()
                time.sleep(0.5)
                redirect_link=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[2]/div[5]/a").get_attribute("href")
            except NoSuchElementException:
                redirect_link= 'N/A'

            try:
                rating=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[2]/div[1]/div[1]/span").text
            except NoSuchElementException:
                Rating= 'N/A'

            try:
                description=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[3]/div[4]/div/div[1]/div").text.replace('\n', ' ')
            except NoSuchElementException:
                description= 'N/A'  

            try:
                image_element=driver.find_elements(By.XPATH,"//div/button/span/div/img")
                images = [img.get_attribute('src').replace("150x150","1024x1024") for img in image_element]
                if not images:
                    images=driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/div/div[1]/div[1]/div/section/div/div[2]/div[1]/div/div/span/picture/img").get_attribute('src').replace("768x768","1024x1024")
            except NoSuchElementException:
                images="N/A"   
            
            # Write the extracted details to the CSV file
            csv_writer.writerow([title, price ,rating ,seller ,description,images,redirect_link,linker])
        
        # Increment the page counter
        page=page+1

    # Close the CSV file
    csv_file.close()

# Run the scrape_deals function in a loop every 3 hours
while True:
    scrape_deals()
    time.sleep(10800) # Pause for 3 hours (10800 seconds)