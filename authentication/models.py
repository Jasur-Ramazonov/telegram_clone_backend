import random
import uuid

from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel


# Create your models here.

NEW, VERIFY, GET_INFORMATION, DONE = ("new","verify","get information","done")
EXPIRATION_TIME = 2

class User(AbstractUser,BaseModel):
    AUTH_STATUS = (
        (NEW,NEW),
        (VERIFY,VERIFY),
        (GET_INFORMATION,GET_INFORMATION),
        (DONE,DONE),
    )

    phone_number = models.CharField(unique=True,null=False,blank=False)
    birth_day = models.DateField(null=True,blank=True)
    photo = models.ImageField(upload_to='user_photo',null=True,blank=True,validators=[FileExtensionValidator(['jpeg','jpg','png'])])
    auth_status = models.CharField(default=NEW,choices=AUTH_STATUS)

    def __str__(self):
        return f"{self.id}"

    def create_code(self,phone_number:str=None):
        code = "".join([str(random.randint(0,9)) for _ in range(4)])
        UserConfirmation.objects.create(user_id=self.id,code=code)
        print("to:",phone_number)
        print("code",code)

    def create_temp_username(self):
        if not self.username:
            temp_username = f"username-{uuid.uuid4().__str__().split("-")[-1]}"
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"username-{uuid.uuid4().__str__().split("-")[-1]}"
            self.username = temp_username

    def create_temp_password(self):
        if not self.password:
            temp_password = "Password12@"
            self.set_password(temp_password)


    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh_token": str(refresh),
            "access": str(refresh.access_token),
        }

    def clean(self):
        self.create_temp_password()
        self.create_temp_username()

    def save(self,*args,**kwargs):
        self.clean()
        super(User,self).save(*args,**kwargs)



class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='confirmations')

    def __str__(self):
        return str(self.user.__str__())

    def save(self,*args,**kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
        super(UserConfirmation,self).save(*args,**kwargs)

