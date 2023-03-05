from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

class UserCreateSerializer(BaseUserCreateSerializer):
    is_verified = serializers.BooleanField(read_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'phone_number',  'password', 'is_verified']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'phone_number', 'is_verified', 'address','profile_picture']


class UserUpdateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'phone_number', 'address', 'profile_picture']


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        user_dict = user.get_user()
        token = super().get_token(user)

         # Add custom claims
        token['username'] = user.username
        token['id'] = user.id
        token['phone_number'] = user.phone_number
        token['email'] = user.email
        token['is_verified'] = user.is_verified
        token['address'] = user_dict['address']
        token['profile_picture'] = user_dict['profile_picture']
        
        # ...

        return token


    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = self.user.get_user()

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


