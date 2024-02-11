from django.urls import re_path
from . import views

urlpatterns = [
    re_path('all_messages', views.all_messages),
    re_path('unread_messages', views.unread_messages),
    re_path(r'^message_details/(?P<pk>\d+)/$', views.message_details),
    re_path(r'^message_delete/(?P<pk>\d+)/$', views.delete_message),
    
    re_path('create_message/', views.create_message)
]
