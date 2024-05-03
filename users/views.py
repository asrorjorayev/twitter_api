from django.shortcuts import render,get_object_or_404
from .serializers import LoginSerializer,RegisterSerializer,UserSerializer,FollowersSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Followers
from django.contrib.auth.mixins import LoginRequiredMixin
     
class LoginView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user is None:
            return Response({'message': 'hatolik qaytadan uruning'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        data = {
            'tabriklaymiz':'Muvaffaqiyatli login qildingiz',
            'refres': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(data)

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

         
        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)
        data = {
            'tabriklaymiz':'Muvaffaqiyatli register qildingiz',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)

class AllUsers(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
    

class FriendRequestAPIView(APIView):
     

    def post(self, request, id):
        to_user = get_object_or_404(User, id=id)
        from_user = request.user

        friend_request, created = Followers.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            message = 'Dostlik so\'rovi muvaffaqiyatli yuborildi!'
        else:
            message = 'Dostlik so\'rovi avval yuborilgan'
        
        response_data = {
            'success': True,
            'message': message,
             
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class MyNetworksAPIView( APIView):
    def get(self, request):
        networks = Followers.objects.filter(to_user=request.user, is_accepted=False)
        serializer = FollowersSerializers(networks, many=True)
        return Response(serializer.data)   
    
class AcceptFriendRequestView(APIView):
     
    def post(self, request, id):
        friend_request = get_object_or_404(Followers, id=id)
        from_user = friend_request.from_user

        main_user = request.user
        main_user.friends.add(from_user)

        friend_request.delete()

        return Response({'message': 'Dostlik sorovi muvaffaqiyatli qabul qilindi'}, status=status.HTTP_200_OK)