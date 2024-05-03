from rest_framework import serializers
from .models import User,Followers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name','last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password', 'confirm_password']
         

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(" Passworlarni bir xil kiriting")
        return data

class FollowersSerializers(serializers.ModelSerializer):
    class Meta():
        model=Followers
        fields=['from_user','to_user','is_accepted']