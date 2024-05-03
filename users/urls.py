from django.urls import path
from .views import LoginView,RegisterView,AllUsers,FriendRequestAPIView,AcceptFriendRequestView,MyNetworksAPIView,MyFollowRequestsApiView
urlpatterns=[
        path('login/',LoginView.as_view(),name='login'),
        path('register/',RegisterView.as_view(),name='register'),
        path('allusers/',AllUsers.as_view(),name='allusers'),
        path('friendrequest/',FriendRequestAPIView.as_view(),name='friend'),
         path('my-follow-requests/', MyFollowRequestsApiView.as_view()),
        path('acceptFriendRequest/',AcceptFriendRequestView.as_view(),name='accepted'),
        path('mynetworks/',MyNetworksAPIView.as_view(),name='mynetworks'),

]