from django.db.models import Model, IntegerField, CharField, TextField, DateField, DateTimeField, BooleanField, OneToOneField, ManyToManyField, ForeignKey, CASCADE, SET_NULL
from django.contrib.auth.models import User


class Entity(Model):
    entityType = CharField(max_length=256)



class BIFUser(Entity):
    user = OneToOneField(User, on_delete=CASCADE)
    phone = CharField(max_length=256, default='')
    snailmail = TextField(default='')


class FestivalInfo(Entity):
    name = CharField(max_length=256)
    description = TextField()
    startDate = DateField()
    numberOfDays = IntegerField(default=1)


class Proposal(Entity):
    title = CharField(max_length=256)
    WAITING = 0
    ACCEPTED = 1
    DELETED = 2
    status = IntegerField(default=WAITING, choices=((WAITING, 'waiting'),(ACCEPTED, 'accepted'),(DELETED,'deleted')))
    info = TextField()
    festival = ForeignKey('FestivalInfo',on_delete=SET_NULL,null=True)


class Venue(Entity):
    name = CharField(max_length=256)
    WAITING = 0
    ACCEPTED = 1
    DELETED = 2
    status = IntegerField(default=WAITING, choices=((WAITING, 'waiting'),(ACCEPTED, 'accepted'),(DELETED,'deleted')))
    info = TextField()
    festival = ForeignKey('FestivalInfo',on_delete=SET_NULL,null=True)


class Batch(Entity):
    name = CharField(max_length=256)
    festival = ForeignKey('FestivalInfo',on_delete=SET_NULL,null=True)
    description = TextField()
#    entryType = CharField(max_length=256)  # may want to add this - limit entries in batch to a specific type; this would be mainly for the UI, to constrain what operations it offers
    members = ManyToManyField('Entity', related_name='batches')


class Listing(Entity):
    who = ForeignKey('Proposal', on_delete=CASCADE)
    where = ForeignKey('Venue', on_delete=CASCADE)
    venuenote = CharField(max_length=256, default='')
    date = DateField()
    starttime = IntegerField()
    endtime = IntegerField()
    installation = BooleanField(default=False)
    listingnote = TextField(default='')
    cancelled = BooleanField(default=False)
    

class Note(Entity):
    creator = ForeignKey('BIFUser', on_delete=SET_NULL, null=True)
    notetext = TextField()
    timestamp = DateTimeField(auto_now=True)
    attachedTo = ManyToManyField('Entity', related_name='notes')


from django.db.models.signals import post_init
from django.dispatch import receiver

@receiver(post_init,sender=BIFUser)
def setEntityTypeBIFUser(sender,instance,**kwargs):
    instance.entityType='bifuser'

@receiver(post_init,sender=FestivalInfo)
def setEntityTypeFestivalInfo(sender,instance,**kwargs):
    instance.entityType='festivalinfo'

@receiver(post_init,sender=Proposal)
def setEntityTypeProposal(sender,instance,**kwargs):
    instance.entityType='proposal'

@receiver(post_init,sender=Venue)
def setEntityTypeVenue(sender,instance,**kwargs):
    instance.entityType='venue'

@receiver(post_init,sender=Batch)
def setEntityTypeBatch(sender,instance,**kwargs):
    instance.entityType='batch'

@receiver(post_init,sender=Listing)
def setEntityTypeListing(sender,instance,**kwargs):
    instance.entityType='listing'

@receiver(post_init,sender=Note)
def setEntityTypeNote(sender,instance,**kwargs):
    instance.entityType='note'

