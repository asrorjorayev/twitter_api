from rest_framework import serializers
from .models import Post,Comment,Like

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['user','content','discription','creted_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['post','user','comment_text','created_at']

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Like
        fields=['post','user','created_at']