from django.urls import path
# from django.contrib.auth import urls as auth_urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('history/', views.history, name='history'),
]
