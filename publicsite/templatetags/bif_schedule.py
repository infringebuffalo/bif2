from django import template
from db.models import *
from django.utils.html import format_html, mark_safe
from datetime import *

register = template.Library()


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
def bif_listingRow(listing,proposal,venue,user=None):
    from django.urls import reverse
    venuenote = ' (%s)'%listing.venuenote if listing.venuenote != '' else ''
    tdflags = mark_safe(' class="cancelled"') if listing.cancelled else ""
    retval = format_html('<tr>')
    groupshows = GroupShow.objects.filter(where=listing.where,date=listing.date)
    groupshowlinks = []
    for g in groupshows:
        if max(listing.starttime,g.starttime) <= min(listing.endtime,g.endtime):
            groupshowlinks.append(format_html('<a href="{}">{}</a> ',reverse('entityInfo',kwargs={'id':g.id}),g.title))
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
        retval += format_html('<td{}><a href="{}">{}</a>{}</td>',tdflags,reverse('entityInfo',kwargs={'id':listing.who.id}),listing.who.title,venuenote if venue else '')
    if not venue:
        retval += format_html('<td{}><a href="{}">{}</a>{}</td>',tdflags,reverse('entityInfo',kwargs={'id':listing.where.id}),listing.where.name,venuenote)
    retval += format_html('</tr>\n')
    return retval

