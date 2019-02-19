from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Announcement,CalendarEvent

admin.site.register(Announcement, MarkdownxModelAdmin)
admin.site.register(CalendarEvent, MarkdownxModelAdmin)