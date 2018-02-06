#!/usr/bin/python


def startPage(formtitle,formtype=None):
    if not formtype:
        formtype = formtitle.lower()
    print("""{%% extends "base_generic.html" %%}

{%% block title %%}Buffalo Infringement Festival %s Proposal{%% endblock %%}

{%% block style %%}
<style>
.avail td { padding: 10px }
.avail tr:nth-child(odd) { background-color: #f0f0f0 }
</style>
{%% endblock %%}

{%% block scripts %%}

<script type="text/javascript">
function validateForm()
{
var f = document.forms["proposalform"];
var fields = ["title", "website", "description_short", "description_long", "contactname", "contactemail", "contactphone", "contactaddress", "volunteer"];
var okay = true;
for (i=0; i < fields.length; i++)
    if ((f[fields[i]].value == null) || (f[fields[i]].value == ""))
        okay = false;
if (!okay)
    {
    alert("All fields must be filled out before this proposal can be submitted");
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

<div style="background:#f88; text-align:center">Note: all fields must be filled in before this form is submitted.</div>

<form method="POST" action="{%% url 'submit' %%}" name="proposalform" onsubmit="return validateForm()">
{%% csrf_token %%}

<input type="hidden" name="type" value="%s" />

<div class="contact">
<h3>Contact info</h3>
<table id="contactinputs">
  <tr><th width="20%%">Proposer / primary contact</th><td> <input type="text" name="contactname" value="" /> </td></tr>
  <tr><th>E-mail</th><td> <input type="text" name="contactemail" value="" /> </td></tr>
  <tr><th>Phone</th><td> <input type="text" name="contactphone" value="" /> </td></tr>
  <tr><th>Zip code</th><td> <input type="text" name="contactaddress" value="" /> </td></tr>
  <tr><th>Facebook address</th><td><input type="text" name="contactfacebook" /></td></tr>
  <tr><th>Best method to contact you</th><td> <select name="bestcontactmethod"> <option value="phone">phone</option> <option value="email">email</option> <option value="facebook">facebook</option> </select> </td></tr>
</table>
<table>
  <tr><th width="20%%">Secondary contact name</th><td><input type="text" name="secondcontactname"></td></tr>
  <tr><th>E-mail</th><td><input type="text" name="secondcontactemail"></td></tr>
  <tr><th>Phone (including area code)</th><td><input type="text" name="secondcontactphone"></td></tr>
</table>

<div class="projectForm">
<h3>Project</h3>
<table>
""" % (formtitle, formtitle, formtype))

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

    
def textInput(label,name):
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><input type='text' name='%s' size='60' /></td>" % name)
    print("</tr>")

def textarea(label,name,rows=4,cols=60):
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><textarea name='%s' rows='%d' cols='%d'></textarea></td>" % (name,rows,cols))
    print("</tr>")

def yesnoInput(label,name):
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'><option value='Y'>Yes</option><option value='N'>No</option></select></td>" % name)
    print("</tr>")

def menuInput(label,name,options):
    checkName(name)
    print("<tr>")
    print("<th width='25%%'>%s</th>" % label)
    print("<td><select name='%s'>" % name)
    for o in options:
        print("<option value='%s'>%s</option>" % (o,o))
    print("</select></td>")
    print("</tr>")

