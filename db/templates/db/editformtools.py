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

<h2>Editing %s proposal </h2>

<div style="background:#f88; text-align:center">Note: all fields marked with * must be filled in before this form is submitted.</div>

<form method="POST" action="{%% url 'db-update' %%}" name="proposalform" onsubmit="return validateForm()">
{%% csrf_token %%}

<input type="hidden" name="prop_id" value="{{ prop_id }}" />
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
""")
    for daynum in range(0,11):
        print("<tr><th>{{daylist.%d}}</th>" % daynum)
        for name,text in [("8am", "8am-noon"), ("noon", "noon-4pm"), ("4pm", "4pm-8pm"), ("8pm", "8pm-midnight"), ("mid", "midnight-4am")]:
            inputname = "available_day%d_%s" % (daynum+1,name)            
            print("""<td>
<input type="hidden" name="%s" value="no">
<input type="checkbox" name="%s" value="yes"{%% if prop_info.%s == "yes" %%} checked{%% endif %%}>
<label for="%s">%s</label>
</td>""" % (inputname,inputname,inputname,inputname,text))
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
    print("<td><input type='text' name='%s' size='60' placeholder='%s' value='{{ prop_info.%s }}'/></td>" % (name,placeholder,name))
    print("</tr>")

def shorttextarea(label,name,rows=4,maxlen=140,placeholder=''):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><textarea name='%s' rows='%d' cols='60' maxlength='%d' placeholder='%s'>{{ prop_info.%s }}</textarea></td>" % (name,rows,maxlen,placeholder,name))
    print("</tr>")

def textarea(label,name,rows=4,placeholder=''):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><textarea name='%s' rows='%d' cols='60' placeholder='%s'>{{ prop_info.%s }}</textarea></td>" % (name,rows,placeholder,name))
    print("</tr>")

def yesnoInput(label,name,default='y'):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'><option value='Y'{%% if prop_info.%s == \"Y\" %%} selected{%% endif %%}>Yes</option><option value='N'{%% if prop_info.%s != \"Y\" %%} selected{%% endif %%}>No</option></select></td>" % (name,name,name))
    print("</tr>")

def menuInput(label,name,options):
    global all_required_fields
    if name in all_required_fields: label = '* ' + label
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'>" % name)
    for o in options:
        print("<option value='%s'{%% if prop_info.%s == \"%s\" %%} selected{%% endif %%}>%s</option>" % (o,name,o,o))
    print("</select></td>")
    print("</tr>")

