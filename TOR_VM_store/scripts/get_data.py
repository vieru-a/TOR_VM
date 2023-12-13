import json
import os
import re

import requests

from bs4 import BeautifulSoup


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


def get_soup(url):
    u = url
    responce = requests.get(u, headers)
    soup = BeautifulSoup(responce.content, 'html.parser')
    return soup


def get_hrefs_list(soup, div_class):
    categories_list_links = [f'{e.find("a")["href"]}&limit=100' for e in soup.find_all('div', {'class': div_class})]
    return categories_list_links


def get_path(path, dir_name):
    dir_path = re.sub('[/"]', '_', dir_name)
    folder_path = f'{path}/{dir_path}'
    new_path = f'{path}/{dir_path}'
    number = 1

    try:
        os.mkdir(folder_path)
        new_path = folder_path
    except FileExistsError:
        while os.path.isdir(new_path):
            new_path = f'{folder_path} ({number})'
            number += 1
        os.mkdir(new_path)

    return new_path.strip(' ')


def save_product(url, path):

    soup = get_soup(url)
    product_data = {}
    lol = list(filter(lambda x: x != '', soup.find('ul', {'class': 'breadcrumb'}).text.split('\n')))

    if len(lol) == 1:
        product_data['cat'] = 'Матрицы металлические контурные'
        product_data['name'] = lol[-1]
    else:
        product_data['name'] = lol[-1]
        product_data['cat'] = lol[-2]

    for i in soup.find_all('ul', {'class': 'list-unstyled'}):
        for each_string in i:
            if 'Артикул' in each_string.text:
                product_data['article_number'] = each_string.text.strip('\n').lstrip('Артикул: ')
            elif 'руб' in each_string.text:
                product_data['price'] = float(each_string.text.strip('\n').rstrip(' руб'))

    product_data['description'] = soup.find('div', {'id': 'tab-description'}).text

    try:
        image_url = soup.find('a', {'class': 'thumbnail'})['href']
        product_data['image'] = save_image(image_url, product_data['article_number'], path)
    except TypeError:
        product_data['image'] = 'Нет данных'

    print(f'{product_data["article_number"]} - {product_data["name"]} - сохранен')

    return product_data


def save_category(url, path):
    soup = get_soup(url)
    category_data = {}

    lol = list(filter(lambda x: x != '', soup.find('ul', {'class': 'breadcrumb'}).text.split('\n')))
    category_data['name'] = re.sub('"', '_', lol[-1])

    try:
        image_url = soup.find('div', {'class': 'col-sm-2'}).find('img').get('src')
        category_data['image'] = save_image(image_url, category_data['name'], path)
    except AttributeError:
        category_data['image'] = 'Нет данных'

    try:
        category_data['description'] = soup.find('div', {'class': 'col-sm-10'}).text
    except AttributeError:
        category_data['description'] = 'Нет данных'

    print(f'{category_data["name"]} - категория сохранена')

    return category_data


def save_image(url, name, path):

    image = requests.get(url).content
    image_path = f'{path}/{name}.jpg'

    with open(image_path, 'wb') as f:
        f.write(image)

    return image_path.lstrip('TOR_VM_store/media/')


def run():
    if not os.path.isdir('TOR_VM_store/media'):
        os.mkdir('TOR_VM_store/media')

    data = []
    categories_data = []
    main_page = get_soup('https://mikond.top/index.php?route=product/category&path=136')

    for category_href in get_hrefs_list(main_page, 'image'):
        category_soup = get_soup(category_href)

        category_name = category_soup.find('div', {'class': 'col-sm-9'}).find('h2').text
        category_path = get_path('TOR_VM_store/media', category_name)
        current_data = save_category(category_href, category_path)
        subcategories_data = []
        products_data = []
        # получаем ссылки на страницу товара
        for product_href in get_hrefs_list(category_soup, 'image'):
            product_soup = get_soup(product_href)
            if product_soup.find('div', {'id': 'tab-description'}):

                product_name = product_soup.find('h1', {'class': 'media-heading'}).text
                product_path = get_path(category_path, product_name)
                products_data.append(save_product(product_href, product_path))

            # если есть подкатегория (sub)
            else:
                sub_category_name = product_soup.find('div', {'class': 'col-sm-9'}).find('h2').text
                sub_cat_path = get_path(category_path, sub_category_name)
                sub_prod = save_category(product_href, sub_cat_path)
                subproducts_data = []
                for sub_product in get_hrefs_list(product_soup, 'image'):
                    sub_soup = get_soup(sub_product)
                    if sub_soup.find('h1', {'class': 'media-heading'}):
                        sub_product_name = sub_soup.find('h1', {'class': 'media-heading'}).text
                        sub_product_path = get_path(sub_cat_path, sub_product_name)
                        subproducts_data.append(save_product(sub_product, sub_product_path))
                sub_prod['products'] = subproducts_data
                subcategories_data.append(sub_prod)

        if len(subcategories_data) != 0:
            current_data['subcategories'] = subcategories_data
        else:
            current_data['products'] = products_data

        data.append(current_data)

    with open('TOR_VM_store/media/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
