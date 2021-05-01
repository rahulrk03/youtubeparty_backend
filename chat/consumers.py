from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "{}".format(user_id)

        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver = text_data_json['receiver']
        sender = text_data_json['sender']
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'recieve_group_message',
                'message': message,
                'sender': sender,
                'receiver': receiver

            }
        )

    async def recieve_group_message(self, event):
        message = event['message']
        receiver = event['receiver']
        sender = event['sender']
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                'message': message,
                'sender': sender,
                'receiver': receiver
            }))