from django.urls import path
from .views import *

urlpatterns = [
    path('kind/<str:name_kind>/', catalog, name='catalog'),
    path('basket/', basket, name='basket'),
    path('add_basket/<str:name_product>/<str:mark>/', add_basket, name='add_basket'),
    path('basket_order/', basket_order, name='basket_order'),
    path('login/', login_func, name='login_func'),
    path('registry/', registry, name='registry'),
    path('cabinet/<str:question>/', cabinet, name='cabinet'),
    path('contact/', contact_view, name='contact'),
    path('', home, name='home'),  # Главная страница
    ]

