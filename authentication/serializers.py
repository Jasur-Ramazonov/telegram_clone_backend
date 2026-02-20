from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken

from shared.utilits import check_phone_number, check_username, check_password
from .models import User, DONE

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model= User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username'
        ]

class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
        ]

    def create(self, validated_data):
        user = super(SignUpSerializer,self).create(validated_data)
        user.create_code(validated_data["phone_number"])
        user.save()
        return user

    def validate(self,data):
        phone_number = data.get('phone_number',None)
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({
                "success": False,
                "message": "This phone number is already used!"
            })
        self.check_phone_number(phone_number)
        return data

    @staticmethod
    def check_phone_number(phone_number:str)->bool|None:
        if phone_number:
           is_valid = check_phone_number(phone_number)
           if is_valid:
               return True
           else:
               raise ValidationError({
                   "success": False,
                   "message": "Your phone number is not correct please check it!"
               })
        else:
            raise ValidationError({
                "success": False,
                "message": "You must enter your phone number"
            })

    def to_representation(self, instance):
        data = super(SignUpSerializer,self).to_representation(instance)
        data.update(instance.get_token())
        return data


class UpdateInformationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(max_length=30,required=True)
    last_name = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'password',
            'birth_day'
        ]

    def validate(self, data):
        username = data.get('username',None)
        password = data.get('password',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        if not first_name and not self.check_first_name(first_name):
            raise ValidationError({
                "success": False,
                "message": "first name is invalid!"
            })
        elif last_name:
            if not self.check_last_name(last_name):
                raise ValidationError({
                    "success": False,
                    "message": "last name is invalid!"
                })
        elif not username:
            raise ValidationError({
                "success": False,
                "message": "username is required field"
            })
        elif not check_username(username):
            raise ValidationError({
                "success": False,
                "message": "username is invalid"
            })
        elif User.objects.filter(username=username).exists():
            raise PermissionDenied({
                "success": False,
                "message": "The username is already taken!"
            })
        elif not password:
            raise ValidationError({
                "success": False,
                "message": "password is required field"
            })
        if not check_password(password):
            print("check_password",check_password(password))
            raise ValidationError({
                "success": False,
                "message": "Invalid password"
            })
        return data

    @staticmethod
    def check_first_name(first_name)->bool:
        first_name = str(first_name)
        length = len(first_name)
        if length > 0 or length < 30:
            return True
        elif not first_name[0].isdigit():
            return True
        return False

    @staticmethod
    def check_last_name(last_name)->bool:
        last_name = str(last_name)
        length = len(last_name)
        if length > 0 or length < 30:
            return True
        elif not last_name[0].isdigit():
            return True
        return False

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name',None)
        instance.set_password(validated_data['password'])
        instance.username = validated_data.get('username')
        instance.birth_day = validated_data.get('birth_day',None)
        instance.auth_status = DONE
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


    def validate(self,data):
        phone_number = data.get('phone_number',None)
        password = data.get('password',None)
        user = User.objects.filter(phone_number=phone_number).first()
        data['user'] = user
        if user:
            if not user.check_password(password):
                raise ValidationError({
                    "success": False,
                    "message": "phone number or password is incorrect!"
                })
        if not user:
            raise ValidationError({
                "success": False,
                "message": "phone number or password is incorrect!"
            })
        elif not phone_number:
            raise ValidationError({
                "success": False,
                "message": "phone number is required field!"
            })
        elif not check_phone_number(phone_number):
            raise ValidationError({
                "success": False,
                "message": "phone number is invalid!"
            })
        elif not password:
            raise ValidationError({
                "success": False,
                "message": "password is required field!"
            })
        elif not check_password(password):
            raise ValidationError({
                "success": False,
                "message": "password is invalid!"
            })
        return data

    def to_representation(self, instance):
        data = super(LoginSerializer,self).to_representation(instance)
        print("instance",instance)
        data.update(instance.get('user').get_token())
        return data


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True,min_length=8)


    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def validate(self, data):
        password = data.get("password",None)
        if not password:
            raise ValidationError({
                "success": False,
                "password": "Password is required field!"
            })
        if not check_password(password):
            raise ValidationError({
                "success": False,
                "password": "Password is invalid"
            })
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def create(self, validated_data):
        user = validated_data['user']
        user.create_code()
        return validated_data


    def validate(self,data):
        phone_number = data.get("phone_number",None)
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise ValidationError({
                "success": False,
                "message": "User not found!"
            })
        elif not phone_number:
            raise ValidationError({
                "success": False,
                "message": "Password id required field"
            })
        elif not check_phone_number(phone_number):
            raise ValidationError({
                "success": False,
                "message": "Phone number is invalid!"
            })
        data['user'] = user
        return data

    def to_representation(self, instance):
        data = super(ForgotPasswordSerializer,self).to_representation(instance)
        data.update(instance['user'].get_token())
        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        try:
            token = RefreshToken(self.validated_data['refresh'])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Token is incorrect or deleted already!")


