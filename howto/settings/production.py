import os
from .howto import BASE_DIR


ADMINS = MANAGERS = ()

ALLOWED_HOSTS = []

SECRET_KEY = ''

DATABASES = {
	'default': {
		'ENGINE': '',
		'HOST': '',
		'NAME': '',
		'USER': '',
		'PASSWORD': ''
	}
}

MONGODB_DATABASE = {
	'HOST': '',
	'NAME': '',
	'USER': '',
	'PASSWORD': '',
	#'PORT': 27017,
	#'CONF': { 'USE_TEXTSEARCH': False }
}

# mount -t tmpfs -o size=[SIZE] tmpfs tmp/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'tmp/'),
        'TIMEOUT': 300
    }
}