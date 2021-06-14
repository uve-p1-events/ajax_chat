from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat, name='chatwindow'),
    path('login', views.loginUser, name='loginUser'),
    path('register', views.registerUser, name='registerUser'),
    path('logout', views.logout, name='logout'),
    path('getChatUserInfo', views.getChatUserInfo, name='getChatUserInfo'),
    path('getGroupChatInfo', views.getGroupChatInfo, name='getGroupChatInfo'),
    path('log_message', views.log_message, name='logMessage'),
    path('getChats', views.get_all_chats, name='getChats'),
    path('loadmessages', views.load_previous_messages, name='loadPreviousMessages'),
    path('moderation/', views.pre_moderation_view, name='preModeration'),
    path('getModeratorMsgs', views.get_pre_moderator_chats, name='getpremoderatormsgs'),
    path('approveModeratorMsgs', views.approve_pre_moderator_msgs, name='approveModeratorMsgs'),
]