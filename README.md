# Учебный проект: Foodgram - продуктовый помощник
### Описание:
Foodgram это веб сервис, с помощью которого, пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список(в формате .txt) продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Вот, что было сделано в ходе работы над проектом:
* настроено взаимодействие Python-приложения с внешними API-сервисами;
* создан собственный API-сервис на базе проекта Django;
* создан Telegram-бот;
* подключено SPA к бэкенду на Django через API;
* созданы образы и запущены контейнеры Docker;
* созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;
* закреплены на практике основы DevOps, включая CI&CD.
### Используемые технологии:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

### Как запустить на удаленном сервере:
Клонировать репозиторий:
```
git clone git@github.com:Epikhin/foodgram-project-react.git
```
Установить на сервере Docker, Docker Compose:
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```
Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

POSTGRES_USER           # django_user
POSTGRES_PASSWORD       # mysecretpassword
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```
Создать и запустить контейнеры Docker, выполнить команду на сервере:
```
sudo docker compose up -d
```
Выполнить миграции:
```
sudo docker compose exec backend python manage.py makemigrations
sudo docker compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```
Скопировать статику:
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/
```
Наполнить базу данных ингредиентами и тэгами:
```
sudo docker compose exec backend python manage.py import_ingredients
sudo docker compose exec backend python manage.py add_tags
```
Для админ-зоны:
Логин: ```admin``` Пароль: ```a```
### Автор backend'a
Епихин Александр (о)_(о)

