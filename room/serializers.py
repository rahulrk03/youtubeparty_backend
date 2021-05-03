from rest_framework import serializers


class JoinRoomSerializer(serializers.Serializer):
    room_name = serializers.CharField(required=True)