from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Message, Chat, Contact

class MessageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    body = serializers.CharField(min_length=1,required=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'body',
            'is_read',
            'chat_id'
        ]

    def validate(self,data):
        print("bu mani datam",data)
        return data

    def create(self, validated_data):
        message = super(MessageSerializer,self).create(validated_data)
        message.save()
        return message

    def update(self, instance, validated_data):
        is_read = validated_data.get("is_read",None)
        body = validated_data.get("body",None)
        if is_read:
            instance.is_read = is_read
        if body:
            instance.body = body
        instance.save()
        return instance


class ChatSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Chat
        fields = [
            'id',
            'creator',
            'user',
        ]

    def create(self, validated_data):
        chat = super(ChatSerializer,self).create(validated_data)
        chat.save()
        return chat


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    owner = serializers.UUIDField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id',
            'owner',
            'contact'
        ]

    def validate(self, data):
        owner = self.context["request"].user
        contact = data.get("contact")
        is_has = Contact.objects.filter(owner=owner,contact=contact).exists()
        if is_has:
            raise ValidationError({
                "message": "Contact can not be duplicate!"
            })
        return data

    def create(self, validated_data):
        contact = super(ContactSerializer,self).create(validated_data)
        contact.save()
        return contact