import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

def scrape_reviews():
    data = []

    for page in range(1, 99):
        url = f'https://au.trustpilot.com/review/getmosh.com.au?page={page}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            continue

        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        div_1 = soup.find('div', class_='styles_wrapper__Zhetz', attrs={"data-reviews-list-start": "true"})
        if not div_1:
            continue 
        
        div_2 = div_1.find_all('div', class_='styles_cardWrapper__kOLEb styles_show__qAseP')
        for i in div_2:
            try:
                ms = i.find('section', class_='styles_reviewContentwrapper__Tzamw', attrs={"aria-disabled":"false"})
                rd = ms.find('div', class_='styles_reviewContent__SCYfD', attrs={"aria-hidden":"false","data-review-content":"true"})
                
                star1 = ms.find('div', class_='star-rating_starRating__sdbkn star-rating_medium__Oj7C9')
                star2 = star1.find('img')
                star = star2.get('alt').split(" ")[1]

                review1 = rd.find('p', class_='typography_body-l__v5JLj typography_appearance-default__t8iAq', attrs={"data-service-review-text-typography":"true"})
                review =review1.text.strip()

                date1 = rd.find('p', class_='typography_body-m__k2UI7 typography_appearance-default__t8iAq', attrs={"data-service-review-date-of-experience-typography":"true"})
                date2 = date1.find('span', class_='typography_body-m__k2UI7 typography_appearance-subtle__PYOVM')
                date_time = date2.text.strip()
                
                data.append({
                    'Date': date_time,
                    'Stars': star,
                    'Review': review
                })
            except AttributeError:
                continue
        print(f"Page {page} scraped successfully.")

    df = pd.DataFrame(data)
    df.to_csv('mosh_reviews.csv', index=False, encoding='utf-8')
    print("Data saved to mosh_reviews.csv")

scrape_reviews()
schedule.every(2).weeks.do(scrape_reviews)

print("Scheduler is running. The script will execute every 2 weeks.")

while True:
    schedule.run_pending()
    time.sleep(1)