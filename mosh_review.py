import requests
from bs4 import BeautifulSoup
import pandas as pd


data = []

for page in range(1, 99):
    url = f'https://au.trustpilot.com/review/getmosh.com.au?page={page}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    div_1 = soup.find('div', class_='styles_wrapper__Zhetz', attrs={"data-reviews-list-start": "true"})
    if not div_1:
        continue 
    
    div_2 = div_1.find_all('div', class_='styles_cardWrapper__kOLEb styles_show__qAseP')
    for i in div_2:
        try:
            date1 = i.find('div', class_='typography_body-m__k2UI7 typography_appearance-subtle__PYOVM')
            date2 = date1.find('time')
            date_time = date2.get('datetime')

            star1 = i.find('div', class_='star-rating_starRating__sdbkn star-rating_medium__Oj7C9')
            star2 = star1.find('img')
            star = star2.get('alt').split(" ")[1]

            review1 = i.find('div', class_='styles_reviewContent__SCYfD', attrs={"aria-hidden": "false", "data-review-content": "true"})
            review = review1.find('p').text.strip()

            data.append({
                'Date': date_time,
                'Stars': star,
                'Review': review
            })
        except AttributeError:
            continue
    print("Page {page} scraped successfully.")

df = pd.DataFrame(data)


df.to_csv('reviews.csv', index=False, encoding='utf-8')

print("Data saved to reviews.csv")
