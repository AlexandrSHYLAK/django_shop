from random import randint
from unicodedata import category


from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Product, Review, FavoriteProducts, Mail

from .forms import LoginForm, RegistrationForm, ReviewForm, ShippingForm, CustomerForm
from .utils import CartForAuthenticatedUser, get_cart_data

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
        context['reviews'] = Review.objects.filter(product=product).order_by('-pk')
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm

        return context


def login_registration(request):
    context = {'title': 'Войти или зарегистрироваться',
               'login_form': LoginForm,
               'registration_form': RegistrationForm}


    return render(request, 'shop/login_registration.html', context)


def user_login(request):
    """Аутентификация пользователя"""
    form =LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Неверное имя пользователя или пароль')
        return redirect('login_registration')

def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')

def user_registration(request):
    """Регистрация пользователя"""
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Аккаунт пользователя успешно создан")
        return redirect('index')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
        # messages.error(request, "Что-то пошло не так")
        return redirect('login_registration')

def save_review(request, product_pk):
    """Сохранение отзывов"""
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_pk)
        review.product = product
        review.save()
        return redirect('product_page', product.slug)


def save_favorite_product(request, product_slug):
    """Добавление или удаление товаров с избранных"""
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=product_slug)
        favorite_products = FavoriteProducts.objects.filter(user=user)
        if product in [i.product for i in favorite_products]:#кверисет разбираем в лист
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=user, product=product)

        next_page = request.META.get('HTTP_REFERER', 'category_detail')
        return redirect(next_page)

def save_subscribers(request):
    """Сохранение почтовых адресов"""
    email = request.POST.get('email')
    user =  request.user if request.user.is_authenticated else None
    if email:
        try:
            Mail.objects.create(mail=email, user=user)
        except IntegrityError:
            messages.error(request, "Вы уже подписаны")
    return redirect('index')

def send_mail_to_subscribers(request):
    """Отправка писем подписчикам"""
    from conf import settings
    from django.core.mail import send_mail
    if request.method == 'POST':
        text = request.POST.get('text')
        mail_list = Mail.objects.all()
        for email in mail_list:
            send_mail(
                subject="У нас новая акция",
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            print(f'Сообщение отправлено на почту: {email} ----- {bool(send_mail)}')
    context = {'title': 'Спамер'}
    return render(request, 'shop/send_mail.html', context)


def cart(request):
    """Страница корзины"""
    cart_info = get_cart_data(request)
    context = {'order': cart_info['order'],
               'order_products': cart_info['order_products'],
               'cart_total_quantity': cart_info['cart_total_quantity'],
               'title': 'Корзина'}

    return render(request, 'shop/cart.html', context)

def to_cart(request, product_id, action):
    """Добавляет товар в корзину"""
    if request.user.is_authenticated:
        CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        messages.error(request, 'Авторизируйтесь или зарегистрируйтесь чтобы совершать покупки')
        return redirect('login_regisration')





def checkout(request):
    """Страница оформления заказа"""
    cart_info = get_cart_data(request)
    context = {'order': cart_info['order'],
               'order_products': cart_info['order_products'],
               'cart_total_quantity': cart_info['cart_total_quantity'],
               'customer_form': CustomerForm(),
               'shipping_form': ShippingForm(),
               'title': 'Оформление заказа'}
    return render(request, 'shop/checkout.html', context)

class FavoriteProductsView(LoginRequiredMixin, ListView):
    """Вывод избранных товаров"""
    model = FavoriteProducts
    context_object_name = 'products'
    template_name = 'shop/favorite_products.html'
    login_url = 'user_registration'

    def get_queryset(self):
        """Получение товаровконкретного пользователя"""
        # user = self.request.user
        favs = FavoriteProducts.objects.filter(user=self.request.user)
        products = [i.product for i in favs]
        return products

def collections(request):
    """Страница Коллекций"""
    context = {'title': 'Коллекции'}
    return render(request, 'shop/collections.html', context)

def new_arrivals(request):
    """Страница Новых поступлений"""
    context = {'title': 'Новые поступления'}
    return render(request, 'shop/new_arrivals.html', context)

def sale(request):
    """Страница Распродажи"""
    context = {'title': 'Распродажи'}
    return render(request, 'shop/sale.html', context)

def accessories(request):
    """Страница Акссесуары"""
    context = {'title': 'Аксесуары'}
    return render(request, 'shop/accessories.html', context)

def about(request):
    """Страница О нас"""
    context = {'title': 'О нас'}
    return render(request, 'shop/about.html', context)

def contact(request):
    """Страница Контактов"""
    context = {'title': 'Контакты'}
    return render(request, 'shop/contact.html', context)