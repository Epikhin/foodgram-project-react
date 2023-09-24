### Проект Foodgram
Foodgram - социальная сеть для публикации рецептов. Сайт выполнен на основе django rest framework и react. В Foodgram реализована функция подписки на авторов, добавление рецептов в избранное, ингредиенты в список покупок, скачивать список покупок

Доступен по [ссылке](https://epikhinfoodgramyp.ddns.net/)

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
Логин: admin
Пароль: a
### Автор backend'a
Епихин Александр (о)_(о)
