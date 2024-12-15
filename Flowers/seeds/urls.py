from django.urls import path
from .views import catalog, login_func, basket, registry, welcome, home, contact_view, add_basket

urlpatterns = [
    path('add_basket/<str:name_product>/', add_basket, name='add_basket'),
    path('kind/<str:name_kind>/', catalog, name='catalog'),
    #path('catalog/', catalog, name='catalog'),
    path('login/', login_func, name='login_func'),
    path('basket/', basket, name='basket'),
    path('registry/', registry, name='registry'),
    path('contact/', contact_view, name='contact'),
    path('', home, name='home'),  # Главная страница
#    path('', welcome, name='welcome'),
    ]
#    path('', ProductListView.as_view(), name='product_list_class'), # Метод as_view() подключает класс
