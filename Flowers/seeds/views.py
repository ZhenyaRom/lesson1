from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from .forms import ContactForm, BuyerForm
from .models import *
from django.db.models import F, DecimalField, ExpressionWrapper

user = Buyer.objects.get(id=1)
per_page = 3



def contact_view(request):
    global user
    context = {'user': user}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # Если форма валидна, обрабатываем данные
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            Post.objects.create(name=name, email=email, message=message)
            post = f"Спасибо, {name}! Мы получили ваше сообщение."
            context['post'] = post
            return render(request, 'seeds/home.html', context)
    else:
        # GET-запрос, создаём пустую форму
        form = ContactForm()
        context['form'] = form
        return render(request, 'seeds/contact.html', context)


# def registry_view(request):
#     global user
#     info = {'error': ''}
#     if request.method == 'POST':
#         form = BuyerForm(request.POST)
#         if form.is_valid():
#             login = form.cleaned_data['login']
#             password = form.cleaned_data['password']
#             password_again = form.cleaned_data['password_again']
#             email = form.cleaned_data['email']
#             buyers = Buyer.objects.all()
#             if password != password_again:
#                 info['error'] = 'Пароли не совпадают'
#                 return render(request, 'seeds/success_order.html', info)
#             for buyer in buyers:
#                 if buyer.login == login:
#                     info['error'] = 'Пользователь с таким "login" уже существует'
#                     return render(request, 'seeds/success_order.html', info)
#                 if buyer.email == email:
#                     info['error'] = 'Пользователь с таким email уже существует'
#                     return render(request, 'seeds/success_order.html', info)
#             Buyer.objects.create(login=login, password=password, email=email)
#             user = Buyer.objects.get(login=login)
#             info['user'] = user
#             post = f'{user}, вы успешно зарегистрировались.\n Мы рады приветствовать вас в нашем магазине.'
#             return render(request, 'seeds/home.html', {'post': post})
#         #return redirect('home')
#     else:
#         forma = BuyerForm()
#         return render(request, 'seeds/success_order.html', {'forma': forma})


def home(request):
    global user
    post = ("Мы рады Вас видеть в нашем интернет-магазине семян! "
            "Мы продаем семена ведущих мировых и российских производителей!")
    post_plus = ("Ассортимент нашего Интернет-магазина постоянно пополняется. Если Вы желаете найти необходимый Вам товар, "
                 "то самый простой способ - воспользуйтесь нашим каталогом. Все товары разбиты на товарные группы по которым "
                 "можно отсортировать список товаров."
                 "Найти товар можно также при помощи поисковой системы.  Для этого необходимо набрать слово в форме запроса "
                 "и нажать на кнопку справа. Результатом Вашего поиска будет список товаров имеющих это слово или словосочетание "
                 "в описании или названии.")
    context = {
        'post': post,
        'post_plus': post_plus,
        'user': user
    }
    return render(request, 'seeds/home.html', context)


def cabinet(request, question=''):
    global user
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
        password_control = user.password
        if password == password_control:
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



def add_basket(request, name_product, mark = '+'):
    if user == Buyer.objects.get(id=1):
        post = 'Чтобы совершать покупки нужно войти или зарегистрироваться'
        context = {'post': post}
        return render(request, 'seeds/home.html', context)
    product = Product.objects.get(name_product=name_product)
    if Basket.objects.filter(buyer=user, product=product).exists():
        my_basket = Basket.objects.get(buyer=user, product=product)
        quantity = my_basket.quantity
        if mark == '+':
            my_basket.quantity = quantity + 1
            my_basket.save()
        else:
            if quantity == 1:
                my_basket.delete()
            else:
                my_basket.quantity = quantity - 1
                my_basket.save()
    else:
        Basket.objects.create(buyer=user, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def catalog(request, name_kind='все товары'):
    global user
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
    paginator = Paginator(filtered_products, per_page)  # создаем пагинатор
    page_number = request.GET.get('page', 1)  # получаем номер страницы, на которую переходит пользователь
    page_obj = paginator.get_page(page_number)  # получаем товары для текущей страницы
    context = {
        'page_obj': page_obj,
        'kinds': kinds,
        'name_kind': name_kind,
        'user': user
    }
    return render(request, 'seeds/catalog.html', context)


def basket_order(request):
    my_basket = Basket.objects.filter(buyer=user)
    if my_basket:
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
            post = f'{user}, ваш заказ успешно оформлен.\n Номер вашего заказа {order}'
            post_plus = ('В течение трех рабочих дней к вам на электронную почту будет отправлен счет, '
                     'который необходимо оплатить. После оплаты напишите нам письмо на email или в обратную '
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
    else:
        error = 'Нельзя оформить заказ с пустой корзиной'
        context = {
            'error': error,
            'user': user
        }
        return render(request, 'seeds/home.html', context)
def basket(request):
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


# def basket(request):
#     global user
#     global my_box
#     list_my_box = []
#     amount_order = 0
#
#     for k, v in my_box.items():
#         list_my_box.append(f'{k} -- {v[0]}шт.  --  {v[1]}руб.')
#         amount_order += v[1]
#     context = {
#         'basket': list_my_box,
#         'amount_order': amount_order,
#         'user': user
#     }
#     return render(request, 'seeds/basket.html', context)


def login_func(request):
    global user
    context = {
        'user': user,
        'error': '',
    }
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        buyers = Buyer.objects.all()
        if password != password_again:
            context['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/login.html', context)
        x = False
        for buyer in buyers:
            if buyer.login == login:
                x = True
                if buyer.password == password:
                    user = buyer
                    post = f'{user}, рады приветствовать вас в нашем магазине.'
                    context['post'] = post
                    context['user'] = user
                    return render(request, 'seeds/home.html', context)
        if x:
            context['error'] = 'Неверный пароль'
            return render(request, 'seeds/login.html', context)
        context['error'] = 'Пользователь с таким login не зарегистрирован'
        return render(request, 'seeds/login.html', context)
    return render(request, 'seeds/login.html', context)


def registry(request):
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
        buyers = Buyer.objects.all()
        if password != password_again:
            context['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/registry.html', context)
        for buyer in buyers:
            if buyer.login == login:
                context['error'] = 'Пользователь с таким "login" уже существует'
                return render(request, 'seeds/registry.html', context)
            if buyer.email == email:
                context['error'] = 'Пользователь с таким email уже существует'
                return render(request, 'seeds/registry.html', context)
        Buyer.objects.create(login=login, password=password, email=email)
        user = Buyer.objects.get(login=login)
        post = f'{user}, вы успешно зарегистрировались.\n Мы рады приветствовать вас в нашем магазине.'
        context['post'] = post
        context['user'] = user
        return render(request, 'seeds/home.html', context)
        #return redirect('home')
    return render(request, 'seeds/registry.html', context)


