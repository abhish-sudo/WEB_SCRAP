import requests
from bs4 import BeautifulSoup
import csv


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
else:
    price1 = "No price found"
    money_back = "No second price item found"


url2 = 'https://www.getmosh.com.au/weight-loss'
headers2 = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
soup2 = fetch_html(url2, headers=headers2)

featured_card = soup2.find('div', class_='comparison-cards_comparison-cards--card--content__UM_bp comparison-cards_comparison-cards--card--featured__sGTuO')
price_details = soup2.find_all('p', class_='comparison-cards_comparison-cards--card--price__fXu1O')
included_details = soup2.find_all('p', class_='comparison-cards_comparison-cards--card--includes__J8oBk')

featured_card_text = featured_card.text.strip() if featured_card else "Not found"
price2 = price_details[1].text.strip() if len(price_details) > 1 else "Second element of price not found"
included2 = included_details[1].text.strip() if len(included_details) > 1 else "Second element of includes not found"


url3 = 'https://youly.com.au/weight-loss-program/?gad_source=1&gbraid=0AAAAABrQSDMfOyTFemD_BcJjP7hQtr61v&gclid=CjwKCAiA-Oi7BhA1EiwA2rIu25-apRu6ItMX6X91SUHvdhE-8-ylFyZM-kfru_anYuSEA1Iw7bUrehoC-LgQAvD_BwE'
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
soup3 = fetch_html(url3, headers=headers3)

fed = soup3.find('div', class_='elementor-element elementor-element-6d3f685 elementor-widget elementor-widget-text-editor')
fed1 = soup3.find('div', class_="elementor-element elementor-element-ecf0bf9 elementor-widget elementor-widget-heading")
fed2 = soup3.find('div', class_="elementor-element elementor-element-54a3e1a elementor-icon-list--layout-traditional elementor-list-item-link-full_width elementor-widget elementor-widget-icon-list")
fed3 = soup3.find('div', class_="elementor-element elementor-element-87f0557 elementor-widget elementor-widget-heading")

fed_text = fed.text.strip() if fed else "Not found"
fed1_text = fed1.text.strip() if fed1 else "Not found"
fed2_text = fed2.text.strip() if fed2 else "Not found"
fed3_text = fed3.text.strip() if fed3 else "Not found"


csv_filename = 'weight_loss_data.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Source", "Price", "Details"])
    writer.writerow(["MyJuniper", price1, money_back])
    writer.writerow(["GetMosh", price2, f"{included2} | {featured_card_text}"])
    writer.writerow(["Youly", fed_text, f"{fed1_text} | {fed2_text} | {fed3_text}"])

print(f"Data has been written to {csv_filename}")
