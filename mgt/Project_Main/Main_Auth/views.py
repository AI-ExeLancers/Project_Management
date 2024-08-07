from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
import json
from .models import User
from .forms import RegisterForm, LoginForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .producer_user_created import ProducerUserCreated
producerUserCreated = ProducerUserCreated()
class RegisterUser(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            producerUserCreated.publish("User Created Method",json.dumps(serializer.validated_data))
            print(serializer.validated_data)

            data = serializer.save()
            data.save()

          
            return Response({
                'msg':"Registration successful !!!",
                'status': status.HTTP_201_CREATED,

            })
        return Response({
                'msg':serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST,
        })
        
class LoginUser(APIView):
    def post(self,request):
        serializer =LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data
        
            refresh =  RefreshToken.for_user(username)
            access_token = str(refresh.access_token)
            
            refresh_token = str(refresh)
            user = User.objects.get(username=username)
            user.user_refresh_token = refresh_token
            user.save()
            
            return Response({
                'msg':"Login Successful !!!",
                'status': status.HTTP_200_OK,
                'access_token':access_token,
                'Token': refresh_token
            })
        return Response({
                'msg':serializer.error_messages,
                'status': status.HTTP_400_BAD_REQUEST,
        })

class ProtectedView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request):
         user = request.user
         serializer = RegisterSerializer(user)
         return Response({
             "data":serializer.data
         })

