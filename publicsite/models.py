import datetime

from django.db import models
from django.utils import timezone

class CalendarEvent(models.Model):
	datetime = models.DateTimeField('date')
	title = models.TextField('title')
	description = models.TextField('description', max_length=200)
	url = models.URLField('url', max_length=100, blank=True, null=True)
	def __str__(self):
		return ' - '.join([self.datetime.__str__(), self.title])
	# things should disappear the day after at approx. midnight
	def is_upcoming_event(self):
		return self.datetime >= timezone.now() - datetime.timedelta(hours=(timezone.now().hour + 1))
