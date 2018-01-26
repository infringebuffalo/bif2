from django.urls import path
from django.contrib.auth import urls as auth_urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newaccount/', views.newAccount, name='newAccount'),
    path('createaccount/', views.createAccount, name='createAccount'),
    path('submit/', views.submit, name='submit'),
    path('musicForm/', views.musicForm, name='musicForm'),
    path('confirm/<int:id>/', views.confirmProposal, name='confirmProposal'),
    path('<int:id>/', views.proposal, name='proposal')
]

urlpatterns += auth_urls.urlpatterns
