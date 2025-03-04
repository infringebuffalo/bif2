# run this via "python manage.py shell < CreateFest.py"
# only do this once, when setting up the database

from db.models import FestivalInfo
import datetime, sys

print("MAKE SURE THIS SCRIPT IS UPDATED FOR THE CURRENT YEAR & DATES")

sys.exit()

print("creating FestivalInfo")
f = FestivalInfo(name='Buffalo Infringement Festival 2025', description='Buffalo Infringement Festival 2025', startDate = datetime.date(2025, 7, 24), numberOfDays=11)
f.save()

print("deleting old proposals, notes, batches, groupshows, and spreadsheets")
from db.models import *
props = Proposal.objects.all()
for i in props:
   i.delete()
notes = Note.objects.all()
for i in notes:
   i.delete()
batches = Batch.objects.all()
for i in batches:
   i.delete()
groups = GroupShow.objects.all()
for i in groups:
   i.delete()
sheets = Spreadsheet.objects.all()
for i in sheets:
   i.delete()
#
## put all venues in "waiting" state, rather than deleting
venues = Venue.objects.all()
for i in venues:
   i.status = Venue.WAITING
   i.save()

print("creating proposalinfos & default batches")
proposalInfo = [
    { "name": "music", "contact": "music@infringebuffalo.org"},
    { "name": "theatre", "contact": "theatre@infringebuffalo.org" },
    { "name": "visualart", "contact": "visualart@infringebuffalo.org" },
    { "name": "literary", "contact": "literary@infringebuffalo.org" },
    { "name": "film", "contact": "film@infringebuffalo.org" },
    { "name": "workshop", "contact": "workshop@infringebuffalo.org" },
    { "name": "dance", "contact": "dance@infringebuffalo.org" },
    ]
for p in proposalInfo:
    name = p["name"]
    contact = p["contact"]
    b = Batch(name=name, festival=f, description=f"{name} proposals")
    b.save()
    dju = User.objects.get(username=contact)
    u = dju.bifuser
    fi = FormInfo(showType=name, festival=f, description=name, defaultContact=u, defaultBatch=b)
    fi.save()
from db.makeforminfo import *
makeFormInfo_all()

print("done")
