# Тестовый проект Django Stripe API

![Django-app workflow](https://github.com/iricshkin/django-stripe-project/actions/workflows/djangostripe_workflows.yml/badge.svg)

Тестовый проект для обзора возможностей платёжной системой Stripe.com.

(4242 4242 4242 4242 - тестовая карта для проведения платежа),можно вводить люой CVC и сроком действия карты.

## Установка

Склонируйте репозиторий и настройте виртуальное окружение

```
сd project_directory
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

заполните `.env.example` в `.env`

Выполните команды из директории проекта

```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

## Запуск проекта через Docker

```
docker-compose up -d --build
```

При первом запуске для функционирования проекта выполните команды:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

## URL адреса

| _URL_       | _Метод_ | _Описание_                                                          |
| ----------- | ------- | ------------------------------------------------------------------- |
| `/buy/{id}` | `GET`   | создает Stripe Chekout Session для Item и возвращает **session_id** |

```
{"id": checkout_session.id}
```

| _URL_        | _Метод_ | _Описание_                                          |
| ------------ | ------- | --------------------------------------------------- |
| `/item/{id}` | `GET`   | возвращает страницу выбранного item c информацией и |
| кнопкой Buy  |

| _URL_             | _Метод_ | _Описание_                                                           |
| ----------------- | ------- | -------------------------------------------------------------------- |
| `/order-buy/{id}` | `GET`   | создает Stripe PaymentIndent для Order и возвращает **clientSecret** |

```
{"clientSecret": intent["client_secret"]}
```

| _URL_            | _Метод_ | _Описание_                                                                                                    |
| ---------------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| `api/order/{id}` | `GET`   | возвращает страницу c информацией о заказе order и форму для ввода email и кнопкой оплаты картой через Stripe |
