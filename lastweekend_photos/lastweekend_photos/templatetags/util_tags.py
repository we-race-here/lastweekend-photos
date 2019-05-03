# noinspection PyPep8Naming
import json as JSON
import re

from django import template
from django.apps import apps
# noinspection PyCompatibility
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def active_if(context, *view_name):
    if context.request.resolver_match.view_name in view_name:
        return 'active'
    return ''


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def join_and(value):
    """Given a list of strings, format them with commas and spaces, but
    with 'and' at the end.

    >>> join_and(['apples', 'oranges', 'pears'])
    "apples, oranges, and pears"

    """
    # convert numbers to strings
    value = [str(item) for item in value]
    if len(value) == 0:
        return ''
    if len(value) == 1:
        return value[0]

    # join all but the last element
    all_but_last = ", ".join(value[:-1])
    return "%s, and %s" % (all_but_last, value[-1])


@register.filter
def join_by_attr(the_list, attr_name='name'):
    return ', '.join(
        str(getattr(i, attr_name)) for i in (the_list or []))


@register.filter
def ex_join(the_list, splitter=', '):
    return splitter.join(str(l) for l in (the_list or []))


# noinspection PyPep8Naming
@register.filter
def index(List, i):
    if i is None:
        return None
    return List[int(i)]


@register.filter(name='getattribute')
def getattribute(value, arg):
    """
    Gets an attribute of an object dynamically AND recursively
    from a string name
    """
    numeric_test = re.compile(r"^\d+$")
    if "." in str(arg):
        firstarg = str(arg).split(".")[0]
        value = getattribute(value, firstarg)
        arg = ".".join(str(arg).split(".")[1:])
        return getattribute(value, arg)
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif isinstance(value, dict) and arg in value:
        return value[arg]
    elif isinstance(value, dict) and str(arg) in value:
        return value[str(arg)]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return ''


@register.filter
def json(a):
    json_str = JSON.dumps(a)
    escapes = ['<', '>', '&']
    for c in escapes:
        json_str = json_str.replace(c, r'\u%04x' % ord(c))

    return mark_safe(json_str)


json.is_safe = True


# noinspection PyPep8Naming
def _get_field(Model, field_name):
    if isinstance(Model, str):
        Model = apps.get_model(Model)

    # noinspection PyProtectedMember
    return Model._meta.get_field(field_name)


@register.simple_tag
def get_verbose_field_name(Model, field_name):
    """
    Returns verbose_name for a field.
    """
    field = _get_field(Model, field_name)
    return field.verbose_name


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def split(s, splitter=" "):
    return s.split(splitter)


# noinspection PyShadowingBuiltins
@register.filter
def equals(input, value):
    return input == value


@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.simple_tag(takes_context=True)
def ex_url(context, name, *args, **kwargs):
    """ External url tag """
    hostname = context.get('hostname') or kwargs.pop('_hostname', None)
    if not hostname:
        request = context.get('request')
        hostname = request and request.get_host()
    if not hostname:
        hostname = settings.HOSTNAME

    if not name:
        return hostname
    url = reverse(name, args=args, kwargs=kwargs)
    return '{0}{1}'.format(hostname, url)


# noinspection PyUnusedLocal
@register.simple_tag(takes_context=True)
def page_size_combo(context, *sizes, **kwargs):
    if not sizes:
        sizes = (10, 20, 30, 50)
    page_size = context.request.GET.get('page_size') or kwargs.get('default', None)
    html = 'Page Size <select class="page-size" name="page_size">'
    for size in sizes:
        selected = ('selected' if str(size) == str(page_size) else '')
        html += '<option value="{0}" {1}>{0}</option>'.format(
            size, selected)
    html += '</select>'
    return mark_safe(html)
