#!/usr/bin/python

all_required_fields = [ "contactname", "contactemail", "contactphone", "contactaddress", "title", "description_short" ]

def startPage(formtitle,formtype=None,requiredfields=None):
    global all_required_fields
    if not formtype:
        formtype = formtitle.lower()
    if requiredfields:
        all_required_fields += requiredfields
    requiredfields_str = ', '.join(map(lambda x:'"%s"'%x,all_required_fields))
    print("""{%% extends "base_generic.html" %%}

{%% block title %%}Buffalo Infringement Festival %s Proposal{%% endblock %%}

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

<h1>{{ prop }}</h1>
<h2>%s proposal </h2>

<div style="background:#f88; text-align:center">Note: all fields marked with * must be filled in before this form is submitted.</div>

<form method="POST" action="{%% url 'submit' %%}" name="proposalform" onsubmit="return validateForm()">
{%% csrf_token %%}

<input type="hidden" name="type" value="%s" />

<div class="contact">
<h3>Contact info</h3>
<table id="contactinputs">""" % (formtitle, requiredfields_str, formtitle, formtype))
    textInput("Proposer / primary contact", "contactname")
    textInput("E-mail", "contactemail")
    textInput("Phone (including area code)", "contactphone")
    textInput("Zip code", "contactaddress")
    textInput("Social media address(es)", "contactfacebook", placeholder="facebook / instagram / twitter")
    menuInput("Best method to contact you", "bestcontactmethod", ["phone", "email", "facebook"])
    print("</table>\n<br>\n<table>")
    textInput("Secondary contact name", "secondcontactname")
    textInput("E-mail", "secondcontactemail")
    textInput("Phone (including area code)", "secondcontactphone")
    print("</table>\n\n<div class='projectForm'>\n<h3>Project</h3>\n<table class='alternategrey'>")


def availabilitySection():
    print("""<div class="projectForm">
<h3>Availability  (click all boxes that apply for each day.)</h3>
<table class="avail">
{% for d in daylist %}
<tr>
<th>{{ d }}</th>
{% for name,text in timelist %}
<td>
<input type="hidden" name="available_day{{forloop.parentloop.counter}}_{{name}}" value="no">
<input type="checkbox" name="available_day{{forloop.parentloop.counter}}_{{name}}" value="yes">
<label for="available_day{{forloop.parentloop.counter}}_{{name}}">{{text}}</label>
</td>
{% endfor %}
</tr>
{% endfor %}
</table>
</div>
""")

def endPage():
    print("""<input type="Submit" name="submit" value="Submit" />
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
    print("<td><input type='text' name='%s' size='60' placeholder='%s'/></td>" % (name,placeholder))
    print("</tr>")

def textarea(label,name,rows=4,placeholder=''):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><textarea name='%s' rows='%d' cols='60' placeholder='%s'></textarea></td>" % (name,rows,placeholder))
    print("</tr>")

def yesnoInput(label,name,default='y'):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    if default.lower() in ('y', 'yes'):
        print("<td><select name='%s'><option value='Y' selected>Yes</option><option value='N'>No</option></select></td>" % name)
    else:
        print("<td><select name='%s'><option value='Y'>Yes</option><option value='N' selected>No</option></select></td>" % name)
    print("</tr>")

def menuInput(label,name,options):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'>" % name)
    for o in options:
        print("<option value='%s'>%s</option>" % (o,o))
    print("</select></td>")
    print("</tr>")

