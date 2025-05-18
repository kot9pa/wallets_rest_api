# Wallets REST API

## Docker
1. Сборка приложения  
`docker build -t app_wallets .`  

2. Запуск БД и приложения (веб-сервер)  
`docker compose up -d`  

    PGAdmin UI http://localhost:8080/

3. Миграция тестовых данных (для Locust)  
`docker exec app_wallets alembic upgrade head`  

## REST API
1. Получение всех кошельков  
`GET localhost:8000/api/v1/wallets`  

2. Получение кошелька по UUID  
`GET localhost:8000/api/v1/wallets/{wallet_uuid}`  

3. Выполнение операций с кошельком  
`GET localhost:8000/api/v1/wallets/{wallet_uuid}/operation`  

    Swagger UI http://localhost:8000/  

## Тестирование
1. Unit tests (Pytest)  
`docker exec app_wallets pytest -v`  

2. Load tests (Locust)  
`docker exec app_wallets locust`  

    Locust UI http://localhost:8089/  

## CLI (опционально)
1. Отредактировать .env и src/config.py (для загрузки переменных окружения)  
2. Запуск из терминала  
`uvicorn src.main:app --workers 4`  

    --workers = number of worker processes (default: 1)