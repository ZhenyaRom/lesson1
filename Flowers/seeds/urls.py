from django.urls import path
from .views import *

urlpatterns = [
    # При запросе каталога или выборе вида растения указываем путь к функции catalog
    path('kind/<str:name_kind>/', catalog, name='catalog'),
    # При запросе содержимого корзины указываем путь к функции basket
    path('basket/', basket, name='basket'),
    # При нажтии кнопки купить в каталоге или при изменении количества товара в корзине
    # указываем путь к функции add_basket
    path('add_basket/<str:name_product>/<str:mark>/', add_basket, name='add_basket'),
    # При запросе на оформление заказа указываем путь к функции basket_order
    path('basket_order/', basket_order, name='basket_order'),
    # При запросе на вход указываем путь к функции login_func
    path('login/', login_func, name='login_func'),
    # При запросе на регистрацию указываем путь к функции registry
    path('registry/', registry, name='registry'),
    # При входе в личный кабинет, при запросе на смену пароля, при запросе оформленных заказов
    # указываем путь к функции cabinet
    path('cabinet/<str:question>/', cabinet, name='cabinet'),
    #  При запросе на отправку сообщения указываем путь к функции contact_view
    path('contact/', contact_view, name='contact'),
    path('', home, name='home'),  # Главная страница
    ]

