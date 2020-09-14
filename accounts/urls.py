from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.dashboard, name='dashboard'),
    path('user/', views.userPage, name='user-page'),
    path('account/<str:id>/', views.account, name='customer')
]
