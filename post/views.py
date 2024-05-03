from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer,CommentSerializer,LikeSerializer
from .models import Post,Comment,Like
from users.models import User
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError


class PostView(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        user=request.user
        request.data['user']=user.id
        serializer=PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class OneUserPostApiView(APIView):
    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            posts = Post.objects.filter(user=user)
            serializer = PostSerializer(posts, many=True)
        except:
            data={
                 "message":"Bunday user mavjud emas"
                }
            raise ValidationError(data)

        return Response(serializer.data)
    
class UpdatePostApiView(APIView):
    permission_classes=(IsAuthenticated,)
    def put(self,request,id):
        post=get_object_or_404(Post,id=id)
        user=request.user
        request.data['user']=user.id
        serializer=PostSerializer(instance=post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data={
            "message":"Muvaffaqiyatli upadate qildingiz ",
            "post":serializer.data
        }
        return Response(data)

class DeletePostApiView(APIView):
    permission_classes=(IsAuthenticated,)
    def delete(self,request,id):
        try:
            post=get_object_or_404(Post,id=id)

        except Post.DoesNotExist:
            return Response({"message":"Bunday Model yoki post mavjud emas"})
        post.delete()
        return Response({"message":"Muvaffaqiyatli O'chirildi"})
    
    
class AllPost(APIView):
    def get(self,request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response (serializer.data)


class CommentView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        
        serializer=CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data={
            "message":"Comment",
            "comments":serializer.data
        }
        return Response(data)



class AllCommentView(APIView):
    def get(self,request):
        comment=Comment.objects.all()
        serializer=CommentSerializer(comment,many=True)
        return Response(serializer.data)

class DeleteCommentView(APIView):
    permission_classes=(IsAuthenticated,)
    def delete(self,request,id):
        try:
            coment=Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"message":"Bunday model yoki comment mavjud emas"})
        coment.delete()
        return Response({"message":"Muvaffaqiyatli o'chirildi"})
    

class LikeView(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
         
        serializer=LikeSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        data={
            "message":"Likes",
            "Like":serializer.data,
        }
        return Response(data)

class LikesApiView(APIView):
    def get(self,request):
        likes=Like.objects.all()
        serializer=LikeSerializer(likes,many=True)
        return Response(serializer.data)
