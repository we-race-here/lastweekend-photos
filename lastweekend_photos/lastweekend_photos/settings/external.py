import os
import sys

from .base import EXTERNAL_CONFIG_PATH, BASE_DIR


def load_module_from_source(path, name=""):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    if not spec:
        raise ImportError('Not found: {}'.format(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


DJANGO_EXTERNAL_CONFIG_PATH = os.getenv('DJANGO_EXTERNAL_CONFIG_PATH', '') or EXTERNAL_CONFIG_PATH
DJANGO_EXTERNAL_CONFIG_PATH = DJANGO_EXTERNAL_CONFIG_PATH.replace('{BASE_DIR}', BASE_DIR)
_external_config = load_module_from_source(DJANGO_EXTERNAL_CONFIG_PATH, '')
self_module = sys.modules[__name__]
for k in dir(_external_config):
    if k.isupper():
        setattr(self_module, k, getattr(_external_config, k))
