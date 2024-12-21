from django.db import models


class Buyer(models.Model):
    """
    Класс таблицы в базе данных для хранения данных о пользователях.

    атрибуты: login, password, email, date_create_buyer.

    """
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_create_buyer = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return self.login


class Kind(models.Model):
    """
    Класс таблицы в базе данных для хранения названий видов растаний.

    атрибут: name_kind.

    """
    name_kind = models.CharField(max_length=50, verbose_name='Название вида')

    def __str__(self):
        return self.name_kind


class Product(models.Model):
    """
    Класс таблицы в базе данных для хранения данных о товарах.

    атрибуты: name_product, specification_product, price, kind.

    """
    name_product = models.CharField(max_length=50, verbose_name='Название сорта')
    specification_product = models.TextField(verbose_name='Описание сорта')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    kind = models.ForeignKey(Kind, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Вид')

    def __str__(self):
        return self.name_product


class Order(models.Model):
    """
    Класс таблицы в базе данных для хранения данных о оформленных заказах.

    атрибуты: author_order, name_buyer, address_buyer, list_product, amount_order, date_create_order, active_order,
    text_order.

    атрибут list_product хранит лист кортежей продуктов включенных в заказ с ценой и количеством.

    """
    author_order = models.ForeignKey(Buyer, on_delete=models.DO_NOTHING, verbose_name='Автор заказа')
    name_buyer = models.CharField(max_length=100, verbose_name='Получатель')
    address_buyer = models.CharField(max_length=300, verbose_name='Адрес получателя')
    list_product = models.TextField(verbose_name='Список товаров')
    amount_order = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость заказа')
    date_create_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    active_order = models.BooleanField(default=False, verbose_name='Заказ получен?')
    text_order = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        return str(self.id)


class Post(models.Model):
    """
    Класс таблицы в базе данных для хранения отправленных сообщений.

    атрибуты: name, email, message.

    """
    name = models.CharField(max_length=100, verbose_name="Ваше имя")
    email = models.EmailField(verbose_name="email")
    message = models.TextField(verbose_name='Сообщение')


class Basket(models.Model):
    """
    Класс таблицы в базе данных для хранения данных о товарах в корзине покупателя.

    атрибуты: buyer, product, quantity.

    """
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Хозяин корзины')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт в корзине")
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')

