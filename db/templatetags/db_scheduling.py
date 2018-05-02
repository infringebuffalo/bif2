from django import template
from db.models import *
from django.utils.html import format_html
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

#<td colspan="6"></td></tr>



@register.simple_tag
def db_venueMenu():
    fest = FestivalInfo.objects.last()
    venues = Venue.objects.all()
    retval = format_html('<select name="venue">')
    for v in venues:
        retval += format_html('<option value="{}">{}</option>', v.id, v.name)
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
            retval += format_html('<option value="{}"{}>{}</option>', t, 'selected' if t==default else '', timeToString(t))
    t = '%02d00' % endHour
    retval += format_html('<option value="{}"{}>{}</option>', t, 'selected' if t==default else '', timeToString(t))
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
def db_listingRow(listing):
    venuenote = ' (%s)'%listing.venuenote if listing.venuenote != '' else ''
    retval = format_html('<tr><tr><td>{}</td><td>{}-{}</td><td>{}{}</td>',listing.date.strftime("%a, %b %d"),timeToString(listing.starttime),timeToString(listing.endtime),listing.where.name,venuenote)
#    if listing.listingnote != '':
#        retval += format_html('<td>{}</td>',listing.listingnote)
    retval += format_html('</tr>\n')
    return retval

