from django.db.models import Model, IntegerField, CharField, TextField, DateField, DateTimeField, BooleanField, OneToOneField, ManyToManyField, ForeignKey, CASCADE, SET_NULL
from django.contrib.auth.models import User


class Entity(Model):
    entityType = CharField(max_length=256)
    permissions = ManyToManyField('BIFUser', through='UserPermission')


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
    festival = ForeignKey('FestivalInfo', on_delete=SET_NULL, null=True)
    orgContact = ForeignKey('BIFUser', on_delete=SET_NULL, null=True)
    class Meta:
        permissions = (("can_schedule", "Schedule shows"),)


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


class GroupShow(Entity):
    title = CharField(max_length=256)
    where = ForeignKey('Venue', on_delete=CASCADE)
    date = DateField()
    starttime = IntegerField()
    endtime = IntegerField()
    cancelled = BooleanField(default=False)
    festival = ForeignKey('FestivalInfo',on_delete=SET_NULL,null=True)
    description = TextField()
    shortdescription = TextField()


class Note(Entity):
    creator = ForeignKey('BIFUser', on_delete=SET_NULL, null=True)
    notetext = TextField()
    timestamp = DateTimeField(auto_now=True)
    attachedTo = ManyToManyField('Entity', related_name='notes')


class UserPermission(Model):
    NONE = 0
    VIEW = 1
    EDIT = 2
    OWNER = 3
    CONTACT = 4
    SCHEDULE = 5
    entity = ForeignKey('Entity', on_delete=CASCADE, related_name='permit_who')
    bifuser = ForeignKey('BIFUser', on_delete=CASCADE, related_name='permit_what')
    permission = IntegerField(default=NONE, choices=((NONE, 'none'), (VIEW, 'view'), (EDIT, 'edit'), (OWNER, 'owner'), (CONTACT, 'festival contact'), (SCHEDULE, 'can schedule')))


class FormInfo(Entity):
    showType = CharField(max_length=256)
    festival = ForeignKey('FestivalInfo',on_delete=SET_NULL,null=True)
    description = TextField()
    defaultContact = ForeignKey('BIFUser', on_delete=SET_NULL, null=True)
    defaultBatch = ForeignKey('Batch', on_delete=SET_NULL, null=True)
    fields = TextField()


class Spreadsheet(Entity):
    name = CharField(max_length=256)
    festival = ForeignKey('FestivalInfo',on_delete=SET_NULL,null=True)
    description = TextField()
    frombatch = ForeignKey('Batch', on_delete=SET_NULL, null=True)
    columns = TextField()


class SpreadsheetRow(Model):
    spreadsheet = ForeignKey('Spreadsheet', on_delete=CASCADE, related_name='rows')
    entity = ForeignKey('Entity', on_delete=CASCADE)
    data = TextField()


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

@receiver(post_init,sender=FormInfo)
def setEntityTypeFormInfo(sender,instance,**kwargs):
    instance.entityType='forminfo'

@receiver(post_init,sender=Spreadsheet)
def setEntityTypeSpreadsheet(sender,instance,**kwargs):
    instance.entityType='spreadsheet'

@receiver(post_init,sender=GroupShow)
def setEntityTypeGroupShow(sender,instance,**kwargs):
    instance.entityType='groupshow'

