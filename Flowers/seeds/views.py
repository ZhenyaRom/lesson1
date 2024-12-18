from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .forms import ContactForm
from .models import *


user = Buyer.objects.get(id=1)  # пока не выполнен вход, присваиваем технический buyer
per_page = 3  # стартовое количество товаров на странице


def home(request):  # Функция для подготовки главной страницы
    # Создаем переменные которые нам нужны на главной странице
    post = ("Мы рады Вас видеть в нашем интернет-магазине семян! "
            "Мы продаем семена ведущих мировых и российских производителей!")
    post_plus = ("Ассортимент нашего Интернет-магазина постоянно пополняется. Если Вы желаете найти необходимый Вам "
                 "товар, то самый простой способ - воспользуйтесь нашим каталогом. Все товары разбиты на товарные группы"
                 "по которым можно отсортировать список товаров."
                 "Найти товар можно также при помощи поисковой системы.  Для этого необходимо набрать слово в форме "
                 "запроса и нажать на кнопку справа. Результатом Вашего поиска будет список товаров имеющих это слово "
                 "или словосочетание в описании или названии.")
    # Сохраняем в словарик для передачи созданные переменные для home.html и user, он нужен на всех страницах,
    # т.к. используется в базовом шаблоне
    context = {
        'post': post,
        'post_plus': post_plus,
        'user': user
    }
    return render(request, 'seeds/home.html', context)  # Переход на главную страницу home.html


def contact_view(request):  # Функция для отправки сообщений
    context = {'user': user}  # Записываем в context user
    if request.method == 'POST':  # Если метод POST
        form = ContactForm(request.POST)  # получаем введенные данные
        if form.is_valid():  # Если форма валидна, обрабатываем данные
            # Присваиваем значения введенных полей в переменные
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            Post.objects.create(name=name, email=email, message=message)  # Записываем в базу
            post = f"Спасибо, {name}! Мы получили ваше сообщение."  # Создаем сообщение об успешной отправке
            context['post'] = post  # Сохраняем в context для передачи
            return render(request, 'seeds/home.html', context)  # Переход на главную страницу
    else:  # Если метод не POST
        form = ContactForm()  # Создаем пустую форму
        context['form'] = form  # Сохраняем для передачи
        return render(request, 'seeds/contact.html', context)  # Переход на страницу сообщений


def cabinet(request, question=''):  # Функция для обработки данных в личном кабинете
    context = {'user': user}  # Сохраняем для передачи user
    if user == Buyer.objects.get(id=1):  # Если user не выполнил вход
        # Пишем сообщение и выгоняем из кабинета
        post = 'Чтобы попасть в личный кабинет нужно войти или зарегистрироваться'
        context['post'] = post
        return render(request, 'seeds/home.html', context)
    if request.method == 'POST':  # Если метод POST
        context['new_password_true'] = True  # переменная для вывода формы на смену пароля в cabinet.html
        password = request.POST.get('password')  # получаем значения введенных переменных
        new_password = request.POST.get('new_password')
        new_password_again = request.POST.get('new_password_again')
        if password == user.password:  # Если введенный пароль соответствует действующему
            if new_password == new_password_again:  # Если новый пароль повторен правильно
                user.password = new_password  # Записываем и сохраняем новый пароль
                user.save()
                post = f'{user}, вы успешно поменяли пароль.'  # Пишем сообщение
                context['post'] = post
                return render(request, 'seeds/home.html', context)  # Выходим на главную страницу
            context['error'] = 'Пароли не совпадают'  # Если новый пароль повторен неверно, пишем об этом
            return render(request, 'seeds/cabinet.html', context)  # и возвращаемся
        context['error'] = 'Неверный пароль'  # Если введенный пароль не соответствует действующему, пишем об этом
        return render(request, 'seeds/cabinet.html', context)  # и возвращаемся
    else:  # Если метод GET
        if question == 'my_order':  # Если запрос на список оформленных заказов
            filtered_order = Order.objects.filter(author_order__id=user.id)  # выбираем заказы
            context['filtered_order'] = filtered_order  # сохраняем заказы для передачи
            return render(request, 'seeds/cabinet.html', context)  # возврвщаемся
        elif question == 'new_password':  # Если запрос на смену пароля
            context['new_password_true'] = True  # переменная для отображения формы на смену пароля в cabinet.html
            return render(request, 'seeds/cabinet.html', context)  # возвращаемся
        else:
            return render(request, 'seeds/cabinet.html', context)  # идем в cabinet.html


def add_basket(request, name_product, mark='+'):  # Функция для добавления товаров в корзину и изменения количества
    if user == Buyer.objects.get(id=1):  # Если user не вошел или не зарегистрировался
        post = 'Чтобы совершать покупки нужно войти или зарегистрироваться'  # пишем об этом сообщение
        context = {'post': post}  # передаем сообщение в контекст
        return render(request, 'seeds/home.html', context)  # Переходим не главную
    # Если вход выполнен
    product = Product.objects.get(name_product=name_product)  # Достаем объект из базы по названию
    if Basket.objects.filter(buyer=user, product=product).exists():  # Если в корзине user-а есть такой товар
        my_basket = Basket.objects.get(buyer=user, product=product)  # Достаем объект из корзины
        if mark == '+':  # Если была нажата кнопка "+"
            my_basket.quantity = my_basket.quantity + 1  # Увеличиваем количество на 1
            my_basket.save()  # Сохраняем объект
        else:  # Если была нажата кнопка "-"
            if my_basket.quantity == 1:  # Если товар в корзине последний
                my_basket.delete()  # Удаляем товар из корзины
            else:  # Если не последний
                my_basket.quantity = my_basket.quantity - 1  # Уменьшаем количество на 1
                my_basket.save()  # Сохраняем объект
    else:  # Если такого товара в корзине нет
        Basket.objects.create(buyer=user, product=product, quantity=1)  # Добавляем объект в корзину
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Возвращаемся откуда пришли


def catalog(request, name_kind='все товары'):  # Функция для отображения каталога
    global per_page  # Объявляем глобальную переменную
    kinds = Kind.objects.all()  # Получаем все виды растений
    if name_kind != 'все товары':  # Если запрос на какой-то конкретный вид
        filtered_products = Product.objects.filter(kind__name_kind=name_kind)  # Выбираем товары этого вида
    else:  # Если нужны все товары
        filtered_products = Product.objects.all()  # Получаем все товары
    if request.method == 'POST':  # Если метод POST
        search_object = request.POST.get('search_object')  # Присваиваем значение из поисковой строки в переменную
        if search_object != None:  # Если что-то введено, выбираем товары в соответствии с запросом
            filtered_products = Product.objects.filter(Q(name_product__icontains=search_object) |
                                                       Q(specification_product__icontains=search_object))

        else:  # Если в поиск ничего не вводили, значит ввели количество товаров на странице
            per_page = request.POST.get('page_len')  # Присваиваем в переменную введенное количество товаров
    paginator = Paginator(filtered_products, per_page)  # создаем пагинатор
    page_number = request.GET.get('page', 1)  # получаем номер страницы, на которую переходит пользователь
    page_obj = paginator.get_page(page_number)  # получаем товары для текущей страницы
    context = {
        'page_obj': page_obj,
        'kinds': kinds,
        'name_kind': name_kind,
        'user': user
    }  # Передаем в контекст товары для текущей страницы, все виды товаров, наименование запрошенного вида и user-a
    return render(request, 'seeds/catalog.html', context)  # Переходим на страницу каталога


def basket_order(request):  # Функция для оформления заказа
    my_basket = Basket.objects.filter(buyer=user)  # выбираем из корзины товары этого user
    if request.method == 'POST':  # Если метод POST
        name_buyer = request.POST.get('name_buyer')  # Присваиваем переменным введенные значения
        address_buyer = request.POST.get('address_buyer')
        text_order = request.POST.get('text_order')
        list_product = []  # Создаем лист в котором будут храниться названия товаров, цена и количество
        amount_order = 0  # Для подсчета общей суммы заказа
        for paragraph in my_basket:  # Перебираем все товары в корзине
            # Добавляем кортежами в лист
            list_product.append((paragraph.product.name_product, paragraph.product.price, paragraph.quantity))
            amount_order = amount_order + paragraph.product.price * paragraph.quantity  # Считаем общую сумму
        # Создаем заказ
        order = Order.objects.create(author_order=user, name_buyer=name_buyer, address_buyer=address_buyer,
                        list_product=list_product, amount_order=amount_order, text_order=text_order)
        my_basket.delete()  # Очищаем корзину
        # Создаем сообщения об оформлении заказа
        post = f'{user}, ваш заказ успешно оформлен. Номер вашего заказа {order}'
        post_plus = ('В течение трех рабочих дней к вам на электронную почту будет отправлен счет, включающий пересылку,'
                    'который необходимо оплатить. После оплаты напишите нам письмо на email или в обратную '
                    'связь на сайте магазина. В письме укажите сумму и дату платежа. '
                    'При отсутствии оплаты в течении десяти дней с момента выставления счета заказ аннулируется.')
        context = {
            'post': post,
            'post_plus': post_plus,
            'user': user
        }  # Передаем в контекст
        return render(request, 'seeds/home.html', context)  # Переходим на главную страницу
    else:  # Если метод GET
        context = {
            'my_basket': my_basket,
            'user': user
        }  # Передаем содержимое корзины и user
        return render(request, 'seeds/basket_order.html', context)  # Переходим на страницу оформления заказа


def basket(request):  # Функция для просмотра содержимого корзины
    my_basket = Basket.objects.filter(buyer=user)  # Выбираем содержимое корзины по user
    amount_basket = 0  # Для подсчета общей стоимости
    for paragraph in my_basket:  # Перебираем все товары в корзине
        amount_basket += paragraph.product.price * paragraph.quantity  # Считаем общую стоимость
    context = {
        'amount_basket': amount_basket,
        'my_basket': my_basket,
        'user': user
    }  # Передаем в context стоимость корзины, содержимое и user
    return render(request, 'seeds/basket.html', context)  # Переходим на страницу корзины


def login_func(request):  # Функция для входа покупателя
    global user  # Объявляем глобальную переменную
    context = {
        'user': user,
        'error': '',
    }  # Сохраняем в context user и переменную для вывода ошибок
    if request.method == 'POST':  # Если метод POST
        login = request.POST.get('login')  # Сохраняем в переменные введенные значения
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        if password != password_again:  # Если пароль не совпадает с повтором пароля
            context['error'] = 'Пароли не совпадают'  # Записываем текст сообщения об ошибке
            return render(request, 'seeds/login.html', context)  # Возвращаемся
        if Buyer.objects.filter(login=login).exists():  # Проверяем есть ли покупатель с таким login
            buyer = Buyer.objects.get(login=login)  # Достаем покупателя с совпавшим login
            if buyer.password == password:  # Проверяем совпадают ли пароли
                user = buyer  # Меняем user на вошедшего покупателя
                post = f'{user}, рады приветствовать вас в нашем магазине.'  # Создаем сообщение о успешном входе
                context['post'] = post  # Передаем сообщение в контекст
                context['user'] = user
                return render(request, 'seeds/home.html', context)  # Переходим на главную страницу
            context['error'] = 'Неверный пароль'  # Создаем сообщение о шибке
            return render(request, 'seeds/login.html', context)  # Выходим обратно
        context['error'] = 'Пользователь с таким login не зарегистрирован'  # Создаем сообщение об ошибке
        return render(request, 'seeds/login.html', context)  # Выходим обратно
    return render(request, 'seeds/login.html', context)  # Переход на login.html


def registry(request):  # Функция для регистрации покупателя
    global user  # Объявляем глобальную переменную
    context = {
        'user': user,
        'error': '',
    }  # Сохраняем в context user и переменную для вывода ошибок
    if request.method == 'POST':  # Если метод POST
        login = request.POST.get('login')  # Сохраняем в переменные введенные значения
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        email = request.POST.get('email')
        if password != password_again:  # Если пароль с повтором не совпадают
            context['error'] = 'Пароли не совпадают'   # Создаем сообщение об ошибке
            return render(request, 'seeds/registry.html', context)  # Выходим обратно
        if Buyer.objects.filter(login=login).exists():  # Проверяем есть ли покупатель с таким login
            context['error'] = 'Пользователь с таким "login" уже существует'   # Создаем сообщение об ошибке
            return render(request, 'seeds/registry.html', context)  # Выходим обратно
        if Buyer.objects.filter(email=email).exists():  # Проверяем есть ли покупатель с таким email
            context['error'] = 'Пользователь с таким email уже существует'   # Создаем сообщение об ошибке
            return render(request, 'seeds/registry.html', context)  # Выходим обратно
        Buyer.objects.create(login=login, password=password, email=email)  # Регистрируем нового покупателя
        user = Buyer.objects.get(login=login)  # Меняем user на зарегистрированного покупателя
        # Создаем сообщение о успешной регистрации
        post = f'{user}, вы успешно зарегистрировались.\n Мы рады приветствовать вас в нашем магазине.'
        context['post'] = post  # Передаем сообщение в контекст
        context['user'] = user
        return render(request, 'seeds/home.html', context)  # Переходим на главную страницу
    return render(request, 'seeds/registry.html', context)  # Переходим на страницу регистрации


