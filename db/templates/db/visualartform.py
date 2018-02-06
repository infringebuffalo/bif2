#!/usr/bin/python

from formtools import *

startPage("Visual Art", "visualart",requiredfields=["work_samples_website","numberperformers","membersinfo","out_of_town","proposaloverlap","agesensitive"])
textInput("Name of piece/series (only one proposal per series, please)", "title")
textInput("Organization affiliation", "organization")
textInput("Website (not Facebook)", "website")
textInput("Social media address(es)", "facebook", placeholder="facebook / instagram / twitter")
textInput("Web link to best example of what you plan to do", "work_samples_website", "a good link will answer most of our questions, to program you effectively")
textarea("Short description (140 chars)", "description_short", 2)
textarea("Long description (for website &amp; press releases)", "description_long", 6)
textarea("Are you part of any other proposals? Explain.", "proposaloverlap", 2)
yesnoInput("Is everyone in the proposal over 21?", "over21")
yesnoInput("Would you like to be scheduled for outdoor performances (sidewalks, porches, yards, parking lots, etc)?", "outdoorperformaces")
menuInput("Where do prefer to be scheduled?", "street_preferred", ["all indoor", "mostly indoor", "either indoor or outdoor", "mostly outdoor", "all outdoor"])
textInput("Do you have a prearranged venue?", "prearrangedvenue")
textInput("Do you have an ideal venue in mind?", "idealvenue")
textarea("What requirements do you have for your venue?", "venuerequirements")
textInput("Is the work kid-friendly, or does it have age-sensitive content, or neither?", "agesensitive")
textInput("Proposal secondary categories, if any:", "secondary_category", placeholder="theatre, dance, music, literary, film/video, workshop")
yesnoInput("Are you interested in collaborating (performing in combination with another proposal of the same or different category)?", "collaboration", default='n')
textarea("If yes, describe the kinds of proposals that might work, and any other info to guide us.", "collaboration_details")
print("</table></div>")

availabilitySection()

print("<div class='projectForm'>\n<h3>Art specifics</h3>\n<table class='alternategrey'>\n")
textInput("Number of art pieces:", "numberpieces")
textarea("Desired wall space:", "wallspace", 3)
textarea("Is the work an installation (not wall-mounted)?  If so, please describe the layout","installationlayout")
yesnoInput("Does the work have an audio component? (For best results, plan to provide your own tech and/or check with venues where you are scheduled.)", "audio")
textInput("Does your proposal require AC power?", "acpower")
print("</table></div>")

print("<div class='projectForm'>\n<h3>Final details</h3>\n<table class='alternategrey'>\n")
textarea("In what ways are you willing to volunteer?", "volunteer", 2, placeholder="equipment gopher, tech (audio/video/stage/etc), PR distribution, videography/photography, other")
textInput("Anything else we need to know?", "anythingelse")
textInput("Any questions?", "questions")
print("</table></div>")

endPage()
