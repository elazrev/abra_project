from django.contrib import admin
from django.urls import re_path, path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test-token', views.test_token),
    
    re_path('users-list', views.users_list),
    
    # Connecting to the messages center
    path('messages_center/', include('messages_center.urls')),
    
]
