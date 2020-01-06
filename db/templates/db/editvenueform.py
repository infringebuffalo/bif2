#!/usr/bin/python

all_required_fields = [ "contactname", "contactemail", "name" ]

def startPage(formtitle,formtype=None,requiredfields=None):
    global all_required_fields
    if not formtype:
        formtype = formtitle.lower()
    if requiredfields:
        all_required_fields += requiredfields
    requiredfields_str = ', '.join(map(lambda x:'"%s"'%x,all_required_fields))
    print("""{%% extends "base_generic.html" %%}

{%% block title %%}Buffalo Infringement Festival %s{%% endblock %%}

{%% block style %%}
<style>
.avail td { padding: 10px }
.avail tr:nth-child(odd) { background-color: #f0f0f0 }
.alternategrey tr:nth-child(odd) { background-color: #f0f0f0 }
.alternategrey td { padding-top: 6px; padding-bottom: 6px }
</style>
{%% endblock %%}

{%% block scripts %%}

<script type="text/javascript">
function validateForm()
{
var f = document.forms["proposalform"];
var fields = [ %s ];
var okay = true;
for (i=0; i < fields.length; i++)
    if ((f[fields[i]].value == null) || (f[fields[i]].value == ""))
        okay = false;
if (!okay)
    {
    alert("All fields marked with * must be filled out before this proposal can be submitted");
    return false;
    }
else
    return true;
}

function hoverFunc(event)
  {
  $(this).parent().find(".helptext").fadeIn()
  }

function unhoverFunc(event)
  {
  $(this).parent().find(".helptext").fadeOut()
  }

function readyFunc()
  {
  $(".questionmark").hover(hoverFunc,unhoverFunc)
  $(".questionmark").parent().find(".helptext").fadeOut()
  }
$(document).ready(readyFunc)
</script>

{%% endblock %%}

{%% block content %%}

{%% load static %%}

<h2>Editing %s proposal </h2>

<div style="background:#f88; text-align:center">Note: all fields marked with * must be filled in before this form is submitted.</div>

<form method="POST" action="{%% url 'db-updateVenue' %%}" name="proposalform" onsubmit="return validateForm()">
{%% csrf_token %%}

<input type="hidden" name="venue_id" value="{{ venue_id }}" />
<input type="hidden" name="type" value="%s" />

<div class='venueForm'>
<table class="alternategrey">""" % (formtitle, requiredfields_str, formtitle, formtype))


def availabilitySection():
    print("""<div class="projectForm">
<h3>Availability</h3>
<table class="avail">
""")
    for daynum in range(0,11):
        print("<tr><th>{{daylist.%d}}</th>" % daynum)
        inputname = "available_day%d" % (daynum+1)            
        print("""<td>
<input type="text" name="%s" value="{{ venue_info.%s }}">
</td>""" % (inputname,inputname))
        print("</tr>")
    print("</table></div>")

def endPage():
    print("""<input type="Submit" name="submit" value="Update" />
</p>
</form>

{% endblock %}""")


formnames = []
def checkName(name):
    if name in formnames:
        raise AssertionError("duplicate name '%s'" % name)
    formnames.append(name)

    
def textInput(label,name,placeholder=''):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><input type='text' name='%s' size='60' placeholder='%s' value='{{ venue_info.%s }}'/></td>" % (name,placeholder,name))
    print("</tr>")

def textarea(label,name,rows=4,placeholder=''):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><textarea name='%s' rows='%d' cols='60' placeholder='%s'>{{ venue_info.%s }}</textarea></td>" % (name,rows,placeholder,name))
    print("</tr>")

def yesnoInput(label,name,default='y'):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'><option value='Y'{%% if venue_info.%s == \"Y\" %%} selected{%% endif %%}>Yes</option><option value='N'{%% if venue_info.%s != \"Y\" %%} selected{%% endif %%}>No</option></select></td>" % (name,name,name))
    print("</tr>")

def menuInput(label,name,options):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'>" % name)
    for o in options:
        print("<option value='%s'{%% if venue_info.%s == \"%s\" %%} selected{%% endif %%}>%s</option>" % (o,name,o,o))
    print("</select></td>")
    print("</tr>")



startPage("Venue")
textInput("Venue name", "name")
textInput("Owner", "ownername")
textInput("Address", "address")
textInput("Website", "website")
textInput("Social media address(es)", "contactfacebook", placeholder="facebook / instagram / twitter")

textInput("Contact person", "contactname")
textInput("Contact e-mail", "contactemail")
textInput("Contact phone", "contactphone")

textInput("Venue type", "venuetype")
textInput("Preferred show genres", "preferredgenres", "theatre / music / visual art / dance / literary / film / workshop")
textInput("Other allowed genres", "allowedgenres", "theatre / music / visual art / dance / literary / film / workshop")
textInput("Performance space", "performancespace", "size & description")
yesnoInput("Wall space available?", "wallspace")
textInput("Wall size", "wallsize")
textInput("Window?", "window")
textInput("Capacity", "capacity")
textInput("Stage?", "stage")

print("</table></div>")

availabilitySection()

endPage()

