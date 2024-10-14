from datetime import timedelta, datetime
from apscheduler.triggers.date import DateTrigger
import logging
from bot.data import user_data


class ReminderBot:
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler

    async def set_reminder(self, message, task, amount, unit):
        # Определяем правильный интервал времени
        delta = self._parse_time_unit(amount, unit)
        reminder_time = datetime.now() + delta

        logging.info(f"Устанавливаем напоминание на: {reminder_time}")
        await message.answer(f"Задача принята: '{task}'. Напомню через {amount} {unit}.")

        try:
            self.scheduler.add_job(
                self.send_reminder_async,
                DateTrigger(run_date=reminder_time),
                args=[message.chat.id, task],
                id=f"reminder_{message.chat.id}_{task}"
            )
            logging.info(f"Напоминание установлено на задачу: {task}, время: {reminder_time}")
        except Exception as e:
            logging.error(f"Ошибка при добавлении задачи в планировщик: {e}")

    async def send_reminder_async(self, chat_id, task):
        try:
            logging.info(f"Отправка напоминания. Задача: {task}, чат: {chat_id}")
            await self.bot.send_message(chat_id, f"Напоминание о задаче: '{task}'")
        except Exception as e:
            logging.error(f"Ошибка при отправке напоминания: {e}")

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
            return timedelta(minutes=amount)  # По умолчанию используем минуты
