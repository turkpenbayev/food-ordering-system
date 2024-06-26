# Проект "Система для заказа еды"

## Обзор

Данный проект представляет собой систему для заказа еды, разработанную с использованием следующих технологий, фреймворков и баз данных:

### Технологии и фреймворки:
- Django: веб-фреймворк на языке Python, используемый для создания веб-приложений.
- Django REST Framework (DRF): надстройка над Django для создания API-интерфейсов.
- Docker: платформа для разработки, доставки и запуска приложений в контейнерах.
- OpenAPI: спецификация для описания RESTful API.
- JWT (JSON Web Token): стандарт для создания токенов доступа.
- PostgreSQL: реляционная база данных с открытым исходным кодом.

## Архитектура

Архитектура проекта разработана с учетом требований масштабируемости, безопасности и эффективности. Вот как она отвечает этим требованиям:

### Масштабируемость
- Использование Docker обеспечивает удобное масштабирование приложения с помощью контейнеров.
- Использование Django и DRF позволяет легко добавлять новые функции и масштабировать API-интерфейсы.

### Безопасность
- Использование JWT для аутентификации и авторизации обеспечивает безопасность приложения путем генерации и проверки токенов доступа.
- Защита данных в PostgreSQL обеспечивается с помощью механизмов аутентификации и авторизации базы данных.

### Эффективность
- Использование Django и DRF позволяет эффективно создавать и обрабатывать запросы к API.
- PostgreSQL обеспечивает эффективное хранение и доступ к данным, что способствует быстрой работе приложения.

## Установка и запуск

### Шаг 1: Запуск Docker контейнеров
```bash
docker-compose up --build
```

### Шаг 2: Доступ к приложению
- После запуска контейнеров вы можете получить доступ к приложению [здесь](http://0.0.0.0:8000/docs/)

### Шаг 3: Доступ к администратору
```bash
Имя пользователя: admin
Пароль: admin
```
- страница админа [здесь](http://0.0.0.0:8000/admin/)
