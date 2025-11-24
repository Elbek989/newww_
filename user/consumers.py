from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Message


class ChattyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chat_room"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        if self.scope["user"].is_authenticated:
            user = self.scope["user"]
            username = "Admin" if user.is_superuser else user.username
        else:
            username = "Anon"

        print(f"{username} connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if self.scope["user"].is_authenticated:
            user = self.scope["user"]
            username = "Admin" if user.is_superuser else user.username
        else:
            username = "Anon"
            user = None

        saved_msg = await sync_to_async(Message.objects.create)(
            user=user,
            username=username,
            text=message
        )

        display_name = saved_msg.display_username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": display_name
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))
