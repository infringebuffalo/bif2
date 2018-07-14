from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login,authenticate
# from django.template import loader
# from django.core.mail import EmailMultiAlternatives

from .models import CalendarEvent

# import json

def index(request):
    ordered_by_date = CalendarEvent.objects.order_by('datetime')
    just_upcoming = list(filter(lambda e: e.is_upcoming_event(), ordered_by_date))
    if len(just_upcoming) > 0:
        next_event = [just_upcoming[0]]
    else:
        next_event = []
    next_events_list = just_upcoming[1:]
    context = { 'next_event' : next_event, 'next_events_list' : next_events_list }
    return render(request,'publicsite/index.html', context)

def about(request):
    return render(request,'publicsite/about.html', { })

def contact(request):
    organizers = [
        {'name' : "David Adamczyk", 'role' : "Street", 'email' : "dga8787@aol.com"},
        {'name' : "Amy Duengfelder + Cat McCarthy ", 'role' : "Art", 'email' : "visualinfringement@live.com"},
        {'name' : "Leslie Fineberg", 'role' : "Dance", 'email' : "danceundertheradar@gmail.com"},
        {'name' : "Eddie Gomez", 'role' : "Literary", 'email' : "eddiegoofball@yahoo.com"},
        {'name' : "Jessica Knoerl", 'role' : "Theater", 'email' : "jessicaknoerl@gmail.com"},
        {'name' : "Dave Pape", 'role' : "Treasurer, Database, Web", 'email' : "depape@buffalo.edu"},
        {'name' : "Curt Rotterdam", 'role' : "Music, Meeting Chair", 'email' : "merlinsbooking@gmail.com"},
        {'name' : "Bill Smythe", 'role' : "Venues", 'email' : "whsmythe@gmail.com"},
        {'name' : "Tom Stoll", 'role' : "Web", 'email' : "tms@kitefishlabs.com"},
        {'name' : "Pam Swarts", 'role' : "Poster", 'email' : ""},
        {'name' : "Janna Willoughby-Lohr", 'role' : "Paper Schedule Design", 'email' : ""},]
    return render(request,'publicsite/contact.html', { 'orgs' : organizers })

def history(request):
    return render(request,'publicsite/history.html', { })

def faq(request):
    qnas = {'General Information':
    [["What is the Buffalo Infringement Festival?",
    "The Buffalo Infringement Festival is a celebration of all art forms in a multitude of locations around the city of Buffalo. The artists are primarily local talent, but they also include regional and international artists. The festival covers a huge variety of art from traditional, family-orientated, and political, eclectic, controversial, and experimental."],
    ["How does it happen?",
    "Many volunteer hours are put in to secure venues, manage availability, and schedule artists. A group of volunteer organizers plan and schedule the eleven days of events, and do fundraising and awareness events throughout the year. We can always use more participants, though, and please consider volunteering!"],
    ["Who are the people behind the Buffalo Infringement Festival?",
    "A group of core volunteer organizers including art enthusiasts, educators, business owners, booking agents, and the artists themselves make Infringement possible."],
    ["Where does Infringement happen?",
    "The Buffalo Infringement Festival began in Allentown, but has spread across the city, including to Grant St, Jefferson Ave, and Elmwood."],
    ["When is Infringement?",
    "It starts on the last Thursday of July and runs eleven days through the first weekend of August. Specific dates change from year to year. The 2018 festival will run from July 26th to August 5th."],
    ["What kind of events occur during Infringement?",
    "Every kind of artistic discipline is represented in this festival--including artists who defy categorization. Music of all varieties including acoustic, folk, progressive, rock, metal, punk, indie, noise, electronic, jazz, and world. Dance, including modern, movement, jazz, step, belly-dancing, swing, African, and many World dances. Theater, from serious to lighthearted. Poetry, spoken word, and other litera. Film: full-length features, short films, and multimedia. Visual art: painting, sculpture, drawing, metal work, wood working, pottery, crafting, DIY, conceptual art, installation, and public art. Street performers like mimes, balloon arts, and juggling. Audience participation events like workshops, demonstrations, and interactive theater"]],
    'Audience Members':
    [["Where is the schedule available?",
    "The schedule is available online and in The Public. The Public schedule comes out the day before Infringement. There are also schedules available at most of the venues. Check online at infringebuffalo.org to stay abreast of any changes!"],
    ["When can we see the schedule?",
    "Look for the schedule in The Public the week of the festival. In 2018 the schedule will appear in the Public on July 25."],
    ["What about last minute changes and cancellations?",
    "The printed schedule is designed several weeks before the actual events, so there are likely to be changes. The online schedule is the most up-to-date source for changes, cancellations, added performances, and contains detailed descriptions of installations and performances."]],
    'Artists':
    [["What does Infringement provide for artists?",
    "We schedule your shows, provide some logistics, and generally promote the festival. Organizers are also take on the job of creating a paper schedule published in the Public and an online schedule."],
    ["When do I sign up?",
    "BIF accepts proposals up until May 1. Actual dates may vary from year to year, so check for calls for work early."],
    ["How do I sign up?",
    "Go to infringebuffalo.org/db. You will need to create an account and then create a new proposal. You must submit multiple proposals if you have more than one project."],
    ["What questions will be asked on the proposal form?",
    "Basic information about your and your performance or showing. Remember to add your short description for The Public, and public description on the website, as well as links to examples of your work online."],
    ["What does BIF NOT provide?",
    "Each artist must provide their own equipment when not at a venue with a backline. You are encouraged to share equipment whenever possible. Unfortuneately, we cannot really do much to promote your show beyond publishing it in the schedule."],
    ["What do I have to do as an artist?",
    "STAY IN TOUCH WITH YOUR ORGANIZER!!! They’ll be contacting you by phone and e-mail about meetings, show requirements, and other specifics. Check your spam folder and start to worry if you don’t hear from someone. Please be respectful of everyone, follow the law, and be ready for things to change."],
    ["Should I promote myself?",
    "Absolutely! With so many events you can easily get lost in the shuffle. It's our suggestion that you make and hang your own flier around town, etc., Use social media and other online platforms to publicize your shows. Include the names of the other performers, projects, companies in that venue on the same day to generate more interest and draw a larger range of viewers. Word of mouth is still the best advertising platform!"],
    ["How do I get in contact with other artists in the same show?",
    "Your schedule will show other artists in the same show.  You can contact your genre organizer to send a cc’ed email of all other artists on the bill. This is especially helpful to bands for setting the order, or sharing gear."],
    ["Why should I fill in program info?",
    "The program info is what will show in the schedule and on the website to patrons, viewers and other artists. This is filled out after the artist has confirmed their dates. Upload a photo to add interest."],
    ["How often should I check my email? What's that strange number calling me?",
    "BIF primarily uses email to communicate with the artists, and we will call you to confirm your scheduling. It is very important that artists check their email regularly during the month before the show. Artists will receive emails from different organizers. The most important being a confirmation that the artist is available for the times scheduled. Artists will also receive emails for the press event, volunteer needs, housing, questions from the venue, and last minute changes to the schedule."],
    ["I'd like to busk. Do I need a license?",
    "Yes. Go to City Hall, Room 303. It’s $10.50, and good for the whole year! You will need 2 passport-sized photos. You may be able have these taken at a kiosk in the lobby."],
    ["If I'm from out of town, where should I stay?",
    "Housing is available for out-of-towners. Many of the participants share their couches or spare bedrooms. There are a couple of co-op houses and venues offering space for larger parties. Hotels in the city are relatively inexpensive and the ones near the airport are pretty cheap. The airport is a 20 minute drive to the city. Plan ahead and contact us if you need help securing housing."],
    ["When do visual artists hang and/or setup their works?",
    "Visual artists receive a email with hang and tear down dates, as well as other details. Artist agreements are requested by some galleries."],
    ["Can you help bands/artists transport their gear?",
    "We can help, but it's ultimately the performers' responsibility to get themselves and their gear to their shows themselves."]],
    'Venues':
    [["What does Infringement provide for a venue?",
    "BIF organizers schedule performances and art appropriate to your venue, based on responses to venue questionaires and communication with organizers."],
    ["When can I find out the schedule for my venue?",
    "We finalize the schedule by July 1st, but most scheduling is done in early to mid June."],
    ["How exactly do I find out which days Infringement is using the space?",
    "Log in to our scheduler, or give your organizer contact a call! You should know the final plan by early July. And one of the organizers should be calling you in the first place."],
    ["So which bands do you choose for my space?",
    "Whichever are available on the nights your venue is, and are appropriate for your space and expressed interests."],
    ["How much of my venue's availability will be filled?",
    "We have 400 artists. If you tell us to schedule a lot for your space, we will. If you're only available for a day or two, we can work with that too. We work with each venue to program concerts and performances that work for the artists, audience, and the venue itself."],
    ["How do I promote my venue for BIF? Will the festival handle this?",
    "BIF only provides scheduling and logistics, so it’s up to each venue to promote themselves. Artists are encouraged to promote their own shows, so they will bring their own fans, friends, and family. The festival organizers make an effort to promote shows, but there's only so much that we can do."],
    ["Can I book a show myself for the venue? What if I have a regularly scheduled event during BIF?",
    "If you want to propose an entire event or there is an event already planned that wants to join forces with BIF, we have no problem allowing the venue to do most of the organization.  We have a few simple requirements: All artists must apply to the festival and communicate with us concerning scheduling. The event should be identified as an Infringement event, and the same guidelines hold regarding payment of performers and charging for entry."],
    ["Can I choose the artists?",
    "With so many artists involved, organizers are assigned to each artist genre. It can be a big juggling game--so trust in their skills to match the venue with what goes best in that space."],
    ["What if I only want certain types of music or visual art?",
    "You may give us guidelines for what genres and styles are most relevant to your venue, and our organizers use common sense. The physical layout an limitations also determine what we will program."],
    ["Who pays our sound/lighting/tech person?",
    "The artists are responsible for paying all extra persons needed for their performance, with the exception of a few larger venues where we or the venue itself provides tech."],
    ["Can my gallery/space collect fees from visual artists selling their works or bands selling CDs?",
    "BIF requests that each venue charge no more than a 20\% commission on fine art. As an artist-run festival, we encourage direct compensation of artists, but we recognize that galleries and other spaces are literally giving us the space to use for free. Those artists selling CDs or DVDs should not be charged any fee."]],
    'Volunteering, Organizing and Contributing the Festival':
    [["Do you accept donations?",
    "Yes. You may currently make a donation via IndieGoGo. Click above. All money goes to local vendors to pay for printing the schedule and securing paid technical and security assistance with some of our larger venues."],
    ["Do you need volunteers?",
    "Yes. All organizers are volunteers. One way to get more involved with the organization of the festival is through volunteering. We have all kinds of tasks that need your help."],
    ["How do I volunteer?",
    "Come to an organizer's meeting. Talk to an organizer. Or email info@infringebuffalo.org with your contact info and how you are interested in helping."],
    ["What do you need volunteers to do?",
    "PR, advertising, street team. General production/tech help. Venue czars, a.k.a. show-runners. You could also write about our artists or show up and photograph/film our events. We can always use people with cars or SUVs to move equipment around."],
    ["Do the organizers meet regularly?",
    "Yes. At least once a month---first Mondays at 6:30 @ Allentown Association (61 College St./Buffalo). Our meetings are a lot of fun. We meet more often in May, June, and July..."],
    ["What other events do you produce?",
    "We produce the festival plus a few fundraisers throughout the year. We have a presence at Music is Art and some other events around town. Our organizers are involved in all kinds of events and organizations."],
    ["Do organizers get paid?",
    "You must be joking."]]}
    return render(request,'publicsite/faq.html', {'qnas' : qnas})


from db.models import *
import json

def schedule(request):
    return render(request,'publicsite/schedule.html', { })

def scheduleShows(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    shows = Proposal.objects.filter(festival=fest,status=Proposal.ACCEPTED).order_by(Lower('title'))
    return render(request,'publicsite/scheduleShows.html', { 'shows': shows })

def scheduleVenues(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    venues = Venue.objects.filter(status=Venue.ACCEPTED).order_by(Lower('name'))
    return render(request,'publicsite/scheduleVenues.html', { 'venues': venues })

def scheduleGenres(request):
    from django.db.models.functions import Lower
    fest = FestivalInfo.objects.last()
    forms = FormInfo.objects.filter(festival=fest).order_by(Lower('showType'))
    shows = Proposal.objects.filter(festival=fest,status=Proposal.ACCEPTED).order_by(Lower('title'))
    genres = []
    for f in forms:
        genreshows = []
        for s in shows:
            infodict = json.loads(s.info)
            if infodict['type'] == f.showType:
                genreshows.append(s)
        genres.append({'name':f.showType, 'shows':genreshows})
    groupshows = GroupShow.objects.filter(festival=fest).order_by(Lower('title'))
    genres.append({'name': 'Group shows', 'shows':list(groupshows)})
    return render(request,'publicsite/scheduleGenres.html', { 'genres': genres })

def scheduleCalendar(request):
    from datetime import timedelta
    from django.db.models.functions import Lower
    days = []
    fest = FestivalInfo.objects.last()
    for d in range(0,fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        listingList = []
        listings = Listing.objects.filter(date=day,installation=False).order_by('starttime',Lower('where__name'))
        installations = Listing.objects.filter(date=day,installation=True).order_by('starttime',Lower('where__name'))
        days.append({'date': day.strftime("%A, %B %-d"), 'listings': listings, 'installations':installations})
    return render(request,'publicsite/scheduleCalendar.html', {'days':days })

def scheduleCalendar2(request):
    from datetime import timedelta
    from django.db.models.functions import Lower
    days = []
    fest = FestivalInfo.objects.last()
    for d in range(0,fest.numberOfDays):
        day = fest.startDate + timedelta(days=d)
        firstTime = 2800
        lastTime = 0
        listings = Listing.objects.filter(date=day,installation=False).order_by(Lower('where__name'),'starttime')
        prevVenue = None
        venueList = []
        listingsAtVenue = []
        groupshows = []
        for l in listings:
            if l.where != prevVenue:
                if prevVenue:
                    venueList.append({'name':prevVenue.name, 'id':prevVenue.id, 'listings':listingsAtVenue, 'groupshows':groupshows})
                listingsAtVenue = []
                groupshows = GroupShow.objects.filter(date=day,where=l.where).order_by('starttime')
                prevVenue = l.where
            listingsAtVenue.append(l)
            firstTime = min(firstTime, l.starttime)
            lastTime = max(lastTime, l.endtime)
        installations = Listing.objects.filter(date=day,installation=True).order_by('starttime',Lower('where__name'))
        days.append({'date': day.strftime("%A, %B %-d"), 'firsttime': firstTime, 'lasttime': lastTime, 'venues': venueList, 'installations':installations})
    return render(request,'publicsite/scheduleCalendar2.html', {'days':days })

def entityInfo(request,id):
    e = get_object_or_404(Entity, pk=id)
    if e.entityType == 'proposal':
        return showInfo(request,e.proposal)
    elif e.entityType == 'venue':
        return venueInfo(request,e.venue)
    elif e.entityType == 'groupshow':
        return groupshowInfo(request,e.groupshow)
    else:
        return render(request, 'db/no_view.html')

def looksLikeURL(s):
    s = s.casefold()
    if s.find(' ') > -1:
        return False
    if s[0:4] == 'www.':
        return True
    elif s[0:12] == 'facebook.com':
        return True
    elif s[0:13] == 'instagram.com':
        return True
    elif s[0:14] == 'soundcloud.com':
        return True
    return False

def showInfo(request,proposal):
    infodict = json.loads(proposal.info)
    url = infodict['website']
    if not url.startswith('http'):
        url = 'http://' + url
    socialmedia = infodict['facebook']
    if socialmedia.startswith('http'):
        socialmediaurl = socialmedia
    elif looksLikeURL(socialmedia):
        socialmediaurl = 'http://' + socialmedia
    else:
        socialmediaurl = ''
    listings = proposal.listing_set.order_by('date','starttime')
    return render(request,'publicsite/showInfo.html', { 'show': proposal, 'info': infodict, 'url': url, 'socialmediaurl': socialmediaurl, 'listings':listings })

def venueInfo(request,venue):
    infodict = json.loads(venue.info)
    listings = venue.listing_set.filter(installation=False).order_by('date','starttime')
    installations = venue.listing_set.filter(installation=True).order_by('date','starttime')
    return render(request,'publicsite/venueInfo.html', { 'venue': venue, 'info': infodict, 'listings': listings, 'installations': installations })

def groupshowInfo(request,groupshow):
    alllistings = Listing.objects.filter(who__festival=groupshow.festival, where=groupshow.where, date=groupshow.date).order_by('starttime')
    listings = []
    for l in alllistings:
        if max(l.starttime,groupshow.starttime) <= min(l.endtime,groupshow.endtime):
            listings.append(l)
    return render(request,'publicsite/groupshowInfo.html', { 'groupshow': groupshow, 'listings': listings })

