from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_favourite',
]

ACCEPTED_FAVORITE_MODELS = []

MIGRATION_MODULES['garpix_favourite'] = 'app.migrations.garpix_favourite'
