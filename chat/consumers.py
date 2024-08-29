import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from textblob import TextBlob
from .models import User, Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # Sentiment value
        blob = TextBlob(message)
        sentiment = blob.sentiment.polarity

        user_id = text_data_json["user"]
        chat_id = text_data_json["chat"]

        chat = await sync_to_async(Chat.objects.get)(pk=chat_id)
        user = await sync_to_async(User.objects.get)(pk=user_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "user": user.username,
                "sentiment": sentiment,
                }
        )
        await sync_to_async(Message.objects.create)(user=user, chat=chat, content=message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        sentiment = event["sentiment"]
        timestamp = datetime.now().strftime("%b. %d, %Y, %I:%M %p")

        if sentiment > 0:
            color = "green"
        elif sentiment < 0:
            color = "red"
        else:
            color = "gray"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message, 
            "user": user, 
            "timestamp":timestamp,
            "color": color,
            }))