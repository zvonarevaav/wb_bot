from datetime import timedelta, datetime
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
from bot.data import user_data


class ReminderBot:
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler
        self.reminders = {}  # Для хранения активных напоминаний

    async def set_reminder(self, message, task, amount, unit, repeat=False):
        # Определяем правильный интервал времени
        delta = self._parse_time_unit(amount, unit)
        reminder_time = datetime.now() + delta

        logging.info(f"Устанавливаем напоминание на: {reminder_time}")

        # Проверяем, если задача уже создана, чтобы избежать дублирования
        try:
            # Добавляем повторяющееся напоминание
            if repeat:
                trigger = IntervalTrigger(**{self._get_interval_key(unit): amount})
                self.scheduler.add_job(
                    self.send_reminder_async,
                    trigger,
                    args=[message.chat.id, task],
                    id=f"reminder_{message.chat.id}_{task}_repeat"
                )
                await message.answer(f"Задача '{task}' создана и будет повторяться каждые {amount} {self._format_unit(unit, amount)}.")
            else:
                # Добавляем одноразовое напоминание
                self.scheduler.add_job(
                    self.send_reminder_async,
                    DateTrigger(run_date=reminder_time),
                    args=[message.chat.id, task],
                    id=f"reminder_{message.chat.id}_{task}"
                )
                await message.answer(f"Задача '{task}' создана и напоминание установлено через {amount} {self._format_unit(unit, amount)}.")

            # Сохраняем напоминание в список активных
            self.reminders.setdefault(message.chat.id, []).append({
                "task": task,
                "time": amount,
                "unit": unit,
                "repeat": repeat
            })
            logging.info(f"Напоминание установлено на задачу: {task}, время: {reminder_time}")
        except Exception as e:
            logging.error(f"Ошибка при добавлении задачи в планировщик: {e}")

    async def send_reminder_async(self, chat_id, task):
        try:
            logging.info(f"Отправка напоминания. Задача: {task}, чат: {chat_id}")
            await self.bot.send_message(chat_id, f"Напоминание о задаче: '{task}'")
        except Exception as e:
            logging.error(f"Ошибка при отправке напоминания: {e}")

    def get_active_reminders(self, chat_id):
        """Возвращает все активные напоминания для данного чата."""
        return self.reminders.get(chat_id, [])

    def delete_reminder(self, chat_id, task):
        """Удаляет напоминание по имени задачи."""
        reminders = self.reminders.get(chat_id, [])
        if not reminders:
            return False

        # Находим напоминание по имени задачи
        for reminder in reminders:
            if reminder['task'] == task:
                reminders.remove(reminder)
                # Удаляем задачу из планировщика
                try:
                    self.scheduler.remove_job(f"reminder_{chat_id}_{task}")
                    self.scheduler.remove_job(f"reminder_{chat_id}_{task}_repeat")
                except Exception as e:
                    logging.error(f"Ошибка при удалении задачи: {e}")
                return True
        return False

    def _parse_time_unit(self, amount, unit):
        logging.info(f"Парсинг времени: {amount} {unit}")
        if unit == 'min':
            return timedelta(minutes=amount)
        elif unit == 'h':
            return timedelta(hours=amount)
        elif unit == 'd':
            return timedelta(days=amount)
        elif unit == 'w':
            return timedelta(weeks=amount)
        elif unit == 'mo':
            return timedelta(days=amount * 30)  # Условный месяц
        else:
            return timedelta(minutes=amount)

    def _get_interval_key(self, unit):
        """Возвращает ключ для IntervalTrigger в зависимости от единицы времени."""
        if unit == 'min':
            return 'minutes'
        elif unit == 'h':
            return 'hours'
        elif unit == 'd':
            return 'days'
        elif unit == 'w':
            return 'weeks'
        else:
            raise ValueError(f"Недопустимая единица времени: {unit}")

    def _format_unit(self, unit, amount):
        """Форматирует единицу времени для отображения в сообщении."""
        if unit == 'min':
            return 'минуту' if amount == 1 else 'минут'
        elif unit == 'h':
            return 'час' if amount == 1 else 'часов'
        elif unit == 'd':
            return 'день' if amount == 1 else 'дней'
        elif unit == 'w':
            return 'неделю' if amount == 1 else 'недель'
        elif unit == 'mo':
            return 'месяц' if amount == 1 else 'месяцев'
        else:
            return unit
