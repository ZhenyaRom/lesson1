from django.db import models


# Create your models here.
class Buyer(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_create_buyer = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return self.login


class Kind(models.Model):
    name_kind = models.CharField(max_length=50, verbose_name='Название вида')
    specification_kind = models.TextField(verbose_name='Описание вида')

    def __str__(self):
        return self.name_kind


class Category(models.Model):
    name_category = models.CharField(max_length=50, verbose_name='Название категории')
    specification_category = models.TextField(verbose_name='Описание категории')
    kind = models.ForeignKey(Kind, on_delete=models.PROTECT, verbose_name='Вид растения')

    def __str__(self):
        return self.name_category


class Product(models.Model):
    name_product = models.CharField(max_length=50, verbose_name='Название сорта')
    specification_product = models.TextField(verbose_name='Описание сорта')
    fabricator = models.CharField(max_length=50, verbose_name='Производитель')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество в упаковке')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    balance = models.PositiveIntegerField(verbose_name='Остаток')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name_product


class Order(models.Model):
    author_order = models.ForeignKey(Buyer, on_delete=models.DO_NOTHING, verbose_name='Автор заказа')
    name_buyer = models.CharField(max_length=100, verbose_name='Получатель')
    address_buyer = models.CharField(max_length=300, verbose_name='Адрес получателя')
    list_product = models.ManyToManyField(Product, related_name='Заказы')
    amount_order = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость заказа')
    date_create_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    active_order = models.BooleanField(default=True, verbose_name='Заказ активный?')
    text_order = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        return str(self.id)