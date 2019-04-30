import traceback

from .base import *

########## Load external config ##########
django_external_config_path = os.getenv('DJANGO_EXTERNAL_CONFIG_PATH', '') or EXTERNAL_CONFIG_PATH
try:
    from .external import *
except ImportError:
    pass
except Exception:
    print('!!!PLEASE CHECK!!! Invalid external setting format: [{}].'.format(django_external_config_path))
    traceback.print_exc()

#############################################
