CSGO Market API SDK — это Python-библиотека (SDK), предназначенная для взаимодействия с CSGO Market API. Она предоставляет удобный и безопасный интерфейс для выполнения операций, таких как:

- Получение информации о скинах и наклейках
- Управление продажами, покупками и ордерами
- Обновление инвентаря
- Перевод средств и управление балансом
- История операций

Библиотека построена на базовом requests, с автоматической повторной попыткой в случае сетевых сбоев благодаря tenacity.
Платформа: https://market.csgo.com
Документация: https://market.csgo.com/ru/api
Создать API KEY: https://market.csgo.com/ru/api/content/start#apigen

Пример использования:
```python
from market_api import MarketApi

api_key = "ваш_ключ_API"

with MarketApi(api_key) as market:
    item = market.search_item_by_hash_name("AK-47 | Redline (Field-Tested)")
    print(item)
```
