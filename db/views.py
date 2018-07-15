from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect

from .models import *

import json

def index(request):
    if request and hasattr(request,'user') and hasattr(request.user,'bifuser'):
        owned = request.user.bifuser.permit_what.filter(permission=UserPermission.OWNER,entity__entityType='proposal',entity__proposal__status=Proposal.ACCEPTED)
        deleted = request.user.bifuser.permit_what.filter(permission=UserPermission.OWNER,entity__entityType='proposal',entity__proposal__status=Proposal.DELETED)
        waiting = request.user.bifuser.permit_what.filter(permission=UserPermission.OWNER,entity__entityType='proposal',entity__proposal__status=Proposal.WAITING)
    else:
        owned = None
        deleted = None
        waiting = None
    return render(request,'db/index.html', { 'owned':owned, 'deleted':deleted, 'waiting':waiting })


@login_required
def allProposals(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    confirmed_props = Proposal.objects.filter(festival=fest,status=Proposal.ACCEPTED).order_by(Lower('title'))
    waiting_props = Proposal.objects.filter(festival=fest,status=Proposal.WAITING).order_by(Lower('title'))
    deleted_props = Proposal.objects.filter(festival=fest,status=Proposal.DELETED).order_by(Lower('title'))
    return render(request,'db/index.html', { 'confirmed_props' : confirmed_props, 'waiting_props' : waiting_props, 'deleted_props': deleted_props })


@login_required
def allVenues(request):
    from django.db.models.functions import Lower
    confirmed_venues = Venue.objects.filter(status=Venue.ACCEPTED).order_by(Lower('name'))
    waiting_venues = Venue.objects.filter(status=Venue.WAITING).order_by(Lower('name'))
    deleted_venues = Venue.objects.filter(status=Venue.DELETED).order_by(Lower('name'))
    return render(request,'db/index.html', { 'confirmed_venues' : confirmed_venues, 'waiting_venues' : waiting_venues, 'deleted_venues': deleted_venues })


@login_required
def batches(request):
    from django.db.models.functions import Lower
    batchlist = Batch.objects.all().order_by(Lower('name'))
    return render(request,'db/batches.html', { 'batchlist' : batchlist })


def submit(request):
    infodict = {}
    infodict = request.POST.copy()
    for k in ['title','csrfmiddlewaretoken','submit']:
        if k in infodict.keys():
            del infodict[k]
    infodict["contactemail"] = infodict["contactemail"].strip()

    defaultContact = None
    defaultBatch = None
    if 'type' in infodict.keys():
        try:
            formInfo = FormInfo.objects.get(showType=infodict['type'])
            defaultContact = formInfo.defaultContact
            defaultBatch = formInfo.defaultBatch
        except:
            pass

    infojson = json.dumps(infodict)
    fest = FestivalInfo.objects.last()
    prop = Proposal(title=request.POST["title"], info=infojson, status=Proposal.WAITING, orgContact=defaultContact, festival=fest)
    prop.save()
    logInfo(request, "saved proposal {ID:%d} ('%s')" % (prop.id,prop.title))

    mail_to = infodict["contactemail"]
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( mail_to )
    except ValidationError:
        logInfo(request, "email '%s' is invalid" % mail_to)
        return render(request,'db/proposal_email_fail.html', {'address':mail_to})
    context = {'prop':prop, 'prop_info':infodict}
    mail_subject = "Buffalo Infringement Festival proposal '%s'" % prop.title
    mail_body = loader.render_to_string('db/submit_email.txt', context)
    if defaultContact:
        cc_list = [ defaultContact.user.email ]
    else:
        cc_list = None
    EmailMultiAlternatives(mail_subject, mail_body, None, [mail_to], cc=cc_list).send()
    if defaultBatch:
        defaultBatch.members.add(prop)
        logInfo(request, "Added {ID:%d} to batch {ID:%d}"%(prop.id,defaultBatch.id))
    return render(request,'db/proposal_submit.html', {})


@permission_required('db.can_schedule')
def reconfirm(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    infodict = json.loads(prop.info)
    mail_to = infodict["contactemail"]
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( mail_to )
    except ValidationError:
        logInfo(request, "email '%s' is invalid" % mail_to)
        return render(request,'db/proposal_email_fail.html', {'address':mail_to})
    context = {'prop':prop, 'prop_info':infodict}
    mail_subject = "Buffalo Infringement Festival proposal '%s'" % prop.title
    mail_body = loader.render_to_string('db/submit_email.txt', context)
    EmailMultiAlternatives(mail_subject, mail_body, None, [mail_to]).send()
    messages.success(request, 'Confirmation message sent')
    logInfo(request, "Sent confirmation email for {ID:%d} to '%s'" % (id,mail_to))
    return redirect('db-entity',id)


def setEntityOwner(e,u):
# need to: check if already owned by someone else, and change it (if allowed)
# note: this if-statement tries to prevent redundant entries, but if the user has some other permission (like VIEW), it will prevent changing ownership - must fix this
    if UserPermission.objects.filter(entity=e,bifuser=u).count() == 0:
        permit = UserPermission(entity=e, bifuser = u, permission=UserPermission.OWNER)
        permit.save()
        logInfo(None, "set owner of {ID:%d} to user {ID:%d}" % (e.id, u.id))
    else:
        logInfo(None, "tried to set owner of {ID:%d} to user {ID:%d} redundantly" % (e.id, u.id))


def confirmProposal(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    prop.status = Proposal.ACCEPTED     # Note that this will also undelete a deleted proposal - will leave it that way for now
    propinfodict = json.loads(prop.info)
    try:
        owner = User.objects.get(username=propinfodict["contactemail"])
        setEntityOwner(prop, owner.bifuser)
    except:
        logInfo(request, "exception while trying to setEntityOwner on {ID:%d}" % prop.id)
    prop.save()
    logInfo(request, "confirmed proposal {ID:%d}" % id)
    return render(request,'db/proposal_confirm.html', {'title':prop.title})


@permission_required('db.can_schedule')
def deleteProposal(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    prop.status = Proposal.DELETED
    prop.save()
    logInfo(request, "deleted proposal {ID:%d}" % id)
    messages.success(request, 'Proposal deleted')
    return redirect('db-entity',id=id)


@permission_required('db.can_schedule')
def undeleteProposal(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    prop.status = Proposal.ACCEPTED   # Note that we can't tell if proposal was previously ACCEPTED or WAITING; will just have to default to this, or redesign
    prop.save()
    logInfo(request, "undeleted proposal {ID:%d}" % id)
    messages.success(request, 'Proposal undeleted')
    return redirect('db-entity',id=id)


def proposalForm(request, template):
    days = ["July 26 (Thu)", "July 27 (Fri)","July 28 (Sat)","July 29 (Sun)","July 30 (Mon)","July 31 (Tue)","Aug 1 (Wed)","Aug 2 (Thu)","Aug 3 (Fri)","Aug 4 (Sat)","Aug 5 (Sun)"]
    times = [("8am", "8am-noon"), ("noon", "noon-4pm"), ("4pm", "4pm-8pm"), ("8pm", "8pm-midnight"), ("mid", "midnight-4am")]
    context = {'daylist':days, 'timelist':times}
    return render(request, template, context)


def musicForm(request):
    return proposalForm(request, 'db/music_form.html')

def theatreForm(request):
    return proposalForm(request, 'db/theatre_form.html')

def visualartForm(request):
    return proposalForm(request, 'db/visualart_form.html')

def danceForm(request):
    return proposalForm(request, 'db/dance_form.html')

def literaryForm(request):
    return proposalForm(request, 'db/literary_form.html')

def filmForm(request):
    return proposalForm(request, 'db/film_form.html')

def workshopForm(request):
    return proposalForm(request, 'db/workshop_form.html')

def venueForm(request):
    return proposalForm(request, 'db/venue_form.html')


@login_required
def editProposal(request, id):
    prop = get_object_or_404(Proposal, pk=id)
    if userCanEdit(request.user.bifuser, prop):
        infodict = json.loads(prop.info)
        infodict['title'] = prop.title
        template = "db/edit_%s_form.html" % infodict['type']
        days = ["July 26 (Thu)", "July 27 (Fri)","July 28 (Sat)","July 29 (Sun)","July 30 (Mon)","July 31 (Tue)","Aug 1 (Wed)","Aug 2 (Thu)","Aug 3 (Fri)","Aug 4 (Sat)","Aug 5 (Sun)"]
        times = [("8am", "8am-noon"), ("noon", "noon-4pm"), ("4pm", "4pm-8pm"), ("8pm", "8pm-midnight"), ("mid", "midnight-4am")]
        context = {'daylist':days, 'timelist':times, 'prop_info':infodict, 'prop_id':id}
        return render(request, template, context)
    else:
        return render(request, 'db/no_view.html')


@login_required
def update(request):
    id = int(request.POST["prop_id"])
    prop = get_object_or_404(Proposal, pk=id)
    infodict = {}
    infodict = request.POST.copy()
    for k in ['title','csrfmiddlewaretoken','submit','prop_id']:
        if k in infodict.keys():
            del infodict[k]
    infodict["contactemail"] = infodict["contactemail"].strip()
    infojson = json.dumps(infodict)
    prop.title = request.POST["title"]
    prop.info = infojson
    prop.save()
    logInfo(request, "updated proposal {ID:%d} ('%s')" % (prop.id,prop.title))
    return redirect('db-entity',id=id)


@permission_required('db.can_schedule')
def groupshow(request,id):
    groupshow = get_object_or_404(GroupShow, pk=id)
    alllistings = Listing.objects.filter(who__festival=groupshow.festival, where=groupshow.where, date=groupshow.date, installation=False).order_by('starttime')
    listings = []
    for l in alllistings:
        if max(l.starttime,groupshow.starttime) <= min(l.endtime,groupshow.endtime):
            listings.append(l)
    context = {'groupshow':groupshow, 'listings':listings}
    return render(request,'db/groupshow.html', context)

@permission_required('db.can_schedule')
def editGroupShow(request,id):
    groupshow = get_object_or_404(GroupShow, pk=id)
    context = {'groupshow':groupshow}
    return render(request,'db/edit_groupshow.html', context)

@permission_required('db.can_schedule')
def updateGroupShow(request):
    id = int(request.POST["groupshow_id"])
    g = get_object_or_404(GroupShow, pk=id)
    g.title = request.POST["title"]
    g.where = get_object_or_404(Venue, pk=int(request.POST["venue"]))
    g.starttime = int(request.POST['starttime'])
    g.endtime = int(request.POST['endtime'])
    g.date = request.POST["date"]
    g.shortdescription = request.POST["shortdescription"]
    g.description = request.POST["description"]
    g.save()
    messages.success(request,"updated groupshow: %s on %s at %s"%(g.title,g.date,g.where.name))
    logInfo(request, "updated groupshow {ID:%d}: %s at {ID:%d} on %s, %d to %d" % (g.id,g.title,g.where.id,g.date,g.starttime,g.endtime))
    return redirect('db-entity',id=id)

@permission_required('db.can_schedule')
def deleteGroupShow(request,id):
    groupshow = get_object_or_404(GroupShow, pk=id)
    title = groupshow.title
    venue = groupshow.where
    groupshow.delete()
    messages.success(request,"deleted groupshow %s"%title)
    logInfo(request,"deleted groupshow %s"%title)
    return redirect('db-entity',id=venue.id)

@permission_required('db.can_schedule')
def allGroupshows(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    groupshows = GroupShow.objects.filter(festival=fest).order_by(Lower('title'))
    return render(request,'db/all_groupshows.html', { 'groupshows' : groupshows })


def newAccount(request):
    return render(request,'db/new_account.html')


from django.contrib.auth.models import User

def createAccount(request):
    from django.db.utils import IntegrityError
    email = request.POST['email'].strip()
    password = request.POST['password']
    name = request.POST['name']
    try:
        djuser = User.objects.create_user(email, email, password, first_name=name)
    except IntegrityError:
        logError(request, "Tried to create duplicate account '%s'"%email)
        messages.error(request, "An account '%s' already exists" % email)
        return render(request, 'db/new_account.html')
    except:
        logError(request, "Unknown error creating account '%s'"%email)
        messages.error(request, 'Failed to create account')
        return render(request, 'db/new_account.html')
    bifuser = BIFUser.objects.create(user=djuser, phone='555-1212')
    claimProposals(bifuser)
    login(request, authenticate(username=email,password=password))
    logInfo(request, "Created new account '%s'"%email)
    return redirect('db-index')


def claimProposals(bifuser):
    email = bifuser.user.email.casefold()
    props = Proposal.objects.filter(info__icontains=email)
    for p in props:
        infodict = json.loads(p.info)
        if ('contactemail' in infodict.keys()) and (infodict['contactemail'].casefold() == email) and (not p.permit_who.filter(permission=UserPermission.OWNER)):
            setEntityOwner(p, bifuser)


def createVenue(request):
    infodict = {}
    infodict = request.POST.copy()
    for k in ['name','csrfmiddlewaretoken','submit']:
        if k in infodict.keys():
            del infodict[k]
    infodict["contactemail"] = infodict["contactemail"].strip()
    infojson = json.dumps(infodict)
    ven = Venue(name=request.POST["name"], info=infojson, status=Venue.WAITING)
    ven.save()
    logInfo(request, "saved venue {ID:%d} ('%s')" % (ven.id,ven.name))
    return redirect('db-index')


@permission_required('db.can_schedule')
def user(request,id):
    bifuser = get_object_or_404(BIFUser, pk=id)
    theuser = bifuser.user
    notes = bifuser.notes.all()
    proposals = bifuser.permit_what.filter(permission=UserPermission.OWNER,entity__entityType='proposal')
    context = {'theuser':theuser, 'bifuser': bifuser, 'proposals': proposals, 'notes':notes}
    return render(request,'db/user.html', context)


@permission_required('db.can_schedule')
def allUsers(request):
    from django.db.models.functions import Lower
    users = BIFUser.objects.all().order_by(Lower('user__email'))
    return render(request,'db/all_users.html', { 'users' : users })


@login_required
def venue(request,id):
    ven = get_object_or_404(Venue, pk=id)
    infodict = json.loads(ven.info)
    inbatches = ven.batches.all()
    batches = Batch.objects.all()
    notes = ven.notes.all()
    listings = ven.listing_set.filter(installation=False).order_by('date','starttime')
    installations = ven.listing_set.filter(installation=True).order_by('date','starttime')
    can_see = {}
    can_see['editlink'] = request.user.has_perm('db.can_schedule')
    can_see['schedule'] = request.user.has_perm('db.can_schedule')
    context = {'venue':ven, 'venue_info':infodict, 'inbatches':inbatches, 'batches':batches, 'notes':notes, 'listings':listings, 'installations':installations, 'can_see': can_see}
    return render(request,'db/venue.html', context)


@login_required
def venueSheet(request,id):
    ven = get_object_or_404(Venue, pk=id)
    infodict = json.loads(ven.info)
    listings = list(ven.listing_set.order_by('date','starttime'))
    groupshows = list(ven.groupshow_set.order_by('date','starttime'))
    allListings = []
    while len(groupshows) > 0 and len(listings) > 0:
        if groupshows[0].date <= listings[0].date and groupshows[0].starttime <= listings[0].starttime:
            allListings.append(groupshows.pop(0))
        else:
            allListings.append(listings.pop(0))
    while len(groupshows) > 0:
        allListings.append(groupshows.pop(0))
    while len(listings) > 0:
        allListings.append(listings.pop(0))
    context = {'venue':ven, 'venue_info':infodict, 'listings':allListings}
    return render(request,'db/venue_sheet.html', context)


@login_required
def editVenue(request, id):
    ven = get_object_or_404(Venue, pk=id)
    infodict = json.loads(ven.info)
    infodict['name'] = ven.name
    template = "db/edit_venue_form.html"
    days = ["July 26 (Thu)", "July 27 (Fri)","July 28 (Sat)","July 29 (Sun)","July 30 (Mon)","July 31 (Tue)","Aug 1 (Wed)","Aug 2 (Thu)","Aug 3 (Fri)","Aug 4 (Sat)","Aug 5 (Sun)"]
    context = {'daylist':days, 'venue_info':infodict, 'venue_id':id}
    return render(request, template, context)


@login_required
def updateVenue(request):
    id = int(request.POST["venue_id"])
    ven = get_object_or_404(Venue, pk=id)
    infodict = {}
    infodict = request.POST.copy()
    for k in ['title','csrfmiddlewaretoken','submit','venue_id']:
        if k in infodict.keys():
            del infodict[k]
    infodict["contactemail"] = infodict["contactemail"].strip()
    infojson = json.dumps(infodict)
    ven.name = request.POST["name"]
    ven.info = infojson
    ven.save()
    logInfo(request, "updated venue {ID:%d} ('%s')" % (ven.id,ven.name))
    return venue(request,id)


@permission_required('db.can_schedule')
def confirmVenue(request,id):
    ven = get_object_or_404(Venue, pk=id)
    ven.status = Venue.ACCEPTED
    ven.save()
    logInfo(request, "confirmed venue {ID:%d}" % id)
    return redirect('db-entity',id=id)


@permission_required('db.can_schedule')
def deleteVenue(request,id):
    ven = get_object_or_404(Venue, pk=id)
    ven.status = Venue.DELETED
    ven.save()
    logInfo(request, "deleted venue {ID:%d}" % id)
    messages.success(request, 'Venue deleted')
    return redirect('db-entity',id=id)


@permission_required('db.can_schedule')
def undeleteVenue(request,id):
    ven = get_object_or_404(Venue, pk=id)
    ven.status = Venue.ACCEPTED
    ven.save()
    logInfo(request, "undeleted venue {ID:%d}" % id)
    messages.success(request, 'Venue undeleted')
    return redirect('db-entity',id=id)


@permission_required('db.can_schedule')
def newBatch(request):
    return render(request,'db/new_batch.html')


@permission_required('db.can_schedule')
def createBatch(request):
    name = request.POST['name']
    description = request.POST['description']
    try:
        batch = Batch(name=name, description=description, festival=None)
    except:
        logError(request, "Unknown error creating batch '%s'"%name)
        messages.error(request, 'Failed to create batch')
        return render(request, 'db/new_batch.html')
    batch.save()
    logInfo(request, "Created new batch {ID:%d} '%s'"%(batch.id,name))
    return redirect('db-entity',id=batch.id)

def sortedBatchMembers(b):
    memberlist = []
    for e in b.members.all():
        memberlist.append({'id':e.id, 'name':entityName(e), 'status':entityStatus(e)})
    memberlist.sort(key=lambda m: m['name'].casefold())
    return memberlist

@permission_required('db.can_schedule')
def batch(request,id):
    b = get_object_or_404(Batch, pk=id)
    memberlist = sortedBatchMembers(b)
    props = Proposal.objects.all()
    context = {'batch':b, 'members':memberlist, 'proposals':props}
    return render(request,'db/batch.html', context)


@permission_required('db.can_schedule')
def addToBatch(request,batchid,memberid):
    b = get_object_or_404(Batch, pk=batchid)
    m = get_object_or_404(Entity, pk=memberid)
    b.members.add(m)
    logInfo(request, "Added {ID:%d} to batch {ID:%d}"%(memberid,batchid))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@permission_required('db.can_schedule')
def addToBatchForm(request):
    batchid = int(request.POST['batch'])
    memberid = int(request.POST['show'])
    return addToBatch(request,batchid,memberid)


@permission_required('db.can_schedule')
def removeFromBatch(request,batchid,memberid):
    b = get_object_or_404(Batch, pk=batchid)
    m = get_object_or_404(Entity, pk=memberid)
    b.members.remove(m)
    logInfo(request, "Removed {ID:%d} from batch {ID:%d}"%(memberid,batchid))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@permission_required('db.can_schedule')
def editBatch(request, id):
    b = get_object_or_404(Batch, pk=id)
    memberlist = []
    for e in b.members.all():
        memberlist.append({'id':e.id, 'name':entityName(e), 'status':entityStatus(e)})
    props = Proposal.objects.all()
    context = {'batch':b, 'members':memberlist, 'proposals':props}
    return render(request,'db/edit_batch.html', context)

@permission_required('db.can_schedule')
def updateBatch(request):
    id = int(request.POST["batch_id"])
    b = get_object_or_404(Batch, pk=id)
    b.name = request.POST['name']
    b.description = request.POST['description']
    b.save()
    logInfo(request, "updated batch {ID:%d} ('%s')" % (b.id,b.name))
    return redirect('db-entity',id=id)

@permission_required('db.can_schedule')
def batchStep(request,batchid,memberid,dir):
    b = get_object_or_404(Batch, pk=batchid)
    memberlist = sortedBatchMembers(b)
    i = 0
    while (i < len(memberlist)) and (memberlist[i]['id'] != memberid):
        i = i+1
    if i >= len(memberlist):
        returnID = memberid
    else:
        if dir > 0:
            returnID = memberlist[(i+1) % len(memberlist)]['id']
        else:
            returnID = memberlist[(i+len(memberlist)-1) % len(memberlist)]['id']
    return redirect('db-entity',id=returnID)

@permission_required('db.can_schedule')
def batchStepForward(request,batchid,memberid):
    return batchStep(request,batchid,memberid,1)

@permission_required('db.can_schedule')
def batchStepBackward(request,batchid,memberid):
    return batchStep(request,batchid,memberid,-1)


def getBatchEmailAddresses(b):
    addrs = []
    for e in b.members.all():
        if e.entityType == 'proposal' and e.proposal.status != e.proposal.DELETED:
            infodict = json.loads(e.proposal.info)
            addrs.append(infodict['contactemail'])
            addrs.append(infodict['secondcontactemail'])
    addrs.sort()
    uniqaddrs = []
    prev = ''
    for a in addrs:
        if a != prev:
            uniqaddrs.append(a)
            prev = a
    return uniqaddrs

@permission_required('db.can_schedule')
def batchEmails(request, id):
    b = get_object_or_404(Batch, pk=id)
    context = { 'batch': b, 'addrs': getBatchEmailAddresses(b) }
    return render(request,'db/batch_emails.html', context)

@permission_required('db.can_schedule')
def composeMailToBatch(request, id):
    b = get_object_or_404(Batch, pk=id)
    fest = FestivalInfo.objects.last()
    context = { 'batch': b, 'sender': request.user.email, 'defaultsubject': fest.name }
    return render(request,'db/batch_composemail.html', context)

@permission_required('db.can_schedule')
def mailBatch(request):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    id = int(request.POST["batch_id"])
    b = get_object_or_404(Batch, pk=id)
    sender = request.POST["sender"]
    addrs = getBatchEmailAddresses(b)
    validaddrs = []
    for a in addrs:
        try:
            validate_email(a)
            validaddrs.append(a)
        except ValidationError:
            logInfo(request, "email '%s' is invalid" % a)
            messages.error(request, "email '%s' is invalid" % a)
    mail_subject = request.POST["subject"]
    mail_body = request.POST["message"]
    EmailMultiAlternatives(mail_subject, mail_body, None, [sender], reply_to=[sender], bcc=validaddrs).send()
    logInfo(request, "sent mail to '%s'" % ', '.join(validaddrs))
    messages.success(request, "sent mail to %s" % ', '.join(validaddrs))
    return redirect('db-entity',id=id)


@permission_required('db.can_schedule')
def autoBatch(request, id):
    b = get_object_or_404(Batch, pk=id)
    allbatches = [{'id':0,'name':'[all proposals]'}]
    for batch in Batch.objects.all():
        allbatches.append({'id':batch.id, 'name':batch.name})
    context = { 'batch': b, 'allbatches': allbatches }
    return render(request, 'db/autobatch.html', context)

@permission_required('db.can_schedule')
def autoBatchRun(request):
    id = int(request.POST["batch_id"])
    b = get_object_or_404(Batch, pk=id)
    frombatchid = int(request.POST["frombatchid"])
    fest = FestivalInfo.objects.last()
    if frombatchid == 0:
        proposals = Proposal.objects.filter(festival=fest)
    else:
        frombatch = get_object_or_404(Batch, pk=frombatchid)
        proposals = frombatch.members.filter(entityType='proposal')
    field = request.POST['field']
    exactlabel = ('exactlabel' in request.POST.keys()) and (request.POST['exactlabel'] == '1')
    value = request.POST['value']
    exactvalue = ('exactvalue' in request.POST.keys()) and (request.POST['exactvalue'] == '1')
    for p in proposals:
        infodict = json.loads(p.proposal.info)
        for label in infodict.keys():
            if stringMatch(field,label,exactlabel) and stringMatch(value,infodict[label],exactvalue):
                b.members.add(p)
    return redirect('db-entity',id)

def stringMatch(needle,haystack,exact):
    n = needle.casefold()
    h = haystack.casefold()
    if exact:
        return n == h
    else:
        return n in h


@permission_required('db.can_schedule')
def deleteBatch(request, id):
    b = get_object_or_404(Batch, pk=id)
    msg = 'Deleted batch "%s"' % b.name
    logmsg = 'deleted batch {ID:%d}' % b.id
    b.delete()
    messages.success(request, msg)
    logInfo(request, logmsg)
    return redirect('db-batches')


@permission_required('db.can_schedule')
def newSpreadsheet(request):
    batches = Batch.objects.all()
    fest = FestivalInfo.objects.last()
    forminfos = FormInfo.objects.all()
    fielddict = {}
    for fi in forminfos:
        fields = json.loads(fi.fields)
        for f in fields:
            fielddict[f[0]] = f[1]
    fieldlist = list(fielddict.items())
    fieldlist.sort()
    for i in range(1,fest.numberOfDays+1):
        for t in ['8am', 'noon', '4pm', '8pm', 'mid']:
            s = 'available_day%d_%s' % (i,t)
            fieldlist.append( (s,s) )
    context = {'batches':batches, 'fields':fieldlist}
    return render(request,'db/new_spreadsheet.html', context)


@permission_required('db.can_schedule')
def createSpreadsheet(request):
    name = request.POST['name']
    fest = FestivalInfo.objects.last()
    description = request.POST['description']
    batchid = int(request.POST['batch'])
    frombatch = get_object_or_404(Batch, pk=batchid)
    columnname = request.POST.getlist('columnname[]')
    propfield = request.POST.getlist('propfield[]')
    default = request.POST.getlist('default[]')
    cols = []
    for c in zip(columnname, propfield, default):
        cols.append([c[0],c[1],c[2]])
    colsjson = json.dumps(cols)
    try:
        spreadsheet = Spreadsheet(name=name, festival=fest, description=description, frombatch=frombatch, columns=colsjson)
    except:
        logError(request, "Unknown error creating spreadsheet '%s'"%name)
        messages.error(request, 'Failed to create spreadsheet')
        return render(request, 'db/new_spreadsheet.html')
    spreadsheet.save()
    messages.success(request, 'created spreadsheet "%s"'%name)
    logInfo(request, "Created new spreadsheet {ID:%d} '%s'"%(spreadsheet.id,name))
    for e in frombatch.members.all():
        values = []
        for c in cols:
            if c[1] != "":
                values.append(getEntityField(e,c[1]))
            else:
                values.append(c[2])
        r = SpreadsheetRow(spreadsheet=spreadsheet, entity=e, data=json.dumps(values))
        r.save()
    return redirect('db-entity',id=spreadsheet.id)


def getEntityField(e,label):
    infodict = {}
    if e.entityType == 'proposal':
        infodict = json.loads(e.proposal.info)
    elif e.entityType == 'venue':
        infodict = json.loads(e.venue.info)
    if label in infodict.keys():
        return infodict[label]
    else:
        return ""

@permission_required('db.can_schedule')
def allSpreadsheets(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    spreadsheets = Spreadsheet.objects.filter(festival=fest).order_by(Lower('name'))
    return render(request,'db/all_spreadsheets.html', { 'spreadsheets' : spreadsheets })


@permission_required('db.can_schedule')
def spreadsheetCounts(request,id):
    from datetime import timedelta
    sheet = get_object_or_404(Spreadsheet, pk=id)
    columns = [c[0] for c in json.loads(sheet.columns)]
    daylist = [(sheet.festival.startDate + timedelta(days=d)) for d in range(0,sheet.festival.numberOfDays)]
    rows = []
    for r in sheet.rows.all():
        vals = json.loads(r.data)
        if r.entity.entityType == 'proposal':
            listings = r.entity.proposal.listing_set.order_by('date')
            numlistings = len(listings)
            daycountDict = {}
            for d in daylist:
                daycountDict[d] = 0
            for l in listings:
                daycountDict[l.date] += 1
            daycount = [daycountDict[d] for d in daylist]
        else:
            numlistings = 0
        rows.append({'title':entityName(r.entity), 'id':r.entity.id, 'values':vals, 'numlistings':numlistings, 'daycount':daycount})
    context = {'spreadsheet':sheet, 'columns':columns, 'rows':rows, 'daylist':daylist, 'showcounts':1}
    return render(request,'db/spreadsheet.html',context)

@permission_required('db.can_schedule')
def spreadsheet(request,id):
    sheet = get_object_or_404(Spreadsheet, pk=id)
    columns = [c[0] for c in json.loads(sheet.columns)]
    rows = []
    for r in sheet.rows.all():
        vals = json.loads(r.data)
        rows.append({'title':entityName(r.entity), 'id':r.entity.id, 'values':vals})
    context = {'spreadsheet':sheet, 'columns':columns, 'rows':rows}
    return render(request,'db/spreadsheet.html',context)


@login_required
def editEntity(request,id):
    e = get_object_or_404(Entity, pk=id)
    if userCanEdit(request.user.bifuser, e):
        if e.entityType == 'proposal':
            return editProposal(request,id)
        elif e.entityType == 'venue':
            return editVenue(request,id)
        elif e.entityType == 'batch':
            return editBatch(request,id)
        elif e.entityType == 'listing':
            return editListing(request,id)
        elif e.entityType == 'groupshow':
            return editGroupShow(request,id)
        else:
            return render(request, 'db/entity_error.html', { 'type': e.entityType })
    else:
        return render(request, 'db/no_edit.html')


@login_required
def entity(request,id):
    e = get_object_or_404(Entity, pk=id)
    if userCanView(request.user.bifuser, e):
        if e.entityType == 'proposal':
            return proposal(request,id)
        elif e.entityType == 'batch':
            return batch(request,id)
        elif e.entityType == 'venue':
            return venue(request,id)
        elif e.entityType == 'spreadsheet':
            return spreadsheet(request,id)
        elif e.entityType == 'bifuser':
            return user(request,id)
        elif e.entityType == 'groupshow':
            return groupshow(request,id)
        else:
            return render(request, 'db/entity_error.html', { 'type': e.entityType })
    else:
        return render(request, 'db/no_view.html')


def userCanView(u, e):
    if u.user.has_perm("db.can_schedule"):
        return True
    perms = e.permit_who.filter(bifuser=u)
    for p in perms:
        if p.permission != UserPermission.NONE:
            return True
    return False


def userCanEdit(u, e):
    if u.user.has_perm("db.can_schedule"):
        return True
    perms = e.permit_who.filter(bifuser=u)
    for p in perms:
        if p.permission in [UserPermission.OWNER, UserPermission.EDIT]:
            return True
    return False


@login_required
def proposal(request,id):
    prop = get_object_or_404(Proposal, pk=id)
    infodict = json.loads(prop.info)
    forminfo = FormInfo.objects.get(showType=infodict['type'])
    formfields = json.loads(forminfo.fields)
    fieldlist = []
    for f in formfields:
        if f[0] in infodict.keys():
            fieldlist.append([f[1], infodict[f[0]]])
    inbatches = prop.batches.all()
    batches = Batch.objects.all()
    notes = prop.notes.all()
    listings = prop.listing_set.order_by('date','starttime')
    owner = prop.permit_who.filter(permission=UserPermission.OWNER).first()
    if owner: owner = owner.bifuser
    can_see = {}
    can_see['editlink'] = request.user.has_perm('db.can_schedule') or owner == request.user.bifuser
    can_see['schedule'] = request.user.has_perm('db.can_schedule') or owner == request.user.bifuser
    context = {'prop':prop, 'prop_info':infodict, 'inbatches':inbatches, 'batches':batches, 'notes':notes, 'fieldlist':fieldlist, 'listings':listings, 'owner':owner, 'can_see': can_see}
    return render(request,'db/proposal.html', context)


def entityName(e):
    if e.entityType == 'proposal':
        return e.proposal.title
    elif e.entityType == 'batch':
        return e.batch.name
    elif e.entityType == 'venue':
        return e.venue.name
    elif e.entityType == 'bifuser':
        return e.bifuser.user.email
    elif e.entityType == 'groupshow':
        return e.groupshow.title
    else:
        return "%s %d" % (e.entityType,e.id)


def entityStatus(e):
    if e.entityType == 'proposal':
        return e.proposal.status
    elif e.entityType == 'venue':
        return e.venue.status
    else:
        return 1


@permission_required('db.can_schedule')
def addNote(request):
    entityid = int(request.POST['entity'])
    notetext = request.POST['note']
    try:
        creator = request.user.bifuser
    except:
        creator = None
    try:
        note = Note(creator=creator, notetext=notetext)
    except:
        logError(request, "Unknown error creating note '%s'"%notetext)
        return redirect('db-index')
    note.save()
    e = get_object_or_404(Entity, pk=entityid)
    note.attachedTo.add(e)
    if creator:
        setEntityOwner(note, creator)
    logInfo(request, "Created new note {ID:%d} attached to {ID:%s} '%s'"%(note.id,entityid,notetext))
    return redirect('db-entity',id=entityid)


@permission_required('db.can_schedule')
def scheduleProposal(request):
    from datetime import timedelta
    proposal = get_object_or_404(Proposal, pk=int(request.POST['proposal']))
    venue = get_object_or_404(Venue, pk=int(request.POST['venue']))
    venuenote = request.POST['venuenote'] if 'venuenote' in request.POST.keys() else ''
    starttime = int(request.POST['starttime'])
    endtime = int(request.POST['endtime'])
    installation = 'installation' in request.POST.keys()
    listnote = request.POST['note'] if 'note' in request.POST.keys() else ''
    fest = FestivalInfo.objects.last()
    for d in range(0,fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        if day.isoformat() in request.POST.keys():
            messages.success(request,'Scheduled %s on %s at %s'%(proposal.title,day.isoformat(),venue.name))
            listing = Listing(who=proposal, where=venue, venuenote=venuenote, date=day, starttime=starttime, endtime=endtime, installation=installation, listingnote=listnote)
            listing.save()
            logInfo(request, "listed {ID:%d} at {ID:%d} on %s at %d" % (proposal.id,venue.id,day,starttime))
    return redirect('db-entity',id=proposal.id)


@permission_required('db.can_schedule')
def scheduleGroupShow(request):
    from datetime import timedelta
    venue = get_object_or_404(Venue, pk=int(request.POST['venue']))
    starttime = int(request.POST['starttime'])
    endtime = int(request.POST['endtime'])
    title = request.POST['title']
    fest = FestivalInfo.objects.last()
    for d in range(0,fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        if day.isoformat() in request.POST.keys():
            messages.success(request,'scheduled groupshow %s on %s at %s'%(title,day.isoformat(),venue.name))
            groupshow = GroupShow(title=title, where=venue, date=day, starttime=starttime, endtime=endtime, festival=fest)
            groupshow.save()
            logInfo(request, "created groupshow {ID:%d} at {ID:%d} on %s at %d" % (groupshow.id,venue.id,day,starttime))
    return redirect('db-entity',id=venue.id)


@permission_required('db.can_schedule')
def editListing(request,id):
    listing = get_object_or_404(Listing, pk=id)
    listing.showtitle = listing.who.title
    listing.venuename = listing.where.name
    context = {'listing':listing}
    return render(request,'db/edit_listing.html', context)

@permission_required('db.can_schedule')
def updateListing(request):
    id = int(request.POST["listing_id"])
    l = get_object_or_404(Listing, pk=id)
    l.where = get_object_or_404(Venue, pk=int(request.POST["venue"]))
    l.venuenote = request.POST['venuenote'] if 'venuenote' in request.POST.keys() else ''
    l.starttime = int(request.POST['starttime'])
    l.endtime = int(request.POST['endtime'])
    l.listnote = request.POST['note'] if 'note' in request.POST.keys() else ''
    l.date = request.POST["date"]
    l.installation = 'installation' in request.POST.keys()
    l.save()
    messages.success(request,"Updated listing: %s on %s at %s"%(l.who.title,l.date,l.where.name))
    logInfo(request, "updated listing {ID:%d}: {ID:%d} at {ID:%d} on %s, %d to %d" % (l.id,l.who.id,l.where.id,l.date,l.starttime,l.endtime))
    return redirect('db-entity',id=int(request.POST["return_entity"]))

@permission_required('db.can_schedule')
def deleteListing(request,id):
    listing = get_object_or_404(Listing, pk=id)
    proposal = listing.who
    messages.success(request,'Deleted listing of %s on %s at %s'%(proposal.title,listing.date.isoformat(),listing.where.name))
    logInfo(request, 'Deleted listing of {ID:%d} on %s at {ID:%d}'%(proposal.id,listing.date.isoformat(),listing.where.id))
    listing.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@permission_required('db.can_schedule')
def cancelListing(request,id):
    listing = get_object_or_404(Listing, pk=id)
    listing.cancelled = True
    listing.save()
    messages.success(request,'Cancelled listing of %s on %s at %s'%(listing.who.title,listing.date.isoformat(),listing.where.name))
    logInfo(request, 'Cancelled listing of {ID:%d} on %s at {ID:%d}'%(listing.who.id,listing.date.isoformat(),listing.where.id))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@permission_required('db.can_schedule')
def uncancelListing(request,id):
    listing = get_object_or_404(Listing, pk=id)
    listing.cancelled = False
    listing.save()
    messages.success(request,'Uncancelled listing of %s on %s at %s'%(listing.who.title,listing.date.isoformat(),listing.where.name))
    logInfo(request, 'Uncancelled listing of {ID:%d} on %s at {ID:%d}'%(listing.who.id,listing.date.isoformat(),listing.where.id))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@permission_required('db.can_schedule')
def calendar(request):
    from datetime import timedelta
    from django.db.models.functions import Lower
    days = []
    fest = FestivalInfo.objects.last()
    for d in range(0,fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        listingList = []
        listings = Listing.objects.filter(date=day,installation=False).order_by('starttime',Lower('where__name'))
        installations = Listing.objects.filter(date=day,installation=True).order_by('starttime',Lower('where__name'))
        days.append({'date': day.strftime("%A, %B %-d"), 'listings': listings, 'installations':installations})
    return render(request, 'db/calendar.html', context={'days':days})

@permission_required('db.can_schedule')
def brochure(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    forminfos = FormInfo.objects.filter(festival=fest)
    genredict = {}
    for fi in forminfos:
        genredict[fi.showType] = {'name':fi.showType, 'proposals': []}
    genredict['groupshows'] = {'name': "group shows", 'proposals': []}
    proposals = Proposal.objects.filter(festival=fest,status=Proposal.ACCEPTED).order_by(Lower('title'))
    for prop in proposals:
        listings = prop.listing_set.order_by('date','starttime')
        infodict = json.loads(prop.info)
        shortdesc = infodict['description_short'] if 'description_short' in infodict.keys() else ''
        if len(shortdesc) > 144:
            shortdesc = shortdesc[:140] + "..."
        url = infodict['website'] if 'website' in infodict.keys() else ''
        if len(listings) > 0:
            genredict[infodict['type']]['proposals'].append({'title':prop.title, 'description':shortdesc, 'url': url, 'listings':listings})
    groupshows = GroupShow.objects.filter(festival=fest).order_by(Lower('title'))
    for g in groupshows:
        alllistings = Listing.objects.filter(who__festival=fest, where=g.where, date=g.date, installation=False).order_by('starttime')
        performers = []
        for l in alllistings:
            if max(l.starttime,g.starttime) <= min(l.endtime,g.endtime):
                performers.append(l.who.title)
        description = g.shortdescription + "<br>Featuring: " + ', '.join(performers)
        genredict['groupshows']['proposals'].append({'title':g.title, 'description':description, 'url':'', 'listings':[g]})
    genres = genredict.values()
    return render(request, 'db/brochure.html', context={'genres':genres})


@permission_required('db.can_schedule')
def searchProposals(request):
    from django.db.models.functions import Lower
    if 'searchterm' in request.POST.keys():
        fest = FestivalInfo.objects.last()
        searchterm = request.POST['searchterm'].casefold()
        props = Proposal.objects.filter(festival=fest,info__icontains=searchterm).order_by(Lower('title'))
    else:
        props = []
    return render(request,'db/search.html', { 'proposals' : props })


import logging

def logInfo(request,message):
    logger = logging.getLogger(__name__)
    logger.info(logMessage(request,message))


def logError(request,message):
    logger = logging.getLogger(__name__)
    logger.error(logMessage(request,message))


def logMessage(request,message):
    from datetime import datetime
    username = 'anonymous-user'
    if request and hasattr(request,'user') and hasattr(request.user,'username') and request.user.username != '':
        username = request.user.username
    ipaddr = 'ip-unknown'
    if request:
        ipaddr = request.META.get('REMOTE_ADDR')
    return "%s %s %s: %s" % (datetime.now().strftime("%Y-%m-%d %X"),ipaddr,username, message)


import re

def viewLogLink(match):
    from django.utils.html import format_html
    from django.urls import reverse
    id = int(match.group(1))
    e = Entity.objects.filter(pk=id)
    if e:
        return format_html('<a href="{}">{}</a>', reverse('db-entity',kwargs={'id':e[0].id}), entityName(e[0]))
    else:
        return match.group()

@permission_required('db.can_schedule')
def viewLog(request):
    from django.conf import settings
    from django.utils.html import format_html, mark_safe
    f = open(settings.LOGGING['handlers']['file']['filename'], 'r')
    lines = f.readlines()
    numlines = int(request.POST['numlines']) if 'numlines' in request.POST.keys() else 100
    regex = re.compile(r'{ID:([0-9]+)}')
    if 'searchterm' in request.POST.keys():
        outlines = []
        searchterm = request.POST['searchterm'].casefold()
        for l in reversed(lines):
            if searchterm in l.casefold():
                outlines.insert(0,mark_safe(regex.sub(viewLogLink,l)))
            else:
                temp = regex.sub(viewLogLink,l)
                if searchterm in temp.casefold():
                    outlines.insert(0,mark_safe(temp))
            if len(outlines) >= numlines:
                break
    else:
        searchterm = ''
        outlines = [mark_safe(regex.sub(viewLogLink,l)) for l in lines[-numlines:]]
    context = {'lines':outlines, 'searchterm':searchterm, 'numlines':numlines}
    return render(request, 'db/log.html', context)

