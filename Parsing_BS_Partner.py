import requests
from bs4 import BeautifulSoup
import os
import csv
import datetime

starttime = datetime.datetime.now()
starttime1 = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

url = 'https://bs-partner.com.ua/ua/catalog/'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
req = requests.get(url, headers=headers)
src = req.text

with open('html\index.html', 'w', encoding="utf-8") as file:
    file.write(src)

with open('html\index.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_products_hrefs = soup.find_all(class_="col-md-6 col-12")

all_categories_dict = {}
for item in all_products_hrefs:
    item_title = item.find('a').get('title')
    item_href = "https://bs-partner.com.ua" + item.find('a').get('href')
    all_categories_dict[item_title] = item_href

for category_name, category_href in all_categories_dict.items():
    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"html/{category_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f'html/{category_name}.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_products_hrefs = soup.find_all(class_="col-md-6 col-12")

    all_categories_tov_dict = {}
    for item in all_products_hrefs:
        item_title = item.find('a').get('title')
        item_href = "https://bs-partner.com.ua" + item.find('a').get('href') + '/?SHOWALL_1=1'
        all_categories_tov_dict[item_title] = item_href

    for category_name, category_href in all_categories_tov_dict.items():
        req = requests.get(url=category_href, headers=headers)
        src = req.text

        with open(f"html/{category_name}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f'html/{category_name}.html', encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_products_hrefs = soup.find_all(class_="prodname")

        all_tov_dict = {}
        for item in all_products_hrefs:
            item_title = item.get('title')
            item_href = "https://bs-partner.com.ua" + item.get('href')
            all_tov_dict[item_title] = item_href

        for tov_name, category_href in all_tov_dict.items():
            req = requests.get(url=category_href, headers=headers)
            src = req.text

            try:
                with open(f"html_tov/{tov_name}.html", "w", encoding="utf-8") as file:
                    file.write(src)
            except FileNotFoundError:
                print(f'Error - {tov_name}.html')


dir_name = "C:\Python\Parsing\parsing_BS_Partner\html_tov"
list = os.listdir(dir_name)

with open(f"bs_parner_{starttime1}.csv", "w", newline='', encoding="cp1251") as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            "name",
            "sku",
            "price",
            "image_href",
            "out_of_stock"
        )
    )

for item in list:
    with open(f'C:\Python\Parsing\parsing_BS_Partner\html_tov\{item}', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    name = soup.find('h1').text
    sku = soup.find(class_='prodarticul').find('span').text
    price = soup.find(class_='fullprice').find('span').text
    image_href = 'https://bs-partner.com.ua/' + soup.find(class_='bx_bigimages_aligner').find('a').get('href')
    try:
        out_of_stock = soup.find(class_='availability').find('span').text
        for x, y in ('Є на складі', '3'), ('Немає в наявності', '0'):
            out_of_stock = out_of_stock.replace(x, y)
    except AttributeError:
        out_of_stock = 0
        print(f'Error {name}')

    with open(f"bs_parner_{starttime1}.csv", "a", newline='', encoding="cp1251") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                name,
                sku,
                price,
                image_href,
                out_of_stock
            )
        )
diftime = datetime.datetime.now() - starttime
print(f'Start time : {starttime}')
print(f'Elapsed time : {diftime}')