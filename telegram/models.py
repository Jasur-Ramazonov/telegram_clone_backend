import uuid

from django.db import models
from django.db.models.constraints import UniqueConstraint

from shared.models import BaseModel
from authentication.models import User

# Create your models here.

class Chat(models.Model):
    id = models.UUIDField(editable=False,unique=True,primary_key=True,default=uuid.uuid4)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_chats')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='other_chats')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['creator','user'],
                name='chat'
            )
        ]


class Message(BaseModel):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="send_messages")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="received_messages")
    chat_id = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name="messages")
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body


class Contact(BaseModel):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='contacts')
    contact = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['owner','contact'],
                name='contact'
            )
        ]

    def __str__(self):
        return f"{self.owner}"
