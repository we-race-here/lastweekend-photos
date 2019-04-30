from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'TEST_NAME': 'travis_ci_test',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

SENDSMS_BACKEND = 'sendsms.backends.dummy.SmsBackend'
