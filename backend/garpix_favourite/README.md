# Garpix Favourite

Избранное для любых моделей. Является частью GarpixCMS.

## Быстрый старт

Установка через pipenv:

```bash
pipenv install garpix_favourite
```

Добавьте `garpix_favourite` в `INSTALLED_APPS` и укажите адрес для миграций:

```python
# settings.py
from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_favourite',
]

MIGRATION_MODULES['garpix_favourite'] = 'app.migrations.garpix_favourite'
```

Создайте директории и файлы:

```bash
backend/app/migrations/garpix_favourite/
backend/app/migrations/garpix_favourite/__init__.py
```

Сделайте миграции и мигрируйте:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Добавьте в `urls.py`:

```python

# ...
urlpatterns = [
    # ...
    # garpix_favourite
    path('', include(('garpix_favourite.urls', 'favourite'), namespace='garpix_favourite')),

]
```


# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)

