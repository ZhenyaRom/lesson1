from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .forms import ContactForm
from .models import *


user = Buyer.objects.get(id=1)  # технический buyer пока не выполнен вход
per_page = 3  # стартовое количество товаров на странице


def home(request):
    """
    Домашняя страница (главная). Также на домашнюю страницу покупатель попадает после регистрации,
    смены пароля или оформления заказа.

    :param request:
    Создает два сообщения.
    :return: render(request, шаблон home.html в который передаются два сообщения и user(buyer)
    """
    post = ("Мы рады Вас видеть в нашем интернет-магазине семян! "
            "Мы продаем семена ведущих мировых и российских производителей!")
    post_plus = ("Ассортимент нашего Интернет-магазина постоянно пополняется. Если Вы желаете найти необходимый Вам "
                 "товар, то самый простой способ - воспользуйтесь нашим каталогом. Все товары разбиты на товарные группы"
                 "по которым можно отсортировать список товаров."
                 "Найти товар можно также при помощи поисковой системы.  Для этого необходимо набрать слово в форме "
                 "запроса и нажать на кнопку справа. Результатом Вашего поиска будет список товаров имеющих это слово "
                 "или словосочетание в описании или названии.")
    context = {
        'post': post,
        'post_plus': post_plus,
        'user': user
    }
    return render(request, 'seeds/home.html', context)  # Переход на главную страницу home.html


def contact_view(request):
    """
    Функция для обработки сообщений.

    :param request:
    :return: render(request, шаблон contact.html в который отправляет пустую форму запроса
    Если пользователем введены данные (name, email, message) сохраняет их в таблицу Post.
    Формирует сообщение об успешном получении сообщения.
    :return: render(request, шаблон home.html в который отправляет сообщение
    """
    context = {'user': user}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            Post.objects.create(name=name, email=email, message=message)
            post = f"Спасибо, {name}! Мы получили ваше сообщение."
            context['post'] = post
            return render(request, 'seeds/home.html', context)
    else:
        form = ContactForm()
        context['form'] = form
        return render(request, 'seeds/contact.html', context)


def cabinet(request, question=''):
    """
    Функция дла обработки запросов из личного кабинета.

    :param request: запрос пользователя
    :param question: может принимать значения '', 'my_order', 'new_password'
                          при question='' :return: cabinet.html;
                          при question='my_order' :return: шаблон cabinet.html и заказы собраные в filtered_order
                          при question='new_password' :return: шаблон cabinet.html и my_order=True
    Если введены данные для смены пароля,
            после проверки на ошибки
            :return: render(request, шаблон home.html в который отправляет сообщение об успешной смене пароля.
            Если обнаружены ошибки
            :return: render(request, шаблон cabinet.html и сообщение о ошибке.

    Если покупатель не вошел/зарегистрировался
    :return: render(request, шаблон home.html в который отправляется сообщение об ошибке.

    """
    context = {'user': user}
    if user == Buyer.objects.get(id=1):
        post = 'Чтобы попасть в личный кабинет нужно войти или зарегистрироваться'
        context['post'] = post
        return render(request, 'seeds/home.html', context)
    if request.method == 'POST':
        context['new_password_true'] = True
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        new_password_again = request.POST.get('new_password_again')
        if password == user.password:
            if new_password == new_password_again:
                user.password = new_password
                user.save()
                post = f'{user}, вы успешно поменяли пароль.'
                context['post'] = post
                return render(request, 'seeds/home.html', context)
            context['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/cabinet.html', context)
        context['error'] = 'Неверный пароль'
        return render(request, 'seeds/cabinet.html', context)
    else:
        if question == 'my_order':
            filtered_order = Order.objects.filter(author_order__id=user.id)
            context['filtered_order'] = filtered_order
            return render(request, 'seeds/cabinet.html', context)
        elif question == 'new_password':
            context['new_password_true'] = True
            return render(request, 'seeds/cabinet.html', context)
        else:
            return render(request, 'seeds/cabinet.html', context)


def add_basket(request, name_product, mark='+'):  # Функция для добавления товаров в корзину и изменения количества
    """
    Функция изменения количества товара в корзине


    :param request: запрос пользователя
    :param name_product: наименование продукта, который добавляется/изменяется
    :param mark: принимает значение '+' или '-'  (по умолчанию '+')
    В зависимости от mark увеличивает или уменьшает количество товара в корзине, также добавит товар если его не было.
    :return: render(request, возвращает на страницу с которой был направлен запрос.

    Если покупатель не вошел/зарегистрировался
    :return: render(request, шаблон home.html в который отправляется сообщение об ошибке.
    """
    if user == Buyer.objects.get(id=1):
        post = 'Чтобы совершать покупки нужно войти или зарегистрироваться'
        context = {'post': post}
        return render(request, 'seeds/home.html', context)
    product = Product.objects.get(name_product=name_product)
    if Basket.objects.filter(buyer=user, product=product).exists():
        my_basket = Basket.objects.get(buyer=user, product=product)
        if mark == '+':
            my_basket.quantity = my_basket.quantity + 1
            my_basket.save()
        else:
            if my_basket.quantity == 1:
                my_basket.delete()
            else:
                my_basket.quantity = my_basket.quantity - 1
                my_basket.save()
    else:
        Basket.objects.create(buyer=user, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def catalog(request, name_kind='все товары'):
    """
    Функция для отображения каталога

    :param request: запрос пользователя
    :param name_kind: название категории товара ( по умолчанию 'все товары')
    передает список товаров конкркетного вида или если был запрос на сортировку - товары удовлетворяющие запросу с
    разделением на страницы
    :return: render(request, шаблон catalog.html в который передаются
                                                      page_obj - список товаров с запрошенной страницы,
                                                      kinds - список всех видов растений,
                                                      name_kind - название запрошенного вида,
                                                      user - пользователь
    """
    global per_page
    kinds = Kind.objects.all()
    if name_kind != 'все товары':
        filtered_products = Product.objects.filter(kind__name_kind=name_kind)
    else:
        filtered_products = Product.objects.all()
    if request.method == 'POST':
        search_object = request.POST.get('search_object')
        if search_object != None:
            filtered_products = Product.objects.filter(Q(name_product__icontains=search_object) |
                                                       Q(specification_product__icontains=search_object))
        else:
            per_page = request.POST.get('page_len')
    paginator = Paginator(filtered_products, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'kinds': kinds,
        'name_kind': name_kind,
        'user': user
    }
    return render(request, 'seeds/catalog.html', context)


def basket_order(request):
    """
    Функция для оформления заказа.

    :param request:
    :return: render(request, шаблон basket_order.html в который передаются
                                                           my_basket - содержимое корзины покупателя,
                                                           user - покупатель.
    Если пользователем введены данные (name_buyer, address_buyer, text_order), сохраняется объект в таблицу Order.
    :return: render(request, шаблон home.html в который передаются сообщения о успешном оформлении заказа.
    """
    my_basket = Basket.objects.filter(buyer=user)
    if request.method == 'POST':
        name_buyer = request.POST.get('name_buyer')
        address_buyer = request.POST.get('address_buyer')
        text_order = request.POST.get('text_order')
        list_product = []
        amount_order = 0
        for paragraph in my_basket:
            list_product.append((paragraph.product.name_product, paragraph.product.price, paragraph.quantity))
            amount_order = amount_order + paragraph.product.price * paragraph.quantity
        order = Order.objects.create(author_order=user, name_buyer=name_buyer, address_buyer=address_buyer,
                        list_product=list_product, amount_order=amount_order, text_order=text_order)
        my_basket.delete()
        post = f'{user}, ваш заказ успешно оформлен. Номер вашего заказа {order}'
        post_plus = ('В течение трех рабочих дней к вам на электронную почту будет отправлен счет, включающий '
                     'пересылку, который необходимо оплатить. После оплаты напишите нам письмо на email или в обратную'
                     'связь на сайте магазина. В письме укажите сумму и дату платежа. '
                     'При отсутствии оплаты в течении десяти дней с момента выставления счета заказ аннулируется.')
        context = {
            'post': post,
            'post_plus': post_plus,
            'user': user
        }
        return render(request, 'seeds/home.html', context)
    else:
        context = {
            'my_basket': my_basket,
            'user': user
        }
        return render(request, 'seeds/basket_order.html', context)


def basket(request):
    """
    Функция для просмотра содержимого корзины покупателя.

    :param request:
    Функция считает общую стоимость товаров в корзине.
    :return: render(request, шаблон basket.html в который передается
                                                   amount_basket - стоимость товаров находящихся в корзине,
                                                   my_basket - товары находящиеся в корзине,
                                                   user - покупатель.)
    """
    my_basket = Basket.objects.filter(buyer=user)
    amount_basket = 0
    for paragraph in my_basket:
        amount_basket += paragraph.product.price * paragraph.quantity
    context = {
        'amount_basket': amount_basket,
        'my_basket': my_basket,
        'user': user
    }
    return render(request, 'seeds/basket.html', context)


def login_func(request):
    """
    Функция для входа покупателя.

    :param request:
    :return: render(request, шаблон login.html в который передается error=''
                                                                    user= пользователь)
    Если введены данные для входа (login, password, password_again) выполняются проверки, после проверок
           :return: render(request, шаблон home.html в который передается сообщение о успешном входе.
           если обнаружены ошибки
           :return: render(request, шаблон login.html в который передается error=сообщение об ошибке,
                                                                           user= пользователь)

    """
    global user
    context = {
        'user': user,
        'error': '',
    }
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        if password != password_again:
            context['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/login.html', context)
        if Buyer.objects.filter(login=login).exists():
            buyer = Buyer.objects.get(login=login)
            if buyer.password == password:
                user = buyer
                post = f'{user}, рады приветствовать вас в нашем магазине.'
                context['post'] = post
                context['user'] = user
                return render(request, 'seeds/home.html', context)
            context['error'] = 'Неверный пароль'
            return render(request, 'seeds/login.html', context)
        context['error'] = 'Пользователь с таким login не зарегистрирован'
        return render(request, 'seeds/login.html', context)
    return render(request, 'seeds/login.html', context)


def registry(request):
    """
    Функция для регистрации покупателя.

    :param request:
    :return: render(request, шаблон registry.html в который передается error=''
                                                                       user= пользователь)
    Если введены данные для входа (login, password, password_again, email, ) выполняются проверки, после проверок
    производится запись в таблицу Buyer.
           :return: render(request, шаблон home.html в который передается сообщение о успешной регистрации.
    если обнаружены ошибки
           :return: render(request, шаблон registry.html в который передается error=сообщение об ошибке,
                                                                              user= пользователь)

    """
    global user
    context = {
        'user': user,
        'error': '',
    }
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        email = request.POST.get('email')
        if password != password_again:
            context['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/registry.html', context)
        if Buyer.objects.filter(login=login).exists():
            context['error'] = 'Пользователь с таким "login" уже существует'
            return render(request, 'seeds/registry.html', context)
        if Buyer.objects.filter(email=email).exists():
            context['error'] = 'Пользователь с таким email уже существует'
            return render(request, 'seeds/registry.html', context)
        Buyer.objects.create(login=login, password=password, email=email)
        user = Buyer.objects.get(login=login)
        post = f'{user}, вы успешно зарегистрировались.\n Мы рады приветствовать вас в нашем магазине.'
        context['post'] = post
        context['user'] = user
        return render(request, 'seeds/home.html', context)
    return render(request, 'seeds/registry.html', context)


