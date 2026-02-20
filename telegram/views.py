from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q

from .serializers import (
    MessageSerializer,
    ChatSerializer,
    ContactSerializer
)
from .models import Chat, Message, Contact

from authentication.serializers import UserSerializer
from authentication.models import User

# Message views
class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class MessageDestroyView(generics.DestroyAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = UserSerializer(self.request.user)
        return Message.objects.filter(sender=user.id)

class MessageUpdateView(generics.UpdateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = UserSerializer(self.request.user).data
        return Message.objects.filter(sender=user["id"])

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.request.path.split('/')[-2]
        return Message.objects.filter(chat_id=chat_id)


# Chat views
class CreateChatView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class DestroyChatView(generics.DestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

class ListChatView(APIView):

    def get(self,request):
        user_id = UserSerializer(request.user).data["id"]
        other_user_ids = [ChatSerializer(chat).data["user"] if str(chat.creator.id) == str(user_id) else ChatSerializer(chat).data["creator"] for chat in  Chat.objects.filter(Q(creator=user_id) | Q(user=user_id))]
        users = [User.objects.filter(id=user_id) for user_id in other_user_ids]
        user_first_names = [UserSerializer(user[0]).data['first_name'] if user else "" for user in users]
        return Response({"data":user_first_names},200)

class CheckChatsView(APIView):

    def post(self,request):
        current_user_id = UserSerializer(request.user).data["id"]
        user_id = request.data["user_id"]
        if not current_user_id or not user_id:
            return Response({
                "success": False,
                "message": "current_user_id and user_id are required!"
            },400)
        current_user_query = User.objects.filter(id=current_user_id).first()
        user_query = User.objects.filter(id=user_id).first()
        if not current_user_query or not user_query:
            return Response({
                "success": False,
                "message": "User not found!"
            },400)
        chat_query = Chat.objects.filter(Q(creator=current_user_id,user=user_id) | Q(creator=user_id,user=current_user_id)).first()
        if not chat_query:
            return Response({
                "success": True,
                "message": "Chat is not found"
            },200)
        else:
            return Response({
                "success": True,
                "message": "Chat is found",
                "data": ChatSerializer(chat_query).data
            },200)


# Contact view

class CreateContactView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(owner=self.request.user)

class DestroyContactView(generics.DestroyAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        owner_username = self.request.user
        owner_instance = User.objects.get(username=owner_username)
        owner = UserSerializer(owner_instance).data
        print(owner)
        return Contact.objects.filter(owner=owner)




# Other views
class GetUserView(APIView):

    def post(self,request):
        data = request.data
        username = data.get("username",None)
        if not username:
            return Response({
                "success": False,
                "message": "username is required field!"
            },400)
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({
                "success": False,
                "message": "user not found!"
            },400)
        data = UserSerializer(user).data
        return Response({
            "success": True,
            "data": data
        },200)


class SearchUsersView(APIView):

    def post(self,request):
        searched_word = request.data.get("searched_word",None)
        user_id = UserSerializer(request.user).data["id"]
        if not searched_word:
            return Response({
                "success": False,
                "detail": "Nothing searched!"
            },400)
        user_queries = User.objects.filter(Q(username__icontains=searched_word) | Q(first_name__icontains=searched_word)).exclude(id=user_id)
        users = [{"id":UserSerializer(user).data["id"],"first_name":UserSerializer(user).data["first_name"],"username":UserSerializer(user).data["username"]} for user in user_queries]
        return Response({
            "data": users
        },200)


