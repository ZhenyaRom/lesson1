# from django.urls import path
# from . import views
# urlpatterns = [
#     path('', views.index, name='index'), # Главная страница
# ]
from django.urls import path
from .views import IndexView, ProductListView, index, product_list, add_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
#    path('', ProductListView.as_view(), name='product_list_class'), # Метод as_view() подключает класс
]

