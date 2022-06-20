# Foodgram Project
### Описание
Проект продуктовый помощник
### Workflow статус
![example workflow](https://github.com/AlexanderKuryatnikov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Как запустить
1. Клонировать репозиторий:
```
git clone git@github.com:AlexanderKuryatnikov/yamdb_final.git
```
2. Создать docker образ фронта и запушить на [Docker Hub](https://hub.docker.com/)
3. На сервере:
  - Установить *Docker* и *Docker Compose*
  - Скопировать на сервер содержимое папки infra, целиком папку doc и файл ingredients.csv (лежит в папке data)
4. Создать переменные окружения в GitHub Actions:
  - **DOCKER_USERNAME** и **DOCKER_PASSWORD** - логин и пароль на Docker Hub
  - **USER** - имя пользователя для подключения к серверу
  - **SSH_KEY** - ssh-ключ для подключения
  - **PASSPHRASE** - фраза-пароль для подключения, если создавали
  - **DB_ENGINE** - *django.db.backends.postgresql*, приложение работает с postgresql
  - **DB_NAME** - имя базы данных
  - **POSTGRES_USER** - логин для подключения к базе данных
  - **POSTGRES_PASSWORD** - пароль для подключения к БД
  - **DB_HOST** - db, название сервиса (контейнера)
  - **DB_PORT** - 5432, порт для подключения к БД
  - **TELEGRAM_TO** - ID вашего телеграм-аккаунта
  - **TELEGRAM_TOKEN** - токен вашего бота
5. На сервере выполнить миграции, создать суперпользователя и собрать статику:
```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```
6. На сервере скопировать файл ingredients.csv в директорию app/data/ контейнера web и запустить в контейнере скрипт заполнения БД ингредиентами:
```
python manage.py load_ingredients_csv
```
### Адрес сервера и администратор
Адрес: http://http://51.250.21.22
Администратор: admin \
Электронная почта: admin@mail.ru \
Пароль: admin
### Автор
Александр Курятников
