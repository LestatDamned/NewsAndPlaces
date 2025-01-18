# News and Places

Проект для управления новостями и примечательными местами с интеграцией данных о погоде.  
Он позволяет:  
- Создавать и управлять новостями.  
- Отправлять рассылки с новостями.  
- Импортировать данные о местах из xlsx-файлов.  
- Отслеживать погоду для этих мест.  
- Экспортировать отчеты по погоде в формате xlsx.

---

## Стек технологий

- **Python 3.12**
- **Django**
- **Django Rest Framework**
- **Celery**
- **Celery Beat** для периодических задач
- **Redis**
- **PostgreSQL** (с использованием PostGIS для работы с геоданными)
- **Docker**

---

## Установка и запуск

### Требования

- **Docker**  
- **Docker Compose**

### Шаги для запуска

1. **Склонируйте репозиторий**:
    ```bash
   git clone https://github.com/LestatDamned/NewsAndPlaces.git
   cd news_and_places
    ```

2. **Скопируйте файл `.env.example` в `.env` и настройте параметры**:
   ```bash
   cp .env.example .env
   ```
   Пример `.env`
   ``` bash
   # Настройки для отправки email
   EMAIL_HOST=your-smtp-host             # Адрес SMTP-сервера (например, smtp.gmail.com)
   EMAIL_HOST_USER=your-email@example.com # Логин (электронная почта)
   EMAIL_HOST_PASSWORD=your-password      # Пароль от сервиса
   DEFAULT_FROM_EMAIL=your-email@example.com # Почта, с которой будут отправляться письма
   
   # Настройки базы данных PostgreSQL
   POSTGRES_NAME=your-db-name            # Имя базы данных
   POSTGRES_USER=your-db-user            # Пользователь базы данных
   POSTGRES_PASSWORD=your-db-password    # Пароль пользователя
   POSTGRES_DB=your-db-name              # Имя базы данных (дублируется для удобства)
   POSTGRES_HOST=db                      # Хост базы данных (например, 'db' для Docker)
   POSTGRES_PORT=5432                    # Порт PostgreSQL (по умолчанию 5432)
   
   # Настройки Redis
   REDIS_HOST=redis://redis:6379/0       # Адрес Redis для задач Celery
   REDIS_CACHES=redis://redis:6379/1     # Адрес Redis для кэширования
   
   # API-ключ для получения данных о погоде
   WEATHER_API_KEY=your-weather-api-key  # Ваш API-ключ от OpenWeatherMap
   ```

3. **Запустите контейнеры с помощью Docker Compose**:
   ```bash
   docker compose up --build
   ```

4. **Доступ к проекту**:  
   После запуска проект будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Настройки

Проект использует `django-constance` для настройки параметров через админку Django.  
Основные настройки:  
- **NEWS_RECIPIENTS** — список получателей рассылки новостей.  
- **NEWS_SUBJECT** — тема письма.  
- **NEWS_TEXT** — текст письма.  
- **NEWS_TIME_OF_MESSAGE** — время отправки ежедневной рассылки новостей.  
- **WEATHER_REPORT_INTERVAL** — интервал между запросами погоды (в секундах, минутах, часах, днях).  
- **WEATHER_REPORT_PERIOD** — период для задач Celery (секунды, минуты, часы, дни).

---

## Миграции и начальная настройка

1. **Примените миграции** для создания таблиц базы данных:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

2. **Создайте суперпользователя** для доступа в админку:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

3. **Доступ к админке**:  
   После настройки админка будет доступна по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

---

## Документация API

### Основные эндпоинты:

1. **CRUD Новости**  
   **`GET /api/news/`** — Список новостей.  
   **`POST /api/news/`** — Создание новости.  
   **`GET /api/news/{id}/`** — Получение новости по ID.  
   **`PUT /api/news/{id}/`** — Обновление новости.  
   **`DELETE /api/news/{id}/`** — Удаление новости.

2. **Импорт мест из xlsx**  
   **`POST /api/import_places/`** — Импортирует данные из xlsx-файла.  

   Формат xlsx-файла:
   - **1 колонка**: Название места (строка).  
   - **2 колонка**: Координаты места в формате "широта, долгота" (строка, например: "56.0105, 92.8625").  
   - **3 колонка**: Рейтинг места (целое число от 0 до 25).  

   **Пример использования с Postman**:  
   - URL: `http://127.0.0.1:8000/api/import_places/`.  
   - Метод: `POST`.  
   - В Body выберите `form-data` и добавьте ключ:  
     - Key: `file`  
     - Type: `File`  
     - Value: Выберите ваш файл `.xlsx`.

3. **Экспорт погоды в xlsx**  
   **`GET /api/export_weather/`** — Экспорт данных о погоде.  

   **Параметры запроса**:
   - `place_id` — ID места.  
   - `start_date` — Дата начала в формате `ГГГГ-ММ-ДД`.  
   - `end_date` — Дата конца в формате `ГГГГ-ММ-ДД`.  

   **Пример запроса**:
   ```bash
   GET /api/export_weather/?place_id=1&start_date=2025-01-01&end_date=2025-01-16
   ```

---

## Примечания

- Данные о погоде получаются из [OpenWeatherMap API](https://openweathermap.org/api).  
  Добавьте ваш API-ключ в файл `.env` для работы.  
- Для разработки и тестирования используются Docker и Docker Compose.  
- Контейнеры запускаются с помощью:
   ```bash
   docker-compose up
   ```