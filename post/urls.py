from django.urls import path
from .views import PostView,AllPost,CommentView,AllCommentView,LikeView,LikesApiView,UpdatePostApiView,DeletePostApiView,DeleteCommentView,OneUserPostApiView
urlpatterns=[
    path('post/',PostView.as_view()),
    path('allpost/',AllPost.as_view()),
    path('update-post/<int:id>/',UpdatePostApiView.as_view()),
    path('delete-post/<int:id>/',DeletePostApiView.as_view()),
    path('one-post/<int:id>/',OneUserPostApiView.as_view()),

    path('create-comment/',CommentView.as_view()),
    path('all-comment/',AllCommentView.as_view()),
    path('delete-comment/',DeleteCommentView.as_view()),
    
    path('create-like/',LikeView.as_view()),
    path('all-like/',LikesApiView.as_view()),
   

]