"""
Представления (Views) для приложения "accounts"
Курсовая работа: "Мудрость предков" - квест по тувинским пословицам
Студент: Хомушку Алдынай Анатольевна
Группа: ФИТ_304

Описание:
Данный модуль содержит функции-представления для обработки HTTP-запросов,
связанных с регистрацией, входом и выходом пользователей.

Функции:
- register_view: Регистрация нового пользователя
- login_view: Вход существующего пользователя
- logout_view: Выход из системы
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    """
    Регистрация нового пользователя
    
    Описание:
    Обрабатывает форму регистрации нового пользователя.
    Если пользователь уже авторизован, перенаправляет на главную.
    
    Логика:
    1. Проверяем, не авторизован ли уже пользователь
    2. Если POST-запрос - обрабатываем форму регистрации
    3. Если форма валидна - создаём пользователя и автоматически входим
    4. Если GET-запрос - показываем пустую форму
    
    Аргументы:
    - request: HTTP-запрос от клиента
    
    Возвращает:
    - render: HTML-шаблон страницы регистрации
    - redirect: Перенаправление на главную после успешной регистрации
    """
    # Если пользователь уже вошёл, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('game:home')
    
    # Обрабатываем POST-запрос (отправка формы)
    if request.method == 'POST':
        # Создаём форму с данными из запроса
        form = UserCreationForm(request.POST)
        
        # Проверяем валидность формы
        if form.is_valid():
            # Сохраняем нового пользователя в базу данных
            user = form.save()
            
            # Автоматически авторизуем пользователя после регистрации
            login(request, user)
            
            # Добавляем сообщение об успехе
            messages.success(request, 'Регистрация успешна! Добро пожаловать! 🎉')
            
            # Перенаправляем на главную страницу
            return redirect('game:home')
    else:
        # GET-запрос - создаём пустую форму
        form = UserCreationForm()
    
    # Контекст для передачи в шаблон
    context = {
        'form': form  # Форма регистрации
    }
    
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """
    Вход существующего пользователя
    
    Описание:
    Обрабатывает форму входа пользователя в систему.
    Проверяет логин и пароль, создаёт сессию.
    
    Логика:
    1. Проверяем, не авторизован ли уже пользователь
    2. Если POST-запрос - получаем логин и пароль
    3. Проверяем учётные данные через authenticate()
    4. Если успешно - создаём сессию через login()
    5. Если ошибка - показываем сообщение
    
    Аргументы:
    - request: HTTP-запрос от клиента
    
    Возвращает:
    - render: HTML-шаблон страницы входа
    - redirect: Перенаправление на главную после успешного входа
    """
    # Если пользователь уже вошёл, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('game:home')
    
    # Обрабатываем POST-запрос (отправка формы)
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Проверяем учётные данные
        # authenticate() возвращает объект User или None
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Учётные данные верны - создаём сессию
            login(request, user)
            
            # Добавляем сообщение об успехе
            messages.success(request, f'С возвращением, {user.username}! 👋')
            
            # Перенаправляем на главную страницу
            return redirect('game:home')
        else:
            # Учётные данные неверны
            messages.error(request, 'Неверный логин или пароль. Попробуйте ещё раз. ❌')
    
    # GET-запрос или ошибка - показываем форму входа
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    Выход пользователя из системы
    
    Описание:
    Завершает сессию пользователя и перенаправляет на страницу входа.
    Требуется авторизация (декоратор @login_required).
    
    Логика:
    1. Вызываем logout() для завершения сессии
    2. Добавляем информационное сообщение
    3. Перенаправляем на страницу входа
    
    Аргументы:
    - request: HTTP-запрос от клиента (требуется авторизация)
    
    Возвращает:
    - redirect: Перенаправление на страницу входа
    """
    # Завершаем сессию пользователя
    logout(request)
    
    # Добавляем информационное сообщение
    messages.info(request, 'Вы успешно вышли из системы. До встречи! 👋')
    
    # Перенаправляем на страницу входа
    return redirect('accounts:login')