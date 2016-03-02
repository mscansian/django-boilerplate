# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = open(os.path.expanduser('~/.django-secret')).read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': open(os.path.expanduser('~/.django-dbpass')).read().strip(),
        'HOST': '',
        'PORT': '',
    },
}
