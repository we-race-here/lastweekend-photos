from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'weekend-photos',
        'USER': 'weekend-photos_user',
        'PASSWORD': '123sat',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

SENDSMS_BACKEND = 'sendsms.backends.dummy.SmsBackend'
