import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time


def scrape_trustpilot_reviews():
    url_base = 'https://au.trustpilot.com/review/myjuniper.com?page='
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    data = []

    for page in range(1, 36): 
        url = url_base + str(page)
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        r_first = soup.find('div', class_='styles_wrapper__Zhetz', attrs={"data-reviews-list-start": "true"})
        if not r_first:
            continue  
        r_second = r_first.find_all('div', class_='styles_cardWrapper__kOLEb styles_show__qAseP')

        for i in r_second:
            star = i.find('div', class_='star-rating_starRating__sdbkn star-rating_medium__Oj7C9')
            star_rate = star.find('img') if star else None
            rating = star_rate.get('alt').split(" ")[1].strip() if star_rate else "No Rating"

            desc_main = i.find('div', class_='styles_reviewContent__SCYfD', attrs={"aria-hidden": "false", "data-review-content": "true"})
            desc = desc_main.find('p', class_='typography_body-l__v5JLj typography_appearance-default__t8iAq', attrs={"data-service-review-text-typography": "true"}) if desc_main else None
            review = desc.text.strip() if desc else "No Review"

            date_tag = desc_main.find('p', class_='typography_body-m__k2UI7 typography_appearance-default__t8iAq', attrs={"data-service-review-date-of-experience-typography": "true"}) if desc_main else None
            date = date_tag.text.split("experience")[1].strip() if date_tag else "No Date"

            data.append({
                "Date": date,
                "Rating": rating,
                "Review": review,
            })

        print(f"Page {page} scraped successfully!")

    df = pd.DataFrame(data)
    df.to_csv('juniper_trustpilot.csv', index=False, encoding='utf-8')
    print("Data saved to 'juniper_trustpilot.csv'")


scrape_trustpilot_reviews()
schedule.every(2).weeks.do(scrape_trustpilot_reviews)

print("Scheduler is running... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)