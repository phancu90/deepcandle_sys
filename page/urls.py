# -*- coding: utf-8 -*-
from django.urls import path
from . import views
app_name = 'page'

urlpatterns = [
    path('', views.home_page, name='home_page'),
]