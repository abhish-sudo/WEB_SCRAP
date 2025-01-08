import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_html(url, headers=None):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')

url1 = 'https://www.myjuniper.com/faq#pricing'
soup1 = fetch_html(url1)
prices = soup1.find('div', id='pricing', class_='faq-block-wrapper')

if prices:
    price_text = prices.find('div', class_='faq-content-rich-text w-richtext').text.strip()
    price1 = price_text.split("from")[1].strip() if "from" in price_text else "No price found"
    money = prices.find_all('div', attrs={'role': 'listitem'}, class_='collection-item w-dyn-item')
    money_back = money[1].text.strip() if len(money) > 1 else "No second price item found"
    features1 = price_text.split("Our treatment")[0].strip() 
else:
    price1 = "No price found"
    features1 = "No features found"
    money_back = "No money back info found"



url2 = 'https://www.getmosh.com.au/weight-loss'
headers2 = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
soup2 = fetch_html(url2, headers=headers2)

featured_card = soup2.find('div', class_='comparison-cards_comparison-cards--card--content__UM_bp comparison-cards_comparison-cards--card--featured__sGTuO')
price_details = soup2.find_all('p', class_='comparison-cards_comparison-cards--card--price__fXu1O')
included_details = soup2.find_all('p', class_='comparison-cards_comparison-cards--card--includes__J8oBk')

price2 = price_details[1].text.strip() if len(price_details) > 1 else "No price found"
features2 = included_details[1].text.strip() if len(included_details) > 1 else "No features found"
money_back2 = featured_card.text.strip() if featured_card else "No money back info found"


url3 = 'https://youly.com.au/weight-loss-program/?gad_source=1&gbraid=0AAAAABrQSDMfOyTFemD_BcJjP7hQtr61v&gclid=CjwKCAiA-Oi7BhA1EiwA2rIu25-apRu6ItMX6X91SUHvdhE-8-ylFyZM-kfru_anYuSEA1Iw7bUrehoC-LgQAvD_BwE'
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
soup3 = fetch_html(url3, headers=headers3)

price3 = soup3.find('div', class_="elementor-element elementor-element-87f0557 elementor-widget elementor-widget-heading").text.strip() 
features3 = soup3.find('div', class_='elementor-element elementor-element-6d3f685 elementor-widget elementor-widget-text-editor').text.strip()
money_back3 = soup3.find('div', class_="elementor-element elementor-element-ecf0bf9").text.strip() if soup3.find('div', class_="elementor-element elementor-element-ecf0bf9") else "No money back info found"



data = [
    {"Source": "MyJuniper", "Price": price1, "Features": features1, "Money Back": money_back},
    {"Source": "GetMosh", "Price": price2, "Features": features2, "Money Back": money_back2},
    {"Source": "Youly", "Price": price3, "Features": features3, "Money Back": money_back3}
]

df = pd.DataFrame(data)


csv_filename = 'weight_loss_data_with_source.csv'
df.to_csv(csv_filename, index=False)

print(f"Data has been saved to {csv_filename}")
