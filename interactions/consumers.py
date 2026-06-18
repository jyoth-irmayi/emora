import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage,Notification
from accounts.models import User 

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope['url_route']['kwargs']['room_id']

        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    @database_sync_to_async
    def save_message(self, room_id, user_id, content):

        room = ChatRoom.objects.get(id=room_id)

        user = User.objects.get(id=user_id)

        ChatMessage.objects.create(
            room=room,
            sender=user,
            content=content
        )


    async def receive(self, text_data):
        if await self.room_expired():

            await self.send(
                text_data=json.dumps({
                    "error": "Chat expired"
                })
            )

            await self.close()

            return
        
        data = json.loads(text_data)

        message = data['message']

        username = data['username']

        # save message in database
        await self.save_message(
            self.room_id,
            self.scope["user"].id,
            message
        )

        await self.create_notification(
            self.room_id,
            self.scope["user"].id
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )


    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                'message': event['message'],
                'username': event['username']
            })
        )

    @database_sync_to_async
    def room_expired(self):

        room = ChatRoom.objects.get(
            id=self.room_id
        )

        if timezone.now() > room.expires_at:

            room.is_active = False
            room.save()

            return True

        return False

    @database_sync_to_async
    def create_notification(self, room_id, sender_id):

        room = ChatRoom.objects.get(id=room_id)

        if room.user1.id == sender_id:
            receiver = room.user2
        else:
            receiver = room.user1

        notification = Notification.objects.filter(
            receiver=receiver,
            sender_id=sender_id,
            room=room,
            is_read=False
        ).first()

        if notification:

            notification.message = "Someone sent you a new message 💬"
            notification.is_read = False
            notification.updated_at = timezone.now()
            notification.save()

        else:
            Notification.objects.create(
                receiver=receiver,
                sender_id=sender_id,
                room=room,
                message="Someone sent you a new message 💬"
            )