
"""
Админ-панель для приложения "game"
Курсовая работа: "Мудрость предков" - квест по тувинским пословицам
Студент: [ТВОЁ ФИО]
Группа: [ТВОЯ ГРУППА]

Описание:
Данный модуль регистрирует модели в админ-панели Django
для удобного управления пословицами и просмотра статистики игр.
"""

from django.contrib import admin
from .models import Proverb, GameSession, GameResult


@admin.register(Proverb)
class ProverbAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Proverb в админ-панели
    
    Показывает список всех пословиц с возможностью:
    - Поиска по тексту и правильному ответу
    - Фильтрации по дате создания
    - Добавления/редактирования пословиц
    """
    # Поля, отображаемые в списке
    list_display = ['text', 'missing_word', 'created_at']
    
    # Поля для поиска
    search_fields = ['text', 'missing_word', 'hint']
    
    # Поля для фильтрации
    list_filter = ['created_at']
    
    # Количество записей на странице
    list_per_page = 20


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели GameSession в админ-панели
    
    Показывает все игровые сессии с информацией о:
    - Пользователе
    - Пословице
    - Количестве попыток
    - Результате (угадано/не угадано)
    """
    list_display = ['user', 'proverb', 'attempts', 'is_correct', 'completed_at']
    list_filter = ['is_correct', 'completed_at']
    search_fields = ['user__username', 'proverb__text']


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели GameResult в админ-панели
    
    Показывает aggregated статистику игроков для лидерборда.
    """
    list_display = ['user', 'wins', 'total_games', 'total_attempts', 'best_score', 'last_played']
    list_filter = ['last_played']
    search_fields = ['user__username']