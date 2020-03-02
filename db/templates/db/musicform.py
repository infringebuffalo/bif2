#!/usr/bin/python

from formtools import *

startPage("Music",formtype="music",requiredfields=["organization","work_samples_website","numberperformers","membersinfo","out_of_town","proposaloverlap","agesensitive"])
textInput("Band name / title", "title")
textInput("Website (not Facebook)", "website")
textInput("Social media address(es)", "facebook", placeholder="facebook / instagram / twitter")
textInput("Web link to best example of what you plan to do", "work_samples_website", "a good link will answer most of our questions, to program you effectively")
shorttextarea("Short description (140 chars)", "description_short", 2, placeholder="This is what people will see in the free weekly paper.  Limited to 140 characters; be succinct.")
textarea("Long description (for website &amp; press releases)", "description_long", 6, placeholder="This text will be shown publicly on our website.  This is what potential audiences see in the schedule on our site.")
textInput("How many members in proposal? (#)", "numberperformers")
textarea("Who are they and what do they do?", "membersinfo", 6)
textInput("Are you based within 60 miles of Buffalo area? Will you need help with housing?", "out_of_town")
textarea("Are any of your members in other proposals? Explain.", "proposaloverlap", 2)
yesnoInput("Is everyone in the proposal over 21?", "over21")
yesnoInput("Would you like to be scheduled for outdoor performances (sidewalks, porches, yards, parking lots, etc)?", "outdoorperformaces")
menuInput("Where do prefer to be scheduled?", "street_preferred", ["all indoor", "mostly indoor", "either indoor or outdoor", "mostly outdoor", "all outdoor"])
yesnoInput("Are you willing to perform as part of opening or closing ceremonies? (Money collected from these two events goes to the festival.)", "openingclosing", default='n')
menuInput("Desired number of performances", "numberperformances", [1,2,3])
yesnoInput("Are you open to having more than one performance per day?", "morethan1perday", default='n')
textInput("Length of performance: (in minutes)", "showlength")
yesnoInput("Is this flexible?", "showlengthflexible")
textInput("Setup time (in minutes)", "setuptime")
textInput("Teardown time (in minutes)", "teardowntime")
textInput("Do you have a prearranged venue?", "prearrangedvenue")
textInput("Do you have an ideal venue in mind?", "idealvenue")
textarea("What requirements do you have for your venue?", "venuerequirements")
textInput("Is the performance kid-friendly, or does it have age-sensitive content, or neither?", "agesensitive")
textInput("Proposal secondary categories, if any:", "secondary_category", placeholder="theatre, dance, visual art, literary, film/video, workshop")
yesnoInput("Are you interested in collaborating (performing in combination with another proposal of the same or different category)?", "collaboration", default='n')
textarea("If yes, describe the kinds of proposals that might work, and any other info to guide us.", "collaboration_details")
print("</table></div>")

availabilitySection()

print("<div class='projectForm'>\n<h3>Music specifics</h3>\n<table class='alternategrey'>\n")
textarea("Equipment detail - describe your gear", "equipment_detail")
textInput("Do you own your own PA?  Will you share it for a group show?", "haspa")
textInput("Do you require microphones to perform (Y/N)? If so, how many? Do you own your own mics?  Share?", "hasmics")
textInput("Does your proposal involve a computer or electronic component (ipod, laptop, cd player, projector, other)?  If yes, explain.", "electronics")
textInput("Do you have a drum kit?  Share?", "hasdrum")
textInput("Can you play acoustic, without amps and mics? Preferred?", "acoustic")
textInput("Volume on a scale from 1-10", "volume")
genreMenu = [ "americana", "blues", "classical", "jazz", "reggae", "country", "electronic", "folk", "rock", "punk", "metal", "hip hop", "rap", "soul", "funk" , "disco", "electronic", "dance", "acoustic", "singer/songwriter", "noise", "world", "pop", "progressive", "hardcore", "avant garde", "synth", "retro", "improv", "jam", "EDM", "industrial", "easy listening", "inspirational - christian & gospel", "instrumental", "choral", "lo-fi", "latin" ]
genreMenu.sort(key=str.lower)
menuInput("Primary genre", "genre", genreMenu)
menuInput("Secondary genre", "genre2", genreMenu)
menuInput("Tertiary genre", "genre3", genreMenu + ["other"])
print("</table></div>")

print("<div class='projectForm'>\n<h3>Final details</h3>\n<table class='alternategrey'>\n")
textarea("In what ways are you willing to volunteer?", "volunteer", 2, placeholder="equipment gopher, tech (audio/video/stage/etc), PR distribution, videography/photography, other")
textInput("Anything else we need to know?", "anythingelse")
textInput("Any questions?", "questions")
print("</table></div>")

endPage()

