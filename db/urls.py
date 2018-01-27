from django.urls import path
from django.contrib.auth import urls as auth_urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newaccount/', views.newAccount, name='newAccount'),
    path('createaccount/', views.createAccount, name='createAccount'),
    path('newbatch/', views.newBatch, name='newBatch'),
    path('createbatch/', views.createBatch, name='createBatch'),
    path('batches/', views.batches, name='batches'),
    path('submit/', views.submit, name='submit'),
    path('musicForm/', views.musicForm, name='musicForm'),
    path('confirm/<int:id>/', views.confirmProposal, name='confirmProposal'),
    path('addtobatch/<int:batchid>/<int:memberid>/', views.addToBatch, name='addToBatch'),
    path('<int:id>/', views.entity, name='entity')
]

urlpatterns += auth_urls.urlpatterns
