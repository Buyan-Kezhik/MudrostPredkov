"""
Представления (Views) для приложения "game"
Курсовая работа: "Мудрость предков" - квест по тувинским пословицам
Студент: Хомушку Алдынай Анатольевна
Группа: ФИТ_304

Описание:
Данный модуль содержит функции-представления для обработки HTTP-запросов
и реализации логики игры с тувинскими пословицами.

Функции:
- home: Главная страница сайта
- start_game: Начало новой игры
- play_game: Игровой процесс (отображение пословицы)
- check_answer: Проверка ответа пользователя
- next_question: Переход к следующему вопросу
- finish_game: Завершение игры и показ результатов
- leaderboard: Таблица лидеров
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.utils import timezone
import random
from .models import Proverb, GameSession, GameResult


def home(request):
    """
    Главная страница сайта
    
    Описание:
    Отображает приветственную страницу с информацией об игре.
    Если пользователь авторизован - показывает кнопку начала игры.
    Если нет - предлагает зарегистрироваться или войти.
    
    Аргументы:
    - request: HTTP-запрос от клиента
    
    Возвращает:
    - render: HTML-шаблон главной страницы
    """
    return render(request, 'game/home.html')


@login_required
def start_game(request):
    # 1. УДАЛЯЕМ старые сессии этого пользователя, чтобы начать с чистого листа
    GameSession.objects.filter(user=request.user).delete() 
    
    # 2. Получаем пословицы
    all_proverbs = list(Proverb.objects.all())
    if len(all_proverbs) == 0:
        return redirect('game:home')
        
    random.shuffle(all_proverbs)
    game_proverbs = all_proverbs[:10]
    
    session_ids = []
    for proverb in game_proverbs:
        session = GameSession.objects.create(
            user=request.user,
            proverb=proverb,
            attempts=0,
            is_correct=False
        )
        session_ids.append(session.id)
        
    return redirect('game:play_game', session_id=session_ids[0])


@login_required
def play_game(request, session_id):
    """
    Отображение текущего вопроса игры
    
    Описание:
    Показывает пользователю пословицу с пропущенным словом
    и поле для ввода ответа.
    
    Логика:
    1. Получаем игровую сессию по ID
    2. Проверяем, принадлежит ли сессия текущему пользователю
    3. Определяем номер текущего вопроса
    4. Передаём данные в шаблон
    
    Аргументы:
    - request: HTTP-запрос (требуется авторизация)
    - session_id: ID текущей игровой сессии
    
    Возвращает:
    - render: HTML-шаблон игрового процесса
    """
    # Получаем сессию или возвращаем ошибку 404
    session = get_object_or_404(GameSession, id=session_id, user=request.user)
    
    # Получаем все сессии текущего пользователя, отсортированные по времени
    user_sessions = list(GameSession.objects.filter(
        user=request.user
    ).order_by('completed_at'))
    
    # Находим индекс текущей сессии в списке
    current_index = next(
        (i for i, s in enumerate(user_sessions) if s.id == session_id),
        None
    )
    
    # Если сессия не найдена, перенаправляем на главную
    if current_index is None:
        return redirect('game:home')
    
    # Вычисляем номер текущего вопроса
    total_questions = len(user_sessions)
    current_number = current_index + 1
    
    # Контекст для передачи в шаблон
    context = {
        'session': session,           # Текущая сессия
        'proverb': session.proverb,   # Пословица
        'attempts': session.attempts, # Количество попыток
        'current_number': current_number,  # Номер вопроса
        'total_questions': total_questions,  # Всего вопросов
    }
    
    return render(request, 'game/play.html', context)


@login_required
def check_answer(request):
    """
    Проверка ответа пользователя (AJAX запрос)
    
    Описание:
    Принимает ответ пользователя, сравнивает с правильным словом
    и возвращает результат в формате JSON.
    
    Логика:
    1. Получаем session_id и ответ из POST-запроса
    2. Увеличиваем счётчик попыток
    3. Сравниваем ответ с правильным словом (без учёта регистра)
    4. Если правильно - помечаем сессию как завершённую успешно
    5. Если 3 попытки исчерпаны - помечаем как неудачную
    6. Обновляем статистику игрока
    
    Аргументы:
    - request: HTTP POST-запрос с данными ответа
    
    Возвращает:
    - JsonResponse: Результат проверки в формате JSON
    """
    # Обрабатываем только POST-запросы
    if request.method == 'POST':
        # Получаем данные из запроса
        session_id = request.POST.get('session_id')
        user_answer = request.POST.get('answer', '').strip().lower()
        
        # Получаем сессию
        session = get_object_or_404(GameSession, id=session_id, user=request.user)
        
        # Увеличиваем счётчик попыток
        session.attempts += 1
        
        # Получаем правильное слово и приводим к нижнему регистру
        correct_word = session.proverb.missing_word.strip().lower()
        
        # Сравниваем ответ с правильным словом
        if user_answer == correct_word:
            # Правильный ответ!
            session.is_correct = True
            session.save()
            
            # Обновляем статистику игрока в лидерборде
            update_game_result(request.user, is_correct=True, attempts=session.attempts)
            
            return JsonResponse({
                'correct': True,
                'message': 'Правильно! Молодец! 🎉',
                'attempts': session.attempts,
                'success': True
            })
        else:
            # Неправильный ответ
            session.save()
            
            # Проверяем, не исчерпаны ли попытки
            if session.attempts >= 3:
                # Попытки закончились
                session.is_correct = False
                session.save()
                update_game_result(request.user, is_correct=False, attempts=session.attempts)
                
                return JsonResponse({
                    'correct': False,
                    'message': f'Неправильно. Правильный ответ: {session.proverb.missing_word}',
                    'attempts': session.attempts,
                    'max_attempts': True,
                    'success': True
                })
            
            # Ещё есть попытки
            remaining = 3 - session.attempts
            return JsonResponse({
                'correct': False,
                'message': f'Неправильно. Осталось попыток: {remaining}',
                'attempts': session.attempts,
                'success': True
            })
    
    # Если не POST-запрос, возвращаем ошибку
    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_game_result(user, is_correct, attempts):
    """
    Обновление статистики игрока для таблицы лидеров
    
    Описание:
    Создаёт или обновляет запись GameResult для пользователя.
    Подсчитывает общее количество игр, побед и попыток.
    
    Аргументы:
    - user: Объект пользователя Django
    - is_correct: Boolean, правильный ли был ответ
    - attempts: Количество попыток в текущей игре
    """
    # Получаем или создаём запись результата
    result, created = GameResult.objects.get_or_create(user=user)
    
    # Увеличиваем счётчик игр
    result.total_games += 1
    
    # Если ответ правильный, увеличиваем счётчик побед
    if is_correct:
        result.wins += 1
        
        # Обновляем лучший счёт (меньше попыток = лучше)
        if result.best_score == 0 or attempts < result.best_score:
            result.best_score = attempts
    
    # Добавляем попытки к общему счётчику
    result.total_attempts += attempts
    
    # Сохраняем изменения
    result.save()


@login_required
def next_question(request, session_id):
    """
    Переход к следующему вопросу
    
    Описание:
    После ответа на текущий вопрос перенаправляет на следующий.
    Если это был последний вопрос - перенаправляет на страницу результатов.
    
    Аргументы:
    - request: HTTP-запрос (требуется авторизация)
    - session_id: ID текущей сессии
    
    Возвращает:
    - redirect: На следующий вопрос или на страницу результатов
    """
    # Получаем все сессии пользователя
    user_sessions = list(GameSession.objects.filter(
        user=request.user
    ).order_by('completed_at'))
    
    # Находим индекс текущей сессии
    current_index = next(
        (i for i, s in enumerate(user_sessions) if s.id == session_id),
        None
    )
    
    if current_index is None:
        return redirect('game:home')
    
    # Проверяем, есть ли следующий вопрос
    if current_index >= len(user_sessions) - 1:
        # Это последний вопрос, переходим к результатам
        return redirect('game:finish_game')
    
    # Переходим к следующему вопросу
    next_session = user_sessions[current_index + 1]
    return redirect('game:play_game', session_id=next_session.id)


@login_required
def finish_game(request):
    """
    Завершение игры и отображение результатов
    
    Описание:
    Показывает пользователю итоги игры:
    - Количество правильных ответов
    - Процент точности
    - Общую статистику
    
    Аргументы:
    - request: HTTP-запрос (требуется авторизация)
    
    Возвращает:
    - render: HTML-шаблон с результатами
    """
    # Получаем все сессии текущей игры
    sessions = GameSession.objects.filter(user=request.user)
    
    # Подсчитываем правильные ответы
    correct_count = sessions.filter(is_correct=True).count()
    total_count = sessions.count()
    
    # Вычисляем процент правильных ответов
    if total_count > 0:
        percentage = (correct_count / total_count) * 100
    else:
        percentage = 0
    
    # Контекст для шаблона
    context = {
        'correct': correct_count,      # Правильных ответов
        'total': total_count,          # Всего вопросов
        'percentage': percentage,      # Процент точности
    }
    
    return render(request, 'game/finish.html', context)


def leaderboard(request):
    """
    Таблица лидеров (рейтинг игроков)
    
    Описание:
    Отображает топ-10 игроков по количеству побед.
    Доступна всем пользователям (не требует авторизации).
    
    Сортировка:
    1. По количеству побед (убывание)
    2. По количеству попыток (возрастание - меньше лучше)
    
    Аргументы:
    - request: HTTP-запрос
    
    Возвращает:
    - render: HTML-шаблон с таблицей лидеров
    """
    # Получаем топ-10 игроков
    leaders = GameResult.objects.select_related('user').order_by(
        '-wins',           # Сначала по победам (убывание)
        'total_attempts'   # Затем по попыткам (возрастание)
    )[:10]
    
    # Контекст для шаблона
    context = {
        'leaders': leaders,  # Список лидеров
    }
    
    return render(request, 'game/leaderboard.html', context)