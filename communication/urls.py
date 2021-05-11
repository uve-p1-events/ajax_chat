from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.loginUser, name='loginUser'),
    path('register', views.registerUser, name='registerUser'),
    path('logout', views.logout, name='logout'),
    path('chat', views.chat, name='chatwindow'),
    path('log_message', views.log_message, name='logMessage'),
    path('getChats', views.get_all_chats, name='getChats'),
    path('test', views.test, name='test'),
]