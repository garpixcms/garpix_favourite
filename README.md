# Garpix Favourite

Избранное для любых моделей. Является частью GarpixCMS.

## Быстрый старт

Установка через pipenv:

```bash
pip install garpix-favourite
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

Модуль использует [ContentType](https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/), чтобы ограничить список моделей, доступных для добавления в избранное определите переменную `ACCEPTED_FAVORITE_MODELS`

Пример:
```
# settings.py
ACCEPTED_FAVORITE_MODELS = ['Post']
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

Получение сущности которую добавили в фавориты:

```python
from garpix_favourite.models import Favorite

obj = Favorite.objects.first()

print(obj.entity, 'entity')
```

# Changelog

See [CHANGELOG.md](backend/garpix_favourite/CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](backend/garpix_favourite/CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)

