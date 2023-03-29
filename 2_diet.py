from time import sleep
import random
import requests
from bs4 import BeautifulSoup
import json
import csv

""" 
сохранякм главную страницу - этап один

url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

req = requests.get(url, headers=headers)
src = req.text
#print(src)

with open('diet.html', 'w') as file:
    file.write(src) """

"""
этап второй сохраняем json
 with open('diet.html') as file:
    src = file.read()


soup = BeautifulSoup(src, 'lxml')
all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')

all_categories_dict = {}
for item in all_products_hrefs:
    item_text = item.text
    item_href = 'https://health-diet.ru' + item.get('href')
    
    all_categories_dict[item_text] = item_href

with open('all_categories_dict.json', 'w') as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)  # ! важно     """

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')
for category_name, category_href in all_categories.items():

    #заменяем в названии категории все пробелы и тп на _

    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    #print(category_name)
    
    headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    
    req = requests.get(url=category_href, headers=headers)
    src = req.text 

    with open(f"data_diet/{count}_{category_name}.html", "w") as file:
        file.write(src)

    with open(f"data_diet/{count}_{category_name}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml') 
    #проверка на наличе таблицы
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    #собираем заголовок таблицы
    table_head = soup.find(class_='uk-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    
    with open(f'data_diet/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
            product,
            calories,
            proteins,
            fats,
            carbohydrates
            )
        )
    #собираем данные продуктов

    products_data = soup.find(class_='uk-table').find('tbody').find_all('tr')
    
    product_info = [] #делаем json

    for item in products_data:
        product_tds = item.find_all('td')
        title = product_tds[0].find('a').text
        # print(title)   
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text 

        product_info.append(   #добавляем для json
            {
            'Title': title,
            'Calories': calories,
            'Proteins': proteins,
            'Fats': fats,
            'Carbohydrates': carbohydrates
            }
        )

        with open(f'data_diet/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                title,
                calories,
                proteins,
                fats,
                carbohydrates
                )
            )
    #запись в json
    with open(f'data_diet/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
    #конец записи в json
    count += 1 
    print(f'# Итерация {count}. {category_name} записан ...')
    iteration_count = iteration_count - 1
    
    if iteration_count == 0:
        print('Работа завершена')
        break

    print(f'Осталось итераций: {iteration_count}')
    sleep(random.randrange(2,4))            