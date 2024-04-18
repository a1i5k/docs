from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import classes
import sqlite3
from enum import Enum
from django.shortcuts import redirect

Special = ['Здоровый', 'Больной']


def connect_db():
    return sqlite3.connect('server.db')


def check_type_account(request, login, cursor):
    res = classes.GetTypeAccount(login, cursor).run()
    if res == 0:
        return render(request, 'main_user.html')
    elif res == 1:
        return render(request, 'main_nutritionist.html')
    else:
        return render(request, 'main_user.html')


def main(request):
    if request.session['login'] != '':
        connect = connect_db()
        cursor = connect.cursor()
        return check_type_account(request, request.session['login'], cursor)
    return redirect('http://127.0.0.1:8000/auth')


def find_diet(request):
    connect = connect_db()
    cursor = connect.cursor()
    login = request.session['login']
    diet_name, dishes = classes.FindDiet(login, cursor).run()
    if diet_name is False:
        context = {'diet': 'Не найдена', 'dishes': dishes, 'found_diet': False, 'found_dish': False}
    elif len(dishes) > 0:
        context = {'diet': diet_name, 'dishes': dishes, 'found_diet': True, 'found_dish': True}
    else:
        context = {'diet': diet_name, 'dishes': dishes, 'found_diet': True, 'found_dish': False}
    connect.commit()
    return render(request, 'find_diet.html', context)


def auth(request):
    context = {'message': ''}
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        login = request.POST.get('login')
        password = request.POST.get('password')
        if classes.Authorization(login, password, cursor).run():
            request.session['login'] = login
            return redirect('http://127.0.0.1:8000/')
        else:
            context = {'message': 'Неверный логин или пароль'}
            return render(request, 'auth.html', context)
    return render(request, 'auth.html', context)


def add_diet(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        name = request.POST.get('name')
        description = request.POST.get('description')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        special = request.POST.get('special')
        classes.AddDiet(name, description, age, height, weight, special, cursor).run()
        connect.commit()
        return redirect('http://127.0.0.1:8000/')
    context = {'specials': Special}
    return render(request, 'add_diet.html', context)


def add_dish(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        name = request.POST.get('name')
        diet = request.POST.get('diet')
        classes.AddDish(name, diet, cursor).run()
        connect.commit()
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'add_dish.html')


def get_history_diet(request):
    connect = connect_db()
    cursor = connect.cursor()
    login = request.session['login']
    diet, dishes = classes.GetHistoryDiet(login, cursor).run()
    context = {'history': diet, 'dishes': dishes}
    return render(request, 'get_history_diet.html', context)


def update_password(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        login = request.POST.get('login')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        classes.RestorePassword(login, phone, password, cursor).run()
        connect.commit()
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'update_password.html')


def registration(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        login = request.POST.get('login')
        request.session['login'] = login
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        phone = request.POST.get('phone')
        type_account = request.POST.get('type')
        if type_account == 'on':
            type_account = 1
        else:
            type_account = 0
        classes.Registration(login, password, mail, phone, type_account, cursor).run()
        connect.commit()
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'registration.html')


def fill_about_me(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        login = request.session['login']
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        special = request.POST.get('special')
        classes.FillAboutMe(age, height, weight, special, login, cursor).run()
        connect.commit()
        return redirect('http://127.0.0.1:8000/')
    context = {'specials': Special}
    return render(request, 'fill_about_me.html', context)


def update_diet(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        old_name = request.POST.get('old_name')
        name = request.POST.get('name')
        description = request.POST.get('description')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        special = request.POST.get('special')
        classes.UpdateDiet(old_name, name, description, age, height, weight, special, cursor).run()
        connect.commit()
        return render(request, 'main_user.html')
    context = {'specials': Special}
    return render(request, 'update_diet.html', context)


def update_dish(request):
    if request.method == 'POST':
        connect = connect_db()
        cursor = connect.cursor()
        old_name = request.POST.get('old_name')
        name = request.POST.get('name')
        classes.UpdateDish(old_name, name, cursor).run()
        connect.commit()
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'update_dish.html')


def unauth(request):
    request.session['login'] = ''
    return redirect('http://127.0.0.1:8000/auth')
