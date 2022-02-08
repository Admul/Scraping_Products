from base64 import encode
from math import prod
from time import sleep
from turtle import end_fill
from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import random

# url = "http://health-diet.ru/table_calorie"

# Показываем сайту, что мы не бот
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}

# # Получаем код страницы
# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)

# # Записываем полученный код страницы в отдельный файл
# with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'w', encoding='utf-8') as file:
#     file.write(src)

# # Читает код страницы index.html
# with open(os.path.join(os.path.dirname(__file__), 'index.html'), encoding='utf-8') as file:
#     src = file.read()
    
# # Использования библиотеки BeatifullSoup4 вместе с библиотекой lxml
# soup = BeautifulSoup(src, "lxml")

# # Выбираем все ссылки страницы и выводим название ссылки и саму ссылку
# links = soup.find_all("a", class_="mzr-tc-group-item-href")

# # Записываем текст ссылки и саму ссылку в массив (ключ = значение)
# all_categories_dict = {}
# for item in links:
#     item_text = item.text
#     item_href = "http://health-diet.ru" + item.get("href")
    
#     all_categories_dict[item_text] = item_href
    
# # Записываем данные массива all_categories_dict в json файл
# with open(os.path.join(os.path.dirname(__file__), 'all_categories_dict.json'), "w", encoding="utf-8") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

# Получаем названия и ссылки из файла all_categories_dict.json
with open(os.path.join(os.path.dirname(__file__), 'all_categories_dict.json'), encoding="utf-8") as file:
    all_categories = json.load(file)
  
# Перебираем json файл  
iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")
for category_name, category_href in all_categories.items():
    
    # Замена символов ",", " ", "-", "\'" на "_"
    rep = [",", " ", "-", "\'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")       
    #print(category_name)

    # Получаем код страниц по ссылкам из json файла
    req = requests.get(url=category_href, headers=headers)
    src = req.text
    
    # Создаем страницу по полученному ранее коду из ссылки
    with open(os.path.join(os.path.dirname(__file__), f"data/{count}_{category_name}.html"), "w", encoding="utf-8") as file:
        file.write(src)
    
    # Чтение кода страницы
    with open(os.path.join(os.path.dirname(__file__), f"data/{count}_{category_name}.html"), encoding="utf-8") as file:
        file.read()
        
    soup = BeautifulSoup(src, "lxml")
    
    # Проверка страницы на наличие страницы с продуктами
    alert_block = soup.find(class_="uk-alert-danger")
    if(alert_block is not None):
        continue
    
    # Получаем заголовки таблиц
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    
    # Записываем заголовки в csv файл
    with open(os.path.join(os.path.dirname(__file__), fr"data/{count}_{category_name}.csv"), "w", newline='') as file:
        writer = csv.writer(file)
        try:
            writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
        except:
            pass
    
    # Собираем данные продуктов
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")
    
    product_info = []
    for item in products_data:
        products_tds = item.find_all("td")
        
        title = products_tds[0].find("a").text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text   
        
        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates  
            }
        )   
        
        with open(os.path.join(os.path.dirname(__file__), f"data/{count}_{category_name}.csv"), "a", newline="") as file:
            writer = csv.writer(file)
            try:
                writer.writerow(
                    (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                    )
                )
            except:
                pass
            
        with open(os.path.join(os.path.dirname(__file__), f"data/{count}_{category_name}.json"), "a", encoding="utf-8") as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)
        
    count += 1
    print(f"# Итерация {iteration_count}. {category_name} записан...")
    iteration_count -= 1
    
    if iteration_count == 0:
        print("Работа завершена")
        break
    
    print(f"Осталось итераций: {iteration_count}")
    # sleep(random.randrange(1, 2))
