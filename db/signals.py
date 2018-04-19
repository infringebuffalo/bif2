from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import BIFUser

def logUserLogin(sender, user, request, **kwargs):
    logInfo('logged in',request)

def logUserLogout(sender, user, request, **kwargs):
    logInfo('logged out',request)

def logLoginFail(sender, credentials, request, **kwargs):
    logInfo('login failed (%s)' % credentials['username'],request)

user_logged_in.connect(logUserLogin)
user_logged_out.connect(logUserLogout)
user_login_failed.connect(logLoginFail)

import logging

def logInfo(message,request=None):
    logger = logging.getLogger(__name__)
    logger.info(logMessage(message,request))


def logError(message,request=None):
    logger = logging.getLogger(__name__)
    logger.error(logMessage(message,request))


def logMessage(message,request=None):
    from datetime import datetime
    username = 'anonymous-user'
    if request and hasattr(request,'user') and hasattr(request.user,'username') and request.user.username != '':
        username = request.user.username
    ipaddr = 'ip-unknown'
    if request:
        ipaddr = request.META.get('REMOTE_ADDR')
    return "%s %s %s: %s" % (datetime.now().strftime("%Y-%m-%d %X"),ipaddr,username, message)

