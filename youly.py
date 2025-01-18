import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging

logging.basicConfig(filename="scraping_errors.log", level=logging.ERROR)

def scrape_reviews():
    with open("valid_proxies.txt", "r") as f:
        proxies = f.read().splitlines()

    start_page = 1
    end_page = 10  
    data = []  
    counter = 0 

    for page in range(start_page, end_page + 1):
        try:
            proxy = proxies[counter % len(proxies)]  
            counter += 1

            chrome_options = Options()
            chrome_options.add_argument(f'--proxy-server={proxy}')

            driver = webdriver.Chrome(options=chrome_options)

            url = f"https://www.productreview.com.au/listings/youly?page={page}"
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.enable-container-query'))
            )

            review_containers = driver.find_elements(By.CSS_SELECTOR, 'div.enable-container-query')

            for container in review_containers:
                try:
                    time_element = container.find_element(By.TAG_NAME, 'time')
                    review_date = time_element.get_attribute('datetime')

                    rating_div = container.find_element(By.CSS_SELECTOR, 'div.L2HzME.H22X0I.Z1tQEL.ktks6p._XLHb7.INtA_9.P_x2fR.aI9zhb.SutvaQ')
                    style_attribute = rating_div.get_attribute('style')
                    rating_score = style_attribute.split('--pr-rating-score:')[1].split(';')[0].strip() if style_attribute else "N/A"

                    review_text = container.find_element(By.CSS_SELECTOR, 'div.Eq4SHG._xR2d7.rdvYUY').text

                    data.append({"Date/Time": review_date, "Stars": rating_score, "Review": review_text})

                except Exception as e:
                    logging.error(f"Error extracting data for a review on page {page}: {e}")

        except Exception as e:
            logging.error(f"Error loading page {page}: {e}")

        finally:
            driver.quit()  

    df = pd.DataFrame(data)
    df.to_csv("reviews.csv", index=False)
    print("Data saved to reviews.csv")

scrape_reviews()
schedule.every(12).weeks.do(scrape_reviews)
print("Scheduler is running... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)
