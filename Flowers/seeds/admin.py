from django.contrib import admin
from .models import *


@ admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'date_create_buyer',)
    search_fields = ('login', 'email', 'date_create_buyer',)


@ admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ('name_kind',)
    search_fields = ('name_kind',)


@ admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_category', 'kind',)
    search_fields = ('name_category', 'kind',)
    list_filter = ('kind',)


@ admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_product', 'category', 'balance',)
    search_fields = ('name_product', 'category', 'balance',)
    list_filter = ('category',)


@ admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_order', 'date_create_order', 'active_order', 'text_order',)
    search_fields = ('id', 'author_order', 'date_create_order',)
    list_filter = ('active_order', 'date_create_order',)

