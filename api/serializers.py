from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import request, routers, serializers, viewsets
from home.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class PermissionSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100,required=True)
    permission = serializers.CharField(max_length=100,required=True)
    post = serializers.CharField(max_length=10,required=True)

    def validate_user(self,value):
        print(value)
        if User.objects.filter(id=value).exists() == False:
            raise serializers.ValidationError("This user dont exists")
        return value
    
    def validate_permission(self,value):
        if value not in map(lambda x:x[0],Permission_field):
            raise serializers.ValidationError('This permission dont exists')
        return value
    
    




        