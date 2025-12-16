from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование категории")
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Категория', related_name='subсategories')

    def get_absolute_url(self):
        """Ссылка на страницу категории"""
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def get_parent_category_photo(self):
        """ для получения картинки родительской категории"""
        if self.image:
            return self.image.url
        else:
            return 'https://smtenergo.ru/static/img/nopic.jpg'

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    price = models.FloatField(verbose_name='Цена')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')#creeated_at
    watched = models.IntegerField(default=0, verbose_name='просмотры')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Здесь скоро будет описание', verbose_name='Описание товара')
    info = models.TextField(default='Дополнительная информация о продукте', verbose_name='Информация о товаре')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Размер в мм')
    color = models.CharField(max_length=30, default='Серебро', verbose_name='Цвет/Материал')

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images.first():
            return self.images.first().image.url
        else:
            return 'https://smtenergo.ru/static/img/nopic.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Товар: pk={self.pk}, title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображения')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'


class Review(models.Model):
    """Модель для отзывов"""
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    created_aat = models.DateField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class FavoriteProducts(models.Model):
    """Избранные товары"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'



class Mail(models.Model):
    mail = models.EmailField(unique=True, verbose_name='Почта')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почты'

class Customer(models.Model):
    """Контактная информация заказчика"""
    user = models.OneToOneField(User, models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    # phone = models.CharField(max_length=255, verbose_name='Контактный телефон')
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

class Order(models.Model):
    """Корзина"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    is_completed = models.BooleanField(default=False, verbose_name='Завершен')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        """Для получения суммы товаров в корзине"""
        order_products = self.ordered.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        """Получение количество товаров в корзине"""
        order_products = self.ordered.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity



class OrderProduct(models.Model):
    """Привязка продукта к корзинеб строчки товаров"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='ordered')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

    @property
    def get_total_price(self):
        """Сам считает общую цену товаров"""
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    """Адресс доставки"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=255, verbose_name='Страна', null=True)
    city = models.CharField(max_length=255, verbose_name='Город')
    state = models.CharField(max_length=255, verbose_name='Область')
    street = models.CharField(max_length=255, verbose_name='Улица/Дом/Квартира')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'




