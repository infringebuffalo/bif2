from django.urls import path
from django.contrib.auth import urls as auth_urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newaccount/', views.newAccount, name='newAccount'),
    path('createaccount/', views.createAccount, name='createAccount'),
    path('allproposals/', views.allProposals, name='allProposals'),
    path('allvenues/', views.allVenues, name='allVenues'),
    path('newbatch/', views.newBatch, name='newBatch'),
    path('createbatch/', views.createBatch, name='createBatch'),
    path('batches/', views.batches, name='batches'),
    path('submit/', views.submit, name='submit'),
    path('musicForm/', views.musicForm, name='musicForm'),
    path('theatreForm/', views.theatreForm, name='theatreForm'),
    path('visualartForm/', views.visualartForm, name='visualartForm'),
    path('danceForm/', views.danceForm, name='danceForm'),
    path('literaryForm/', views.literaryForm, name='literaryForm'),
    path('filmForm/', views.filmForm, name='filmForm'),
    path('workshopForm/', views.workshopForm, name='workshopForm'),
    path('confirm/<int:id>/', views.confirmProposal, name='confirmProposal'),
    path('delete/<int:id>/', views.deleteProposal, name='deleteProposal'),
    path('undelete/<int:id>/', views.undeleteProposal, name='undeleteProposal'),
    path('venueForm/', views.venueForm, name='venueForm'),
    path('createVenue/', views.createVenue, name='createVenue'),
    path('editVenue/<int:id>/', views.editVenue, name='editVenue'),
    path('confirmVenue/<int:id>/', views.confirmVenue, name='confirmVenue'),
    path('deleteVenue/<int:id>/', views.deleteVenue, name='deleteVenue'),
    path('undeleteVenue/<int:id>/', views.undeleteVenue, name='undeleteVenue'),
    path('addtobatch/<int:batchid>/<int:memberid>/', views.addToBatch, name='addToBatch'),
    path('addtobatch/', views.addToBatchForm, name='addToBatch'),
    path('edit/<int:id>/', views.editProposal, name='editProposal'),
    path('update/', views.update, name='update'),
    path('updateVenue/', views.updateVenue, name='updateVenue'),
    path('addNote/', views.addNote, name='addNote'),
    path('<int:id>/', views.entity, name='entity')
]

urlpatterns += auth_urls.urlpatterns
