# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        videoUrl = text_data_json.get('videoUrl')
        message = text_data_json.get('message')
        playStatus= text_data_json.get('playStatus')
        print(text_data_json)
        if videoUrl:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_url',
                    'videoUrl': videoUrl,
                }
            )
        elif message:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        elif playStatus:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'play_status',
                    'playStatus': playStatus,
                }
            )

    async def play_status(self, event):
        playStatus = event['playStatus']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'playStatus': playStatus,
        }))

    async def video_url(self, event):
        videoUrl = event['videoUrl']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'videoUrl': videoUrl,
        }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
