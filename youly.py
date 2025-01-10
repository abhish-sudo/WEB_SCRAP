from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize the web driver
driver = webdriver.Chrome()

# Prepare a list to store the extracted data
data = []

# Define the number of pages you want to scrape
start_page = 1
end_page = 10  # Scrape pages from 1 to 10

for page in range(start_page, end_page + 1):
    # Construct the URL for the current page
    url = f"https://www.productreview.com.au/listings/youly?page={page}"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    # Locate all review containers
    review_containers = driver.find_elements(By.CSS_SELECTOR, 'div.enable-container-query')

    for container in review_containers:
        try:
            # Extract the date
            time_element = container.find_element(By.TAG_NAME, 'time')
            review_date = time_element.get_attribute('datetime').split('T')[0]  # Extract only the date

            # Extract the star rating from the style attribute
            rating_div = container.find_element(By.CSS_SELECTOR, 'div.L2HzME.H22X0I.Z1tQEL.ktks6p._XLHb7.INtA_9.P_x2fR.aI9zhb.SutvaQ')
            style_attribute = rating_div.get_attribute('style')
            if style_attribute:
                rating_score = style_attribute.split('--pr-rating-score:')[1].split(';')[0].strip() 
            else:
                rating_score = "N/A"  # Default if no rating is found

            # Extract the review text
            review_text = container.find_element(By.CSS_SELECTOR, 'div.Eq4SHG._xR2d7.rdvYUY').text

            # Append the extracted data to the list
            data.append({"Date/Time": review_date, "Stars": rating_score, "Review": review_text})

        except Exception as e:
            print(f"Error extracting data for a review: {e}")

# Close the web driver
driver.close()

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("reviews.csv", index=False)

print("Data saved to reviews.csv")
