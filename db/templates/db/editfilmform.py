#!/usr/bin/python

from editformtools import *

startPage("Film/Video","film")
textInput("Title", "title")
textInput("Organization / production company", "organization")
textInput("Website (not Facebook)", "website")
textInput("Social media address(es)", "facebook", placeholder="facebook / instagram / twitter")
textInput("Web link to best example of what you plan to do", "work_samples_website", "a good link will answer most of our questions, to program you effectively")
textarea("Short description (140 chars)", "description_short", 2)
textarea("Long description (for website &amp; press releases)", "description_long", 6)
textarea("Who made the work and what are their roles?", "membersinfo", 6)
textInput("Are you based within 60 miles of Buffalo area? Will you need help with housing?", "out_of_town")
textarea("Are any of your members in other proposals? Explain.", "proposaloverlap", 2)
yesnoInput("Would you like to be scheduled for outdoor performances (sidewalks, porches, yards, parking lots, etc)?", "outdoorperformaces")
menuInput("Where do prefer to be scheduled?", "street_preferred", ["all indoor", "mostly indoor", "either indoor or outdoor", "mostly outdoor", "all outdoor"])
menuInput("Desired number of performances", "numberperformances", [1,2,3,4,5])
textInput("Length of screening: (in minutes)", "showlength")
textInput("Do you have a prearranged venue?", "prearrangedvenue")
textInput("Do you have an ideal venue in mind?", "idealvenue")
textInput("Is the performance kid-friendly, or does it have age-sensitive content, or neither?", "agesensitive")
textInput("Proposal secondary categories, if any:", "secondary_category", placeholder="theatre, dance, visual art, literary, music, workshop")
yesnoInput("Are you interested in collaborating (performing in combination with another proposal of the same or different category)?", "collaboration", default='n')
textarea("If yes, describe the kinds of proposals that might work, and any other info to guide us.", "collaboration_details")
print("</table></div>")

availabilitySection()

print("<div class='projectForm'>\n<h3>Film/Video specifics</h3>\n<table class='alternategrey'>\n")
textarea("Your equipment details (what equipment you bring, plus any unusual or unusually large setups)", "equipment_detail")
print("</table></div>")

print("<div class='projectForm'>\n<h3>Final details</h3>\n<table class='alternategrey'>\n")
textarea("In what ways are you willing to volunteer?", "volunteer", 2, placeholder="equipment gopher, tech (audio/video/stage/etc), PR distribution, videography/photography, other")
textInput("Anything else we need to know?", "anythingelse")
textInput("Any questions?", "questions")
print("</table></div>")

endPage()

