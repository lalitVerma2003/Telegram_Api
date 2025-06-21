from .models import *
from rest_framework import serializers
# from utils.validator import validate_email

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email','country_code', 'phone_no', 'profile_pic_url', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop("password")  
        user = User(**validated_data) 
        user.set_password(password)  
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


    
class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sessions
        fields = '__all__'