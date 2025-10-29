from django.contrib import admin
from .models import Product, Category, Gallery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title', )}


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'create_at', 'size', 'color')#creeated_at
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title')
    inlines = (GalleryInline, )



admin.site.register(Gallery)
