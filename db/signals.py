from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import BIFUser

def logUserLogin(sender, user, request, **kwargs):
    logInfo(request, 'logged in')

def logUserLogout(sender, user, request, **kwargs):
    logInfo(request, 'logged out')

def logLoginFail(sender, credentials, request, **kwargs):
    logInfo(request, 'login failed (%s)' % credentials['username'])

user_logged_in.connect(logUserLogin)
user_logged_out.connect(logUserLogout)
user_login_failed.connect(logLoginFail)

import logging

def logInfo(request, message):
    logger = logging.getLogger(__name__)
    logger.info(logMessage(request,message))


def logError(request, message):
    logger = logging.getLogger(__name__)
    logger.error(logMessage(request,message))


def logMessage(request, message):
    from datetime import datetime
    username = 'anonymous-user'
    if request and hasattr(request,'user') and hasattr(request.user,'username') and request.user.username != '':
        username = request.user.username
    ipaddr = 'ip-unknown'
    if request:
        ipaddr = request.META.get('REMOTE_ADDR')
    return "%s %s %s: %s" % (datetime.now().strftime("%Y-%m-%d %X"),ipaddr,username, message)

