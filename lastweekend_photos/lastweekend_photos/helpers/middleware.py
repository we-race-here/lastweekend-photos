import os
import traceback

import simplejson as json
from django.conf import settings
from reversion.middleware import RevisionMiddleware


class DisableCSRFMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'CSRF_DISABLED', False):
            setattr(request, '_dont_enforce_csrf_checks', True)

        response = self.get_response(request)
        return response


class InjectUiVersionInHeadersMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_ui_version(self):
        ui_packages_path = os.path.join(settings.BASE_DIR, 'FRONTEND', 'lastweekend_photos_ui', 'package.json')
        if not os.path.exists(ui_packages_path):
            return
        version = None
        try:
            with open(ui_packages_path) as f:
                data = json.load(f)
            version = data.get('version')
        except Exception:
            traceback.print_exc()
        return version

    def __call__(self, request):
        response = self.get_response(request)
        ui_version = self._get_ui_version()
        if ui_version:
            response['X-UI-Version'] = ui_version
        else:
            print('Cannot discover UI version!')
        return response


class CustomRevisionMiddleware(RevisionMiddleware):
    atomic = False
