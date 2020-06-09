import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message, Profile
from datetime import datetime
from django.utils import timezone


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
        input_type = text_data_json['inputtype']
        if input_type == '1':
            message = text_data_json['message']
            username = text_data_json['user']

            user = User.objects.get(username=username)
            date = datetime.now()
            new_message = Message.objects.create(author=user, content=message, roomname=self.room_name, timestamp=date)

            new_message.save()
            timestamp = new_message.timestamp

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
        elif input_type == '2':
            action = text_data_json['action']
            user = text_data_json['user']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'action_message',
                    'action': action,
                    'username': user,
                }
            )
        elif input_type == '3':
            action = text_data_json['action']
            username = text_data_json['user']
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            if action == 'offline':
                profile.is_online = False
                profile.last_seen = timezone.now()
                profile.save()
                s = profile.last_seen
                action = s.strftime("%B")+" "+str(s.day)+", "+str(s.year)+", "+s.strftime("%I:%M %p")
            elif action == 'online':
                profile.is_online = True
                profile.save()
                action = 'Online'

            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'action_message',
                    'action': action,
                    'username': username,
                }
            )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'inputtype': '1',
            'message': message,
            'username': username,
        }))

    async def action_message(self, event):
        action = event['action']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'inputtype': '2',
            'action': action,
            'username': username,
        }))

