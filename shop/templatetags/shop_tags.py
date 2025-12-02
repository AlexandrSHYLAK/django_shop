from multiprocessing.resource_tracker import register

from django import template
from shop.models import Category, FavoriteProducts
from django.template.defaulttags import register as range_register

register = template.Library()

@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)

@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Цена',
            'sorters': [
                ('price', 'по возрастанию'),
                ('-price', 'по убыванию')
            ]
        },
        {
            'title': 'Цвет',
            'sorters': [
                ('color', 'от А до Я'),
                ('-color', 'от Я до А')
            ]
        },
        {
            'title': 'Размер',
            'sorters': [
                ('size', 'по возрастанию'),
                ('-size', 'по убыванию')
            ]
        }
    ]
    return sorters


@register.simple_tag()
def get_favorite_products(user):
    """Вывод избранных товаров"""
    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products