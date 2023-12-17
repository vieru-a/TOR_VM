import json

from TOR_VM_store.models import *


def save_product(product, category):
    new_product = Product.objects.create(
        name=product['name'],
        image=product['image'],
        description=product['description'],
        article_number=product['article_number'],
        price=product['price'],
        cat=category,
    )
    print(f'Товар {new_product.article_number} сохранен')


def run():

    with open('TOR_VM_store/media/data.json', 'r') as f:
        data = json.load(f)

    for d in data:
        new_category = Category.objects.create(
            name=d['name'],
            image=d['image'],
            description=d['description'],
            type=Category.CATEGORY
        )
        print(f'Категория {new_category.name} сохранена')

        if 'subcategories' in d.keys():
            for s in d['subcategories']:
                new_subcategory = Category.objects.create(
                    name=s['name'],
                    image=s['image'],
                    description=s['description'],
                    type=Category.SUBCATEGORY,
                    parent=new_category
                )
                print(f'Подкатегория {new_subcategory.name} сохранена')

                for p in s['products']:
                    save_product(p, new_subcategory)

        else:
            for p in d['products']:
                save_product(p, new_category)
