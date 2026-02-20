from django.contrib import admin
from .models import Message, Chat, Contact

# Register your models here.
admin.site.register(Message)
admin.site.register(Contact)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['id','creator','user']