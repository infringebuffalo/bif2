import datetime
import bleach

from markdown import markdown
from markdownx.models import MarkdownxField
from django.db import models
from django.utils import timezone

from django.dispatch import receiver
from django.db.models.signals import pre_save

class Announcement(models.Model):
	last_updated = models.DateTimeField('last_updated', editable=False)
	title = models.TextField('title') # not displayed on site
	image_url = models.URLField('url', max_length=128, blank=True, null=True)
	description = MarkdownxField()
	description_html = models.TextField('description_url', editable=False)
	def __str__(self):
		return ' - '.join([self.last_updated.__str__(), self.title])

@receiver(pre_save, sender=Announcement)
def mark_it_down_now(sender, instance, **kwargs):
    print(instance.description)
    instance.last_updated = timezone.now()
    instance.description_html = markdown(bleach.clean(instance.description, strip=True))


class CalendarEvent(models.Model):
	datetime = models.DateTimeField('date')
	title = models.TextField('title') # DISPLAYED on site (don't repeat the title in an H tag in the body)
	image_url = models.URLField('url', max_length=128, blank=True, null=True)
	description = MarkdownxField()
	description_html = models.TextField('description_url', editable=False)
	def __str__(self):
		return ' - '.join([self.datetime.__str__(), self.title])
	# things should disappear the day after at approx. midnight
	def is_upcoming_event(self):
		return self.datetime >= timezone.now() - datetime.timedelta(hours=(timezone.now().hour + 1))

@receiver(pre_save, sender=CalendarEvent)
def mark_it_down(sender, instance, **kwargs):
    print(instance.description)
    instance.description_html = markdown(bleach.clean(instance.description, strip=True))