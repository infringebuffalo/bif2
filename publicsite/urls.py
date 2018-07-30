from django.urls import path
# from django.contrib.auth import urls as auth_urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('history/', views.history, name='history'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/allshows/', views.scheduleShows, name='scheduleShows'),
    path('schedule/allvenues/', views.scheduleVenues, name='scheduleVenues'),
    path('schedule/allgenres/', views.scheduleGenres, name='scheduleGenres'),
    path('schedule/calendar/', views.scheduleCalendar, name='scheduleCalendar'),
    path('schedule/calendar/<int:daynum>/', views.scheduleCalendar, name='scheduleCalendar'),
    path('schedule/calendar2/', views.scheduleCalendar2, name='scheduleCalendar2'),
    path('schedule/calendar2/<int:daynum>/', views.scheduleCalendar2, name='scheduleCalendar2'),
    path('schedule/map/', views.scheduleMap, name='scheduleMap'),
    path('schedule/<int:id>/', views.entityInfo, name='entityInfo'),
]
