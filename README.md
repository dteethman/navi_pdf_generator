# Генератор PDF с ценниками

## API

### /create
Вход: JSON\
Выход: PDF

Формат входа
```json
[
  {
    "icon": "icons/protect.png",
    "zone": "Защищай смартфон",
    "title": "Vivo",
    "category": "Чехлы",
    "quantity": 2
  }
]
```
Если title отсутствует, то он все равно должен передаваться как пустая строка.
