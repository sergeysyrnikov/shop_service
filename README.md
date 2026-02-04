# Тестовый сервис 
### Представляет coбой тестовый асинхронный FastAPI сервер(магазин товаров)

## Запуск проекта

В терминале из корня проекта выполнить команду:

- **Для разработки (dev):**

```bash
  ENV=dev uvicorn main:shop_app --reload
```
- **Для разработки (prod):**
```bash
  ENV=prod uvicorn main:shop_app --reload
```
    

## Database schema

[![DB schema](docs/db/schema.svg)](https://dbdiagram.io/d/shop-69820089bd82f5fce27fa965)