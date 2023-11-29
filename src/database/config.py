from settings import settings

config = {
    'connections': {
        'default': f'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@db:5432/{settings.POSTGRES_DB}'
    },
    'apps': {
        'models': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default'
        }
    }
}
