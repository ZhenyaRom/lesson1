from django.contrib import admin
from .models import *


@ admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'date_create_buyer',)
    list_filter = ('login', 'email', 'date_create_buyer',)
    search_fields = ('login', 'email', 'date_create_buyer',)


@ admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ('name_kind',)
    search_fields = ('name_kind',)


@ admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_product', 'fabricator', 'amount', 'price', 'kind')
    search_fields = ('name_product', 'fabricator', 'amount', 'price', 'kind')
    list_filter = ('name_product', 'fabricator', 'amount', 'price', 'kind')


@ admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_order', 'date_create_order', 'active_order', 'text_order',)
    search_fields = ('id', 'author_order', 'date_create_order',)
    list_filter = ('active_order', 'date_create_order',)


@ admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')


# @ admin.register(Basket)
# class BasketAdmin(admin.ModelAdmin):
#     list_display = ('buyer', 'product', 'quantity')
#     search_fields = ('buyer', 'product')
#     list_filter = ('buyer', 'product')
