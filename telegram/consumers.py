from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer, ChatSerializer
import json
from asgiref.sync import sync_to_async
from authentication.serializers import UserSerializer
from .models import Chat


class ChatConsumer(AsyncWebsocketConsumer):

   async def connect(self):
       self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
       chat = await self.chat_validate_convert(self.chat_id)
       user = self.scope.get("user",None)
       if not user:
           await self.close()
           return
       self.user_id = str(UserSerializer(user).data["id"])
       self.receiver_id = str(chat["creator"] if str(chat["user"]) == str(self.user_id) else chat["user"])
       print("chat",chat)
       self.group = f"user_{self.user_id}"
       await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )
       await self.accept()

   @sync_to_async
   def chat_validate_convert(self,chat_id):
       chat_query = Chat.objects.get(id=chat_id)
       return ChatSerializer(chat_query).data


   @sync_to_async
   def validate_and_save(self,data):
       print("my data",data)
       serializer = MessageSerializer(data=data)
       serializer.is_valid(raise_exception=True)
       serializer.save()

   async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data = json.loads(text_data)
            text_data["sender"] = self.user_id
            text_data["chat_id"] = self.chat_id
            print("text data",text_data)
            await self.validate_and_save(text_data)
            await self.channel_layer.group_send(
                f"user_{self.receiver_id}",
                {
                    "type": "chat_message",
                    "message": text_data["body"],
                    "user": f"{self.user_id}"
                }
            )
            print("salom hammaga")
            return
        await self.close()

   async def chat_message(self,event):
        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "user": event["user"]
                })
        )

   async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.receiver,
            self.channel_name
        )