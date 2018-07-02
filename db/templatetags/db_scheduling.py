from django import template
from db.models import *
from django.utils.html import format_html, mark_safe
from datetime import *

register = template.Library()

@register.simple_tag
def db_smallCalendar():
    fest = FestivalInfo.objects.last()
    retval = format_html('<table rules="all">\n<tr><th>S<th>M<th>T<th>W<th>T<th>F<th>S</tr>\n<tr>')
    if fest.startDate.isoweekday() < 7:
        retval += format_html('<td colspan="{}"></td>\n', fest.startDate.isoweekday())
    for d in range(0, fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        if day.isoweekday() == 7:
            retval += format_html('</tr><tr>')
        retval += format_html('<td class="calEntry" data-bifday="{}"><input type="checkbox" name="{}" value="1" />{}</td>\n', d, day.isoformat(), day.day)
    retval += format_html('</table>')
    return retval

@register.simple_tag
def db_horizCalendar():
    fest = FestivalInfo.objects.last()
    retval = format_html('<table>\n<tr>\n')
    if fest.startDate.isoweekday() < 7:
        retval += format_html('<td colspan="{}"></td>\n', fest.startDate.isoweekday())
    for d in range(0, fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        bg = "background: lightblue" if day.isoweekday() in [6,7] else ""
        retval += format_html('<td class="calEntry" data-bifday="{}" style="{}"><input type="checkbox" name="{}" value="1" /><br>{}</td>\n', d, bg, day.isoformat(), day.day)
    retval += format_html('</tr></table>')
    return retval


@register.simple_tag
def db_dateMenu(**kwargs):
    fest = FestivalInfo.objects.last()
    if 'defaultDate' in kwargs:
        defaultDate = kwargs['defaultDate']
    else:
        defaultDate = ''
    retval = format_html('<select name="date">')
    for d in range(0, fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        retval += format_html('<option value="{}" {}>{}</option>', day, 'selected' if day.isoformat()==defaultDate else '', day.strftime('%a %b %d'))
    retval += format_html('</select>')
    return retval


@register.simple_tag
def db_venueMenu(**kwargs):
    fest = FestivalInfo.objects.last()
    if 'defaultVenue' in kwargs:
        defaultVenue = int(kwargs['defaultVenue'])
    else:
        defaultVenue = 0
    venueObjects = Venue.objects.filter(status=Venue.ACCEPTED)
    venues = [(v.name, v.id) for v in venueObjects]
    venues.sort(key=lambda v: v[0].casefold())
    retval = format_html('<select name="venue">')
    for v in venues:
        retval += format_html('<option value="{}" {}>{}</option>', v[1], 'selected' if v[1]==defaultVenue else '', v[0])
    retval += format_html('</select>')
    return retval


@register.simple_tag
def db_proposalMenu():
    fest = FestivalInfo.objects.last()
    proposalObjects = Proposal.objects.filter(status=Proposal.ACCEPTED,festival=fest).all()
    proposals = [(p.title, p.id) for p in proposalObjects]
    proposals.sort(key=lambda p: p[0].casefold())
    retval = format_html('<select name="proposal">')
    for p in proposals:
        name = p[0]
        if len(name) > 32:
            name = name[:29] + "..."
        elif name == "":
            name = "NEEDS A TITLE"
        retval += format_html('<option value="{}">{}</option>', p[1], name)
    retval += format_html('</select>')
    return retval


@register.simple_tag
def db_timeMenu(startHour,endHour,name,*args,**kwargs):
    startHour = int(startHour)
    endHour = int(endHour)
    if 'default' in kwargs:
        default = str(kwargs['default'])
    else:
        default = '1900'
    retval = format_html('<select name="{}">',name)
    for hour in range(startHour, endHour):
        for minute in [0, 15, 30, 45]:
            t = '%02d%02d' % (hour, minute)
            retval += format_html('<option value="{}" {}>{}</option>', t, 'selected' if t==default else '', timeToString(t))
    t = '%02d00' % endHour
    retval += format_html('<option value="{}" {}>{}</option>', t, 'selected' if t==default else '', timeToString(t))
    retval += format_html('</select>')
    return retval


def timeToString(t):
    t = int(t)
    if t == 1200:
        return 'noon'
    elif t == 2400:
        return 'midnight'
    h = int(t/100)
    m = t - h*100
    h = h % 24
    if h >= 12:
        suffix = 'pm'
        if h > 12:
            h = h - 12
    else:
        suffix = 'am'
        if h == 0:
            h = 12
    if m != 0:
        return '%d:%02d%s' % (h,m,suffix)
    else:
        return '%d%s' % (h,suffix)


@register.simple_tag
def db_time(t):
    return format_html(timeToString(t))


@register.simple_tag
def db_listingRow(listing,proposal,venue):
    from django.urls import reverse
    venuenote = ' (%s)'%listing.venuenote if listing.venuenote != '' else ''
    tdflags = mark_safe(' class="cancelled"') if listing.cancelled else ""
    retval = format_html('<tr>')
    groupshows = GroupShow.objects.filter(where=venue,date=listing.date) if venue else []
    groupshowlinks = []
    for g in groupshows:
        if max(listing.starttime,g.starttime) <= min(listing.endtime,g.endtime):
            groupshowlinks.append(format_html('<a href="{}">{}</a> ',reverse('db-entity',kwargs={'id':g.id}),g.title))
    if len(groupshowlinks) > 0:
        retval += format_html('<td class="groupshow">')
        for g in groupshowlinks:
            retval += g
    else:
        retval += format_html('<td></td>')
    retval += format_html('<td{}>{}</td>',tdflags,listing.date.strftime("%a, %b %d"))
    if listing.installation:
        retval += format_html('<td{}>installation</td>',tdflags)
    else:
        retval += format_html('<td{}>{}-{}</td>',tdflags,timeToString(listing.starttime),timeToString(listing.endtime))
    if not proposal:
        retval += format_html('<td{}><a href="{}">{}</a>{}</td>',tdflags,reverse('db-entity',kwargs={'id':listing.who.id}),listing.who.title,venuenote if venue else '')
    if not venue:
        retval += format_html('<td{}><a href="{}">{}</a>{}</td>',tdflags,reverse('db-entity',kwargs={'id':listing.where.id}),listing.where.name,venuenote)
    retval += format_html('<td><a href="{}"><i class="material-icons">edit</i></a></td>',reverse('db-editEntity',kwargs={'id':listing.id}))
    retval += format_html('<td><a href="{}" onclick="return confirm(\'Are you sure you want to permanently delete this listing?\');"><i class="material-icons">delete_forever</i></a></td>',reverse('db-deleteListing',kwargs={'id':listing.id}))
    if listing.cancelled:
        retval += format_html('<td><a href="{}"><i class="material-icons">restore</i></a></td>',reverse('db-uncancelListing',kwargs={'id':listing.id}))
    else:
        retval += format_html('<td><a href="{}"><i class="material-icons">cancel</i></a></td>',reverse('db-cancelListing',kwargs={'id':listing.id}))
#    if listing.listingnote != '':
#        retval += format_html('<td>{}</td>',listing.listingnote)
    retval += format_html('</tr>\n')
    return retval

@register.simple_tag
def db_brochurelistingRow(listing):
    from django.urls import reverse
    venuenote = ' (%s)'%listing.venuenote if listing.venuenote != '' else ''
    spanflags = mark_safe(' class="cancelled"') if listing.cancelled else ""
    retval = format_html('<span{}>',spanflags)
    retval += format_html('{} ',listing.date.strftime("%a, %b %d"))
    if listing.installation:
        retval += format_html('installation ')
    else:
        retval += format_html('{}-{} ',timeToString(listing.starttime),timeToString(listing.endtime))
    retval += format_html('{} {} ',listing.where.name,venuenote)
    retval += format_html('</span>\n')
    return retval


venuesheet_prevlisting = None

@register.simple_tag
def db_venuesheetlisting(listing):
    from json import loads
    global venuesheet_prevlisting
    infodict = loads(listing.who.info)
    retval = format_html('<tr>\n')
    if not venuesheet_prevlisting or venuesheet_prevlisting.date != listing.date:
        retval += format_html('<td colspan="2"><b>{}</b></td>\n</tr>\n<tr>\n',listing.date.strftime("%a, %b %d"))
    if listing.installation:
        retval += format_html('<td valign="top">installation</td>\n')
    else:
        retval += format_html('<td valign="top">{}-{}</td>\n',timeToString(listing.starttime),timeToString(listing.endtime))
    retval += format_html('<td><b>{}</b><br>{}<br>email: {}<br>phone: {}<br>social media: {}<br>best contact method: {}</td>\n',listing.who.title,infodict['contactname'],infodict['contactemail'],infodict['contactphone'],infodict['contactfacebook'],infodict['bestcontactmethod'])
    retval += format_html('</tr>\n')
    venuesheet_prevlisting = listing
    return retval


@register.simple_tag
def db_entityFromURL(url):
    from urllib.parse import urlparse
    from django.urls import resolve
    r = resolve(urlparse(url).path)
    retval = format_html('{}',r.kwargs['id'])
    return retval
