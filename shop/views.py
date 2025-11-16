from random import randint
from unicodedata import category

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Category, Product

class Index(ListView):
    """Главная страница"""
    model = Product
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}
    template_name = 'shop/index.html'

    def get_queryset(self):
        """ Вывод родительской категории"""
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, **kwargs):
        """вывод на страницу дополнительных элементов"""
        context = super().get_context_data()
        context['top_products'] = Product.objects.order_by('-watched')[:8]
        return context


class SubCategories(ListView):
    """Вывод подкатегории на отдельной странице"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        """Получение всех товаров подкатегории"""
        type_field = self.request.GET.get('type')
        if type_field:
            products = Product.objects.filter(category__slug=type_field)
            return products


        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subсategories.all()
        products = Product.objects.filter(category__in=subcategories).order_by('?')

        sort_field = self.request.GET.get('sort')
        if sort_field:
            products = products.order_by(sort_field)

        return products

    def get_context_data(self, *, object_list = ..., **kwargs):
        """Дополнительные элемеенты"""
        context = super().get_context_data()
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context

class ProductPage(DetailView):
    """Вывод товара на отдельной странице"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_page.html'

    def get_context_data(self, **kwargs):
        """Вывод на страницу дополнительных элементов"""
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = product
        # products = Product.objects.filter(category=product.category)
        # data = []
        # for i in range(5):
        #     random_index = randint(0, len(products) - 1)
        #     random_product = products[random_index]
        #     if random_product not in data and str(random_product) != product.title:
        #         data.append(random_product)
        # context['products'] = data

        data = Product.objects.all().exclude(slug=self.kwargs['slug']).filter(category=product.category)[:5]
        context['products'] = data
        return context
