from django.shortcuts import render,get_object_or_404
from .serializers import LoginSerializer,RegisterSerializer,UserSerializer,FollowersSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Followers
 
     
class LoginView(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user is None:
            return Response({'message': 'hatolik qaytadan uruning'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        data = {
            'tabriklaymiz':'Muvaffaqiyatli login qildingiz',
            "username":request.user.username,
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
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request):
        to_user = User.objects.get(id=request.data['to_user'])
        from_user = request.user
        follow_request = Followers.objects.filter(from_user=from_user).filter(to_user=to_user)

        if not follow_request:
            try:
                Followers.objects.create(from_user=from_user, to_user=to_user)
                data = {
                    "success": True,
                    "message": f"sorov yuborildi  {to_user} ga"
                }
            except:
                data = {
                    "success": False,
                    "message": f" sorov yuborilmadi"
                }
        else:
            data = {
                "success": False,
                "message": "Follow request already sent"
            }
        return Response(data)


class MyNetworksAPIView( APIView):
    def get(self, request):
        networks = Followers.objects.filter(to_user=request.user, is_accepted=False)
        serializer = FollowersSerializers(networks, many=True)
        return Response(serializer.data)   


class MyFollowRequestsApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        follow_requests = Followers.objects.filter(to_user=request.user, is_accepted=False)
        serializer = FollowersSerializers(follow_requests, many=True)

        if follow_requests:
            data = serializer.data
        else:
            data = {
                "success": False,
                "message": "sizda mavjud emas"
            }

        return Response(data)
    

class AcceptFriendRequestView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        id = request.data['follow_request_id']
        try:
            follow_request_user = Followers.objects.get(id=id)
            from_user = follow_request_user.from_user
            main_user = request.user

            follow_request_user.is_accepted = True
            follow_request_user.save()
            main_user.followers.add(from_user)
            from_user.followers.add(main_user)

            data = {
                "success": True,
                "message": f"{from_user.username} is accepted!"
            }
        except:
            data = {
                'success': False,
                'message': "Follow request user doesn't exist"
            }
        return Response(data)

