import time

from django.conf import settings
from django.core import signing
from django.core.signing import Signer
from django.http import Http404
from django.utils import baseconv
from twilio.rest import Client as TwilioRestClient


def get_twilio_client():
    return TwilioRestClient(settings.SENDSMS_TWILIO_ACCOUNT_SID, settings.SENDSMS_TWILIO_AUTH_TOKEN)


def unsign(s, salt=None, max_age=None, abort=True):
    args = dict(max_age=max_age)
    if salt:
        args['salt'] = salt
    try:
        unsign_res = signing.loads(s, **args)
    except (signing.BadSignature, signing.SignatureExpired):
        if abort:
            raise Http404('Not Found')
        return None
    if not unsign_res or not isinstance(unsign_res, dict):
        if abort:
            raise Http404('Not Found')
        return None
    return unsign_res


def get_signed_age(s, salt=None):
    signer = Signer(salt=salt)
    result = signer.unsign(s)
    value, timestamp = result.rsplit(signer.sep, 1)
    timestamp = baseconv.base62.decode(timestamp)
    age = time.time() - timestamp
    return age
