from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Кнопка для создания напоминания
def create_reminder_button():
    reminder_button = InlineKeyboardButton(text="📝 Создать напоминание", callback_data="create_reminder")


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [reminder_button]
        # Убираем строку с кнопкой для просмотра активных задач
        # [active_tasks_button]
    ])
    return keyboard


# Кнопки для выбора единицы времени
def create_time_unit_buttons():
    min_button = InlineKeyboardButton(text="⏱ Минуты", callback_data="min")
    hour_button = InlineKeyboardButton(text="🕒 Часы", callback_data="h")
    day_button = InlineKeyboardButton(text="📅 Дни", callback_data="d")
    week_button = InlineKeyboardButton(text="📆 Недели", callback_data="w")
    month_button = InlineKeyboardButton(text="🗓 Месяц", callback_data="mo")  # Кнопка "Месяц"
    repeat_button = InlineKeyboardButton(text="🔄 Повторять",
                                         callback_data="repeat")  # Кнопка для повторяющегося напоминания

    # Создаем inline-клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [min_button, hour_button],  # первая строка с двумя кнопками
        [day_button, week_button],  # вторая строка с двумя кнопками
        [month_button],  # третья строка с кнопкой "Месяц"
        [repeat_button]  # строка с кнопкой "Повторять"
    ])
    return keyboard



