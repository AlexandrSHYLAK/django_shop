from  django.urls import path
from  .views import *


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<slug:slug>', SubCategories.as_view(), name='category_detail'),
    path('product/<slug:slug>', ProductPage.as_view(), name='product_page'),
    # path('', Contact.as_view(), name='contact'),
]