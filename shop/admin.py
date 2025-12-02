from django.contrib import admin
from .models import Product, Category, Gallery, Review, Mail, \
    Customer, Order, OrderProduct, ShippingAddress

from django.utils.safestring import mark_safe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title', )}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Колличество товаров'


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'create_at', 'size', 'color', 'get_photo')#creeated_at
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title')
    inlines = (GalleryInline, )
    readonly_fields = ('watched', )

    def get_photo(self, obj):
        if obj.images.all():
            # print(obj.images.all(), '------0')
            # print(obj.images.all()[0], '------1')
            # print(obj.images.all()[0].image, '------2')
            # print(obj.images.all()[0].image.url, '------3')
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


admin.site.register(Gallery)

admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение отзывов в админке"""
    list_display = ('pk', 'author', 'created_aat')
    readonly_fields = ('author', 'text', 'created_aat')


@admin.register(Mail)
class ReviewMail(admin.ModelAdmin):
    """Почтовые подписки"""
    list_display = ('pk', 'mail', 'user')
    readonly_fields = ('mail', 'user')


@admin.register(Order)
class ReviewOrder(admin.ModelAdmin):
    """Корзина"""
    list_display = ('customer', 'created_at', 'is_completed', 'shipping')
    readonly_fields = ('customer', 'is_completed', 'shipping')
    list_filter = ('customer', 'is_completed')

@admin.register(Customer)
class ReviewCustomer(admin.ModelAdmin):
    """Заказчики"""
    list_display = ('user', 'first_name', 'last_name', 'email')
    readonly_fields = ('user', 'first_name', 'email', 'last_name', 'phone')
    list_filter = ('user', )

@admin.register(OrderProduct)
class ReviewOrderProduct(admin.ModelAdmin):
    """Товары в заказах"""
    list_display = ('product', 'order', 'quantity', 'added_at')
    readonly_fields = ('product', 'order', 'quantity', 'added_at')
    list_filter = ('product', )

@admin.register(ShippingAddress)
class ReviewShippingAddress(admin.ModelAdmin):
    """Адреса доставки"""
    list_display = ('customer', 'city', 'state')
    readonly_fields = ('customer', 'order', 'city', 'state', 'street')
    list_filter = ('customer', )



