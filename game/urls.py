"""
URL-адреса для приложения "game"
Курсовая работа: "Мудрость предков" - квест по тувинским пословицам
Студент: [ТВОЁ ФИО]
Группа: [ТВОЯ ГРУППА]

Описание:
Данный модуль содержит маршрутизацию для игровых страниц:
- Главная страница
- Начало игры
- Игровой процесс
- Проверка ответа (AJAX)
- Переход к следующему вопросу
- Завершение игры
- Таблица лидеров
"""

from django.urls import path
from . import views

# Имя приложения для обратных ссылок в шаблонах
app_name = 'game'

# Список URL-паттернов приложения game
urlpatterns = [
    # Главная страница сайта
    path('', views.home, name='home'),
    
    # Начало новой игры (создание 10 сессий)
    path('game/start/', views.start_game, name='start_game'),
    
    # Игровой процесс (отображение пословицы)
    # <int:session_id> - динамический параметр (ID сессии)
    path('game/play/<int:session_id>/', views.play_game, name='play_game'),
    
    # Проверка ответа (AJAX запрос)
    path('game/check/', views.check_answer, name='check_answer'),
    
    # Переход к следующему вопросу
    path('game/play/<int:session_id>/next/', views.next_question, name='next_question'),
    
    # Завершение игры и показ результатов
    path('game/finish/', views.finish_game, name='finish_game'),
    
    # Таблица лидеров (рейтинг игроков)
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]