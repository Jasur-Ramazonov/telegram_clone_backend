from datetime import datetime

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    SignUpSerializer,
    UpdateInformationSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    LogoutSerializer,
    UserSerializer,
)
from .models import User, VERIFY


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = SignUpSerializer(user).data
        return Response({
            "success": True,
            "message": "You sign up!",
            "data": data
        },200)


class VerifyCodeView(APIView):

    def post(self,request):
        user = request.user
        code = request.data.get('code',None)
        if user.confirmations.filter(code=code,expiration_time__gte=datetime.now()).exists():
            user.auth_status = VERIFY
            user.save()
            return Response({
                "success": True,
                "message": "Your account verified"
            },status=200)
        else:
            raise PermissionDenied({
                "success": False,
                "message": "Code is invalid"
            })


class GetVerifyCodeView(APIView):

    def get(self,request):
        user = request.user
        if user.confirmations.filter(expiration_time__gte=datetime.now()).exists():
            return Response({
                "success": False,
                "message": "Your code is valid yet please try again!"
            },status=403)
        else:
            user.create_code(user.phone_number)
            return Response({
                "success": True,
                "message": "Your verify code resend!"
            },status=201)


class UpdateInformationView(generics.UpdateAPIView):
    serializer_class = UpdateInformationSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UpdatePhotoView(APIView):

    def put(self,request):
        photo = request.data.get('photo',None)
        user = request.user
        if photo:
            user.photo = photo
            user.save()
            return Response({
                "success": True,
                "message": "Photo uploaded!"
            },status=200)
        else:
            raise ValidationError({
                "success": False,
                "message": "Photo is required to upload!"
            })

    def delete(self,request):
        user = request.user
        photo = user.photo
        if photo:
            user.photo.delete()
            user.photo = None
            user.save()
            return Response({
                "success": True,
                "message": "Photo is deleted!"
            },status=204)
        else:
            raise ValidationError({
                "success": False,
                "message": "Photo is already deleted!"
            })

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response({
            "success": True,
            "message": "You logged in!",
            "data": data
        },200)


class ResetPasswordView(APIView):

    def put(self,request):
        user = request.user
        serializer = ResetPasswordSerializer(instance=user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Your password is reset!",
            "data": serializer.data
        },status=200)


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({
            "success": True,
            "data": data
        },200)

class LogoutView(APIView):

    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({
                "success": False,
                "detail": "No refresh token"
            },401)
        data = {
            "refresh": refresh_token
        }
        serializer = LogoutSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "You logged out!"
        },200)


class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user





