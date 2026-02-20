from django.contrib import admin
from .models import User,UserConfirmation

# Register your models here.
admin.site.register(UserConfirmation)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id','username']
    search_fields = ['username','first_name']
