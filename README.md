# Bookmarks App
### О проекте
Bookmarks App - проект для сохранения пользователем веб-сайтов в закладки. После регистрации в сервисе пользователь может создавать различные коллекции в
которые будет добавлять свои закладки. Одна и та же закладка может быть в одной или нескольких коллекциях сразу.
Пользователь отправляет ссылку, далее сервис получает следующую информацию о ссылке из html-кода страницы:
- Заголовок страницы
- Краткое описание
- Ссылка на страницу
- Тип ссылки
- Картинка превью

### Технологии
- Python
- Django
- DRF
- Djoser
- Beautifulsoup4
- Docker
- PostgreSQL

### Как запустить проект
- Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Etozheigor/bookmarks.git
```

```
cd bookmarks
```

- Активировать виртуальное окружение и установить зависимости:

```
poetry shell
poetry install
```

- перейти в папку bookmarks_app/bookmarks_app, создать файл .env и заполнить его по шаблону (можно использовать
файл .env.example, заполнив необходимые данные и просто переименовав его в .env) :


шаблон заполнения файла:

```
SECRET_KEY= # секретный ключ Джанго-проекта
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER= # логин для подключения к базе данных (установите свой)
POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)
DB_HOST=localhost
DB_PORT=5432
```


База данных Postgres запускается в контейнере Docker:

- Перейти в папку с файлом docker-compose.yml и запустить контейнер:

```
docker-compose up
```
- Перейти в папку bookmarks_app, выполнить миграции и запустить проект

```
cd bookmarks_app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Проект будет доступен локально по адресу:

```
http://localhost/
```

Документация к Api находится по адресу:

```
http://localhost/swagger/
```

### Эндпоинты проекта:
- Регистрация пользователя:
```
http://localhost/api/v1/users/
```
- Вход/выход из системы (получение токена)
```
http://localhost/api/v1/auth/jwt/create/
http://localhost/api/v1/auth/jwt/refresh/
http://localhost/api/v1/auth/jwt/verify/
```
- Добавление/получение/изменение(добавление закладки в коллекцию)/удаление закладки:
```
http://localhost/api/v1/bookmarks/
```
-Добавление/получение/изменение/удаление коллекции:
```
http://localhost/api/v1/collections/
```
