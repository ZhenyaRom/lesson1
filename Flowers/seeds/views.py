from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import View
from .forms import ContactForm
from .models import *


user = Buyer.objects.get(id=1)
per_page = 3
my_box = {}


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # Если форма валидна, обрабатываем данные
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Здесь можно отправить сообщение по email или сохранить в базу данных
            return render(request, 'seeds/contact_plus.html', {'name': name})
            #return HttpResponse(f"Спасибо, {name}! Мы получили ваше сообщение.")
    else:
        # GET-запрос, создаём пустую форму
        form = ContactForm()
        return render(request, 'seeds/contact.html', {'form': form})


def home(request):
    kinds = Kind.objects.all()
    return render(request, 'seeds/home.html', {'kinds': kinds})


def welcome(request):
    return render(request, 'seeds/welcome.html', {'user': user})


def add_basket(request, name_product):
    global my_box
    product = Product.objects.get(name_product=name_product)
    if product in my_box.keys():
        count = my_box.get(product)[0] + 1
        my_box[product] = [count, product.price, product.price * count]
    else:
        my_box[product] = [1, product.price, product.price]
    return redirect('home')


def catalog(request, name_kind):
    global per_page
    kinds = Kind.objects.all()
    if name_kind != 'all':
        filtered_products = Product.objects.filter(kind__name_kind=name_kind)
    else:
        filtered_products = Product.objects.all()
    if request.method == 'POST':
        per_page = request.POST.get('page_len')
    paginator = Paginator(filtered_products, per_page)  # создаем пагинатор
    page_number = request.GET.get('page')  # получаем номер страницы, на которую переходит пользователь
    page_obj = paginator.get_page(page_number)  # получаем товары для текущей страницы
    context = {
        'page_obj': page_obj,
        'kinds': kinds,
    }

    return render(request, 'seeds/catalog.html', context)


def basket_order(request):
    buyer0 = Buyer.objects.get(id=1)
    if user == buyer0:
        return redirect('basket')

    return render(request, 'seeds/basket_order.html')



def basket(request):
    global my_box
    list_my_box = []
    amount_order = 0

    for k, v in my_box.items():
        list_my_box.append(f'{k} -- {v[0]}шт.  --  {v[2]}руб.')
        amount_order += v[2]
    context = {
        'basket': list_my_box,
        'amount_order': amount_order,
    }
    return render(request, 'seeds/basket.html', context)



def login_func(request):
    global user
    info = {'error': ''}
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        buyers = Buyer.objects.all()
        if password != password_again:
            info['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/login.html', info)
        x = False
        for buyer in buyers:
            if buyer.login == login:
                x = True
                if buyer.password == password:
                    user = buyer
                    info['user'] = user
                    return redirect('home')
        if x:
            info['error'] = 'Неверный пароль'
            return render(request, 'seeds/login.html', info)
        info['error'] = 'Пользователь с таким login не зарегистрирован'
        return render(request, 'seeds/login.html', info)
    return render(request, 'seeds/login.html')


def registry(request):
    global user
    info = {'error': ''}
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        email = request.POST.get('email')
        buyers = Buyer.objects.all()
        if password != password_again:
            info['error'] = 'Пароли не совпадают'
            return render(request, 'seeds/registry.html', info)
        for buyer in buyers:
            if buyer.login == login:
                info['error'] = 'Пользователь с таким "login" уже существует'
                return render(request, 'seeds/registry.html', info)
            if buyer.email == email:
                info['error'] = 'Пользователь с таким email уже существует'
                return render(request, 'seeds/registry.html', info)
        Buyer.objects.create(login=login, password=password, email=email)
        user = Buyer.objects.get(login=login)
        info['user'] = user
        return redirect('home')
    return render(request, 'seeds/registry.html')


