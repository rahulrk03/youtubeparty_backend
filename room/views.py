from random import randint
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from room.db import database
from datetime import datetime as dt
from .serializers import JoinRoomSerializer


class CreateRoomAPI(APIView):
    def post(self, request):
        try:
            room_name = str(randint(00000000, 99999999))
            exist_room = database['room'].find_one({"status": "Active",
                                                    "room_name": room_name})
            if not exist_room:
                database['room'].insert_one({"room_name": room_name,
                                             "status": "Active",
                                             "created_time": dt.now(),
                                             "total_members": 0})
                return Response({"data": room_name,
                                 "message": "Success"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"data": None,
                                 "message": "Please Try Again"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Error"},
                            status=status.HTTP_400_BAD_REQUEST)


class JoinRoomAPI(APIView):
    def post(self, request):
        try:
            serializer = JoinRoomSerializer(data=request.data)
            if serializer.is_valid():
                exist_room = database['room'].find_one({"status": "Active",
                                                        "room_name": request.data['room_name']})
                if exist_room:
                    exist_room['total_members'] += 1
                    database['room'].update({"_id": exist_room['_id']},
                                            {"$set": exist_room})
                return Response({"data": None,
                                 "message": "Welcome"},
                                status=status.HTTP_200_OK)
            return Response({"data": serializer.errors,
                             "message": "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Error"},
                            status=status.HTTP_400_BAD_REQUEST)