import ast
import base64
import datetime
import decimal
import functools
import inspect
import random
import string
import traceback
import uuid

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied, RequestDataTooBig
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.constants import EMPTY_VALUES
from rest_framework import status, serializers
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from rest_framework.filters import OrderingFilter as OrderingFilterBackend
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from sendsms import api
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.mail.backends.filebased import EmailBackend
from django.contrib.auth.mixins import PermissionRequiredMixin as \
    DjangoPermissionRequiredMixin

print = functools.partial(print, flush=True)


def to_dict(obj, fields=None, fields_map=None, extra_fields=None):
    """
    convert a model object to a python dict.
    @param obj: object of a db model
    @param fields: list of fields which we want to show in return value.
        if fields=None, we show all fields of model object
    @type fields: list
    @param fields_map: a map converter to show fields as a favorite.
        every field can bind to a lambda function in fields_map.
        if a field was bind to a None value in fields_map, we ignore this field
        to show in result
    @type fields_map: dict
    @param extra_fields: add new or override existing fields
    """
    data = {}
    fields_map = fields_map or {}

    if fields is None:
        fields = [f.name for f in obj.__class__._meta.fields]
    fields.extend(extra_fields or [])
    for field in fields:
        if field in fields_map:
            if fields_map[field] is None:
                continue
            func = fields_map.get(field)
            if len(inspect.signature(func).parameters) == 1:
                v = func(obj)
            else:
                v = func()
        else:
            v = getattr(obj, field, None)
        if isinstance(v, datetime.datetime):
            data[field] = v.isoformat() + 'Z'
        elif isinstance(v, datetime.date):
            data[field] = v.isoformat()
        elif isinstance(v, decimal.Decimal):
            data[field] = float(v)
        else:
            data[field] = v

    return data


class CustomPagination(PageNumberPagination):
    """ Custom Pagination to be used in rest api"""

    BIG_PAGE_SIZE = 10000000
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        if view:
            max_page_size = getattr(view, 'max_page_size', self.max_page_size)
            if max_page_size is None:
                max_page_size = settings.REST_FRAMEWORK.get('MAX_PAGE_SIZE_DEFAULT', 100)
            self.max_page_size = self.BIG_PAGE_SIZE if max_page_size == 0 else max_page_size
        return super(CustomPagination, self).paginate_queryset(queryset, request, view=view)

    def get_page_size(self, request):
        """
        this is overrided to allow 0 as a page_size.
        if page_size=0, we will set page_size as max_page_size.
        """
        page_size = self.page_size
        if self.page_size_query_param:
            try:
                page_size = _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=False,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass
        if page_size == 0:
            page_size = self.max_page_size
        return page_size

    def get_paginated_response(self, data):
        """ override pagination structure in list rest api """
        next_page = self.page.next_page_number() if \
            self.page.has_next() else None
        previous_page = self.page.previous_page_number() if \
            self.page.has_previous() else None
        return Response({
            'pagination': {
                'next_url': self.get_next_link(),
                'previous_url': self.get_previous_link(),
                'current_page': self.page.number,
                'next_page': next_page,
                'previous_page': previous_page,
                'first_page': 1,
                'last_page': self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request),
                'total': self.page.paginator.count,
            },
            'results': data
        })


class DuplicateError(APIException):
    status_code = status.HTTP_409_CONFLICT


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'


class CustomLoggingMixin(LoggingMixin):
    '''
    Customized and enhanced LoggingMixin
    '''
    CLEANED_SUBSTITUTE = '****'
    SKIPPED_SUBSTITUTE = '<<skipped>>'
    INVALID_SUBSTITUTE = '<<invalid>>'
    logging_methods = settings.DRF_TRACKING_LOGGING_METHODS
    sensitive_fields = {
        'current_password', 'new_password', 're_new_password'
    }
    skipped_fields = {
        'image', 'photo', 'avatar', 'photo_thumb'
    }

    def handle_exception(self, exc):
        response = super(CustomLoggingMixin, self).handle_exception(exc)
        skip_errors = getattr(self, 'drf_tracking_skip_errors_data', settings.DRF_TRACKING_SKIP_ERRORS_DATA)
        if isinstance(skip_errors, dict):
            method = self.log.get('method')
            skip_errors = skip_errors.get(method.lower(), False) or skip_errors.get(method.upper(), False)
        if isinstance(exc, APIException) and exc.status_code < 500:
            self.log.pop('errors', None)
        elif skip_errors:
            self.log['errors'] = self.SKIPPED_SUBSTITUTE
        return response

    def logging_skip_response(self):
        method = self.log.get('method') or ''
        skip_response = getattr(self, 'drf_tracking_skip_response_data', settings.DRF_TRACKING_SKIP_RESPONSE_DATA)
        if isinstance(skip_response, dict):
            skip_response = skip_response.get(method.lower(), False) or skip_response.get(method.upper(), False)
        return skip_response

    def logging_skip_data(self):
        method = self.log.get('method') or ''
        skip_data = getattr(self, 'drf_tracking_skip_request_data', settings.DRF_TRACKING_SKIP_REQUEST_DATA)
        if isinstance(skip_data, dict):
            skip_data = skip_data.get(method.lower(), False) or skip_data.get(method.upper(), False)
        return skip_data

    def logging_skip_query_params(self):
        method = self.log.get('method') or ''
        skip_query_params = getattr(self, 'drf_tracking_skip_request_query_params',
                                    settings.DRF_TRACKING_SKIP_REQUEST_QUERY_PARAMS)
        if isinstance(skip_query_params, dict):
            skip_query_params = skip_query_params.get(method.lower(), False) or skip_query_params.get(method.upper(),
                                                                                                      False)
        return skip_query_params

    def handle_log(self):
        skip_response = self.logging_skip_response()
        skip_data = self.logging_skip_data()
        skip_query_params = self.logging_skip_query_params()
        if skip_response:
            self.log['response'] = self.SKIPPED_SUBSTITUTE
        if skip_data:
            self.log['data'] = self.SKIPPED_SUBSTITUTE
        if skip_query_params:
            self.log['query_params'] = self.SKIPPED_SUBSTITUTE
        return super(CustomLoggingMixin, self).handle_log()

    def _clean_data(self, data):
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except UnicodeDecodeError:
                data = self.INVALID_SUBSTITUTE

        if isinstance(data, list):
            return [self._clean_data(d) for d in data]
        if isinstance(data, dict):
            SENSITIVE_FIELDS = {'api', 'token', 'key', 'secret', 'password', 'signature'}
            SKIPPED_FIELDS = self.skipped_fields or set()
            data = dict(data)
            if self.sensitive_fields:
                SENSITIVE_FIELDS = SENSITIVE_FIELDS | {field.lower() for field in self.sensitive_fields}

            for key in list(data.keys()):
                if key.lower() in SKIPPED_FIELDS:
                    data[key] = self.SKIPPED_SUBSTITUTE
                    continue
                if key.lower() in SENSITIVE_FIELDS:
                    data[key] = self.CLEANED_SUBSTITUTE
                    continue
                value = data[key]
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass
                if isinstance(value, list) or isinstance(value, dict):
                    data[key] = self._clean_data(value)
        return data


class PermissionRequiredMixin(DjangoPermissionRequiredMixin):

    def get_permission_required(self):
        perms = self.permission_required or ()
        if isinstance(perms, dict):
            perms = perms.get(self.request.method.lower(), ()) or ()

        if isinstance(perms, str):
            perms = (perms,)

        return perms

    def handle_no_authenticated(self):
        if self.request.is_ajax():
            return JsonResponse({'error': 'Not Authorized'}, status=401)
        return redirect_to_login(self.request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())

    def handle_no_permission(self):
        if self.request.is_ajax():
            return JsonResponse({'error': 'Permission Denied'}, status=403)
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return render(self.request, "no-permission.html", status=403)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_authenticated()
        if not self.has_permission():
            return self.handle_no_permission()
        return super(PermissionRequiredMixin, self
                     ).dispatch(request, *args, **kwargs)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if not isinstance(data, UploadedFile):
            if hasattr(data, 'read'):
                data = data.read().decode()
            if data.startswith('data:image'):
                fmt, imgstr = data.split(';base64,')  # fmt ~= data:image/X,
                ext = fmt.split('/')[-1]  # guess file extension
                uid = uuid.uuid4()
                data = ContentFile(base64.b64decode(imgstr), name=uid.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)


class CustomFileBasedEmailBackend(EmailBackend):
    def write_message(self, message):
        res = super(CustomFileBasedEmailBackend, self).write_message(message)
        if getattr(settings, 'EMAIL_BODY_TO_FILE'):
            try:
                with open(settings.EMAIL_BODY_TO_FILE, 'w') as f:
                    f.write(str(message.body))
            except Exception:
                traceback.print_exc()
        if getattr(settings, 'EMAIL_BODY_TO_CONSOLE') is True:
            print(message.body)
        return res


def random_id(n=8, no_upper=False, no_lower=False, no_digit=False):
    rand = random.SystemRandom()
    chars = ''
    if no_upper is False:
        chars += string.ascii_uppercase
    if no_lower is False:
        chars += string.ascii_lowercase
    if no_digit is False:
        chars += string.digits
    if not chars:
        raise Exception('chars is empty! change function args!')
    return ''.join([rand.choice(chars) for _ in range(n)])


def send_sms(message, to, from_=None, fail_silently=False):
    from_ = from_ or settings.SMS_DEFAULT_FROM_PHONE
    if isinstance(to, str):
        to = [to]
    return api.send_sms(body=message, from_phone=from_, to=to, fail_silently=fail_silently)


def ex_reverse(viewname, **kwargs):
    if viewname.startswith('http://') or viewname.startswith('https://'):
        return viewname

    host = kwargs.pop('hostname', None)
    request = kwargs.pop('request', None)
    scheme = kwargs.pop('scheme', None)
    if not host:
        host = request.get_host() if request else settings.HOSTNAME

    if not viewname:
        rel_path = ''
    elif viewname.startswith('/'):
        rel_path = viewname
    else:
        rel_path = reverse(viewname, **kwargs)

    scheme = '{}://'.format(scheme) if scheme else ''

    return '{0}{1}{2}'.format(scheme, host, rel_path)


class NotSet(object):
    pass


def custom_rest_exception_handler(exc, context):
    """ Custom rest api exception handler """
    from rest_framework import exceptions
    from rest_framework.views import exception_handler, set_rollback
    response = exception_handler(exc, context)
    if response is None:
        if isinstance(exc, RequestDataTooBig):
            response = Response({'reason': 'too big data or file upload'},
                                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        else:
            response = Response({'reason': 'unexpected server error'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
            traceback.print_exc()
        return response

    err_msg = str(exc)
    if isinstance(exc, ProtectedError):
        data = {'reason': 'cannot delete this record! this record is related to other entities and is protected'}
        set_rollback()
        return Response(data, status=status.HTTP_412_PRECONDITION_FAILED)
    if isinstance(exc, IntegrityError) and ('already exists' in err_msg or 'must make a unique set' in err_msg or
                                            'must be unique' in err_msg):
        data = {'reason': 'duplicate unique key'}
        set_rollback()
        return Response(data, status=status.HTTP_409_CONFLICT)
    if isinstance(exc, exceptions.NotAuthenticated):
        response.status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, exceptions.ValidationError) and (
            'already exists' in err_msg or 'must make a unique set' in err_msg or 'must be unique' in err_msg):
        response.status_code = status.HTTP_409_CONFLICT

    return response


class DynamicFieldsSerializerMixin(object):
    """
    This class allow you to have dynamic fields in get rest api.
    user can pass "fields" and "xfields" as a get query parameter.
    "fields" specify list of fields you want to be shown as a result.
    "xfields" specify list of fields you want to be excluded in result.
    i.e:
    fields=id,name
    or
    xfields=name1,name2
    """
    extra_fields = []

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)
        if not self.context:
            return

        params = self.context['request'].query_params
        fields = params.get('fields')
        xfields = params.get('xfields')
        exfields = (params.get('exfields') or '').split(',')
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if xfields:
            xfields = xfields.split(',')
            for field_name in xfields:
                self._exclude_field(field_name.split('.'))

        for extra_field in self.extra_fields:
            if extra_field not in exfields:
                self._exclude_field(extra_field.split('.'))

    def _exclude_field(self, field_name, fields_container=None):
        if fields_container == None:
            fields_container = self.fields

        if len(field_name) == 1:
            return fields_container.pop(field_name[0], None)
        inner_fields = fields_container.get(field_name[0], None)
        if not inner_fields:
            return
        return self._exclude_field(field_name[1:], inner_fields.fields)


class ExtendedOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        self.ordering_map = kwargs.pop('ordering_map', {})
        super(ExtendedOrderingFilter, self).__init__(*args, **kwargs)

    def get_ordering_value(self, param):
        descending = param.startswith('-')
        param = param[1:] if descending else param
        field_name = self.param_map.get(param, param)
        field_name = self.ordering_map.get(field_name, field_name)
        if callable(field_name):
            res = field_name(descending)
            if not isinstance(res, (tuple, list)):
                res = [res]
            return res
        if isinstance(field_name, str):
            field_name = (field_name,)

        return [("-%s" % f if descending else f) for f in field_name]

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        ordering = []
        for param in value:
            ordering.extend(list(self.get_ordering_value(param)))
        return qs.order_by(*ordering)


class ExtendedOrderingFilterBackend(OrderingFilterBackend):
    def get_valid_fields(self, queryset, view, context=None):
        fields = super(ExtendedOrderingFilterBackend, self).get_valid_fields(queryset, view, context=context or {})
        extra_fields = getattr(view, 'extra_ordering_fields', {}) or {}
        fields.extend([(item, item) for item in extra_fields.keys()])
        return fields

    def get_ordering(self, request, queryset, view):
        fields = super(ExtendedOrderingFilterBackend, self).get_ordering(request, queryset, view)
        extra_fields = getattr(view, 'extra_ordering_fields', {}) or {}
        if not extra_fields:
            return fields
        new_fields = []
        for field in fields:
            descending = field.startswith('-')
            field = field[1:] if descending else field
            field_ordering = extra_fields.get(field, field)
            if callable(field_ordering):
                field_ordering = field_ordering(descending)
                if not isinstance(field_ordering, (list, tuple)):
                    field_ordering = (field_ordering,)
            else:
                if isinstance(field_ordering, str):
                    field_ordering = (field_ordering,)
                field_ordering = ['{}{}'.format('-' if descending else '', f) for f in field_ordering]
            new_fields.extend(field_ordering)
        return new_fields


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'OPTIONS': [],
        'HEAD': [],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ExplicitPermissions(BasePermission):
    '''
    set this as a member of permission_classes field of view. i.e:
    permission_classes=(permissions.IsAuthenticated, ExplicitPermissions)

    in View classs we need to have a class property called 'explicit_permissions'. i.e:
    explicit_permissions = 'student.view_therapiststudentassigned'
    explicit_permissions = ['student.view_therapiststudentassigned', 'student.add_therapiststudentassigned']
    explicit_permissions = {
        'staff_assign': 'student.view_therapiststudentassigned'
    }
    explicit_permissions = {
        'staff_assign': {
            'get': 'student.view_therapiststudentassigned',
            'post': 'student.add_therapiststudentassigned'
        }
    }
    '''

    def has_permission(self, request, view):
        perms = getattr(view, 'explicit_permissions', None)
        http_method = request.method.lower()
        action = view.action
        if isinstance(perms, dict):
            perms = perms.get(action, []) or []
        if isinstance(perms, dict):
            perms = perms.get(http_method, []) or []
        if isinstance(perms, str):
            perms = [perms]
        return True if not perms else request.user.has_perms(perms)


def capitalize_first(s):
    if s:
        return s[0].upper() + s[1:]
    return s


def netref_to_native(d):
    if isinstance(d, dict):
        return {k: netref_to_native(v) for k, v in d.items()}
    if isinstance(d, list):
        return list(netref_to_native(v) for v in d)
    if isinstance(d, tuple):
        return tuple(netref_to_native(v) for v in d)
    if isinstance(d, set):
        return set(netref_to_native(v) for v in d)
    return d


def success_message(message, request):
    return messages.success(request, mark_safe(message))


def error_message(message, request):
    return messages.error(request, mark_safe(message), extra_tags='danger')


def info_message(message, request):
    return messages.info(request, mark_safe(message))


def warning_message(message, request):
    return messages.warning(request, mark_safe(message))


def send_form_errors(form, request):
    msgs = []
    for k, v in form.errors.items():
        msg = '' if k.startswith('__') else '{0}: '.format(k)
        msgs.append('<li>{0}{1}</li>'.format(msg, ', '.join(v)))

    if msgs:
        return error_message(''.join(msgs), request)


def get_current_page_size(request, default=None):
    page_size = default or settings.PAGINATION_DEFAULT_PAGINATION
    try:
        page_size = int(request.GET.get('page_size'))
    except (ValueError, TypeError):
        pass

    if page_size <= 0:
        page_size = default or settings.PAGINATION_DEFAULT_PAGINATION
    return min(page_size, settings.PAGINATION_MAX_SIZE)
