from django.urls import path
from chat.views import user_list

urlpatterns = [
    path('',  user_list, name='user_list'),
]