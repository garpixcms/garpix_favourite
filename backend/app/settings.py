from garpixcms.settings import *  # noqa
from garpix_user.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_favourite',
    'garpix_user'
]

ACCEPTED_FAVORITE_MODELS = ['User']

MIGRATION_MODULES.update({
    'garpix_favourite': 'app.migrations.garpix_favourite',
    'garpix_user': 'app.migrations.garpix_user'
})

GARPIX_USER = {

}
