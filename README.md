<h1 align="center">Wildberries Bot </h1>

Это телеграм-бот, созданный для установки и управления напоминаниями. Бот помогает пользователям создавать задачи, устанавливать для них напоминания на основе временных интервалов (минуты, часы, дни, недели, месяцы) и просматривать активные задачи.

Функционал:
Создание напоминаний — Пользователь может создать задачу с указанием временного интервала.
Повторяющиеся задачи — Поддерживается создание повторяющихся задач.
Просмотр активных задач — Пользователь может просмотреть список всех активных напоминаний с помощью команды /view.

Технологии, использованные в боте:
Python — Основной язык программирования для создания бота.
Aiogram — Асинхронная библиотека для разработки Telegram ботов на Python.
PostgreSQL — База данных для хранения информации о пользователях и напоминаниях.
SQLAlchemy — ORM (Object-Relational Mapping) для взаимодействия с базой данных.
APScheduler — Планировщик задач для управления напоминаниями, их созданием и отправкой в нужное время.
Docker — Для контейнеризации приложения, что облегчает его развертывание и запуск на любых серверах.
dotenv — Для работы с переменными окружения через файл .env.

