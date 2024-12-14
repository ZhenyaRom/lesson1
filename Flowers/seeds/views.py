from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *

user = Buyer.objects.get(id=1)
per_page = 3


def welcome(request):
    context = {
        'user': user,
    }
    return render(request, 'welcome.html', context)


def catalog(request):
    global per_page
    # получаем все виды цветов
    kinds = Kind.objects.all() #.order_by('name_kind')  # и отсортируем по алфавиту
    if request.method == 'POST':



        per_page = request.POST.get('page_len')

    # создаем пагинатор
    paginator = Paginator(kinds, per_page)  # per_page постов на странице

    # получаем номер страницы, на которую переходит пользователь
    page_number = request.GET.get('page')

    # получаем посты для текущей страницы
    page_obj = paginator.get_page(page_number)

    # передаем контекст в шаблон
    return render(request, 'catalog.html', {'page_obj': page_obj})


def basket(request):
    context = {
        'title': 'tit',
        'user': user,
    }
    return render(request, 'basket.html', context)


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
            return render(request, 'login.html', info)
        x = False
        for buyer in buyers:
            if buyer.login == login:
                x = True
                if buyer.password == password:
                    user = buyer
                    info['user'] = user
                    return render(request, 'welcome.html', info)
        if x:
            info['error'] = 'Неверный пароль'
            return render(request, 'login.html', info)
        info['error'] = 'Пользователь с таким login не зарегистрирован'
        return render(request, 'login.html', info)
    return render(request, 'login.html')


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
            return render(request, 'registry.html', info)

        for buyer in buyers:
            if buyer.login == login:
                info['error'] = 'Пользователь с таким "login" уже существует'
                return render(request, 'registry.html', info)
            if buyer.email == email:
                info['error'] = 'Пользователь с таким email уже существует'
                return render(request, 'registry.html', info)
        Buyer.objects.create(login=login, password=password, email=email)
        user = Buyer.objects.get(login=login)
        info['user'] = user
        return render(request, 'welcome.html', info)
    return render(request, 'registry.html')


