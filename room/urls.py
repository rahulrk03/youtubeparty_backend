from django.urls import path
from room.views import CreateRoomAPI, JoinRoomAPI

urlpatterns = [
    path('createRoom/', CreateRoomAPI.as_view(), name='create_room'),
    path('joinRoom/', JoinRoomAPI.as_view(), name='join_room')
]