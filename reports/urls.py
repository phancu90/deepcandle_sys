# -*- coding: utf-8 -*-
from django.urls import path
from . import views
app_name = 'page'

urlpatterns = [
    path('', views.report_page, name='report_page'),
]