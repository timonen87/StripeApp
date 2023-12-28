# Тестовый проект Django Stripe API

![Django-app workflow](https://github.com/iricshkin/django-stripe-project/actions/workflows/djangostripe_workflows.yml/badge.svg)

Проект создан с целью ознакомиться с платёжной системой Stripe.com. Она имеет подробный API и бесплатный тестовый режим для имитации
и тестирования платежей. С помощью python библиотеки stripe можно удобно создавать платежные формы разных видов, сохранять данные
клиента, и реализовывать прочие платежные функции.
Существует несколько [тестовых карт](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=checkout&integration=checkout#additional-testing-resources)
(4242 4242 4242 4242 - для проведения успешного платежа),
которые вы можете использовать, чтобы проверить работу приложения. Используйте их с любым CVC и сроком действия карты.

## Реализованные задачи

- Django Модели Item, Order, Discount, Tax
- Просмотр Django Моделей через Django Admin панели
- Использование environment variables
- Запуск, используя Docker
- Stripe Payment Intent
- Поле Item.currency

## Установка

Склонируйте репозиторий. Находясь в папке с кодом создайте виртуальное окружение `python -m venv venv`, активируйте его (Windows: `source venv\scripts\activate`; Linux/Mac: `source venv/bin/activate`), установите зависимости `python -m pip install -r requirements.txt`.
Переименуйте `.env.example` в `.env` и заполните его.

Для запуска сервера разработки, находясь в директории проекта выполните команды:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

## Запуск проекта

Перейдите в папку проекта и выполните команду:

```
docker-compose up -d --build
```

При первом запуске для функционирования проекта выполните команды:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

## Деплой на удаленный сервер

Необходимо создать переменные окружения в вашем репозитории github в разделе `secrets`

```
DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USERNAME # Логин от Docker Hub

HOST # Публичный ip адрес сервера
USER # Пользователь сервера
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ

STRIPE_PUBLISHABLE_KEY # Ваш Publishable key с сайта stripe.com
STRIPE_SECRET_KEY # Ваш Secret key с сайта stripe.com
```

При каждом обновлении репозитория (git push) будет происходить:

- проверка кода соответствие страндарту PEP8 (с помощью пакета flake8)
- сборка и обновление образа на сервисе Docker Hub
- отправка уведомления в Telegram

## URL адреса

| _URL_       | _Метод_ | _Описание_                                                          |
| ----------- | ------- | ------------------------------------------------------------------- |
| `/buy/{id}` | `GET`   | создает Stripe Chekout Session для Item и возвращает **session_id** |

```
{"client_secret": "some_secret_key"}
```

| _URL_        | _Метод_ | _Описание_                                                                 |
| ------------ | ------- | -------------------------------------------------------------------------- |
| `/item/{id}` | `GET`   | возвращает страницу выбранного item и форму для оплаты картой через Stripe |

Success Response:

- Code: 200
- Content:Checkout page

| _URL_             | _Метод_ | _Описание_                                                          |
| ----------------- | ------- | ------------------------------------------------------------------- |
| `/order-buy/{id}` | `GET`   | создает Stripe PaymentIndent для Order и возвращает **user_secret** |

Success Response:

- Code: 200
- Content:

```
{"client_secret": "some_secret_key"}
```

| _URL_            | _Метод_ | _Описание_                                                                  |
| ---------------- | ------- | --------------------------------------------------------------------------- |
| `api/order/{id}` | `GET`   | возвращает страницу выбранного order и форму для оплаты картой через Stripe |

Success Response:

- Code: 200
- Content:Checkout page

## Об авторе

Ирина Фок [iricshkin](https://github.com/iricshkin/)
