from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from .serializers import TokenObtainPairSerializer, UserUpdateSerializer
from .models import User



class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer



   


   

