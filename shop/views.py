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
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subсategories.all()
        products = Product.objects.filter(category__in=subcategories).order_by('?')
        return products


# class Contact(ListView):
#     """Контакты"""
#     model = Product
#     context_object_name = 'contact'
#     extra_context = {'title': 'Контакты'}
#     template_name = 'shop/contact.html'