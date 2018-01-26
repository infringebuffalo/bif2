from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.template import loader
from django.core.mail import EmailMultiAlternatives

from .models import *

import json

def index(request):
    props = Proposal.objects.all()
    return render(request,'db/index.html', { 'prop_list' : props })


def submit(request):
    infodict = {}
    infodict = request.POST.copy()
    for k in ['title','csrfmiddlewaretoken']:
        if k in infodict.keys():
            del infodict[k]

    infojson = json.dumps(infodict)
    prop = Proposal(title=request.POST["title"],info=infojson,status=Proposal.WAITING)
    prop.save()

    mail_to = infodict["contactemail"]
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( mail_to )
    except ValidationError:
        return render(request,'db/proposal_email_fail.html', {'address':mail_to})
    context = {'prop':prop, 'prop_info':infodict}
    mail_subject = "Buffalo Infringement Festival proposal '%s'" % prop.title
    mail_body = loader.render_to_string('db/submit_email.txt', context)
    EmailMultiAlternatives(mail_subject, mail_body, None, [mail_to]).send()
    return render(request,'db/proposal_submit.html', {})


def confirmProposal(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    prop.status = Proposal.ACCEPTED     # Note that this will also undelete a deleted proposal - will leave it that way for now
    prop.save()
    logInfo("confirmed proposal %d" % id, request)
    return render(request,'db/proposal_confirm.html', {'title':prop.title})


def musicForm(request):
    return render(request,'db/music_form.html', {})


def newAccount(request):
    return render(request,'db/new_account.html', {})


from django.contrib.auth.models import User

def createAccount(request):
    from django.db.utils import IntegrityError
    email = request.POST['email']
    password = request.POST['password']
    try:
        djuser = User.objects.create_user(email, email, password)
    except IntegrityError:
        logError("Tried to create duplicate account '%s'"%email)
        err = "An account '%s' already exists" % email
        return render(request, 'db/new_account.html', { 'error': err })
    except:
        logError("Unknown error creating account '%s'"%email)
        return render(request, 'db/new_account.html', { 'error': 'Failed to create account.' })
    bifuser = BIFUser.objects.create(user=djuser, phone='555-1212')
    login(request, authenticate(username=email,password=password))
    logInfo("Created new account '%s'"%email)
    return redirect('index')


@login_required
def proposal(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    infodict = json.loads(prop.info)
    context = {'prop':prop, 'prop_info':infodict}
    return render(request,'db/proposal.html', context)


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
    if request and request.user and request.user.username and request.user.username != '':
        username = request.user.username
    ipaddr = 'ip-unknown'
    if request:
        ipaddr = request.META.get('REMOTE_ADDR')
    return "%s %s %s: %s" % (datetime.now().strftime("%Y-%m-%d %X"),ipaddr,username, message)

