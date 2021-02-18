from django.shortcuts import render
from rest_framework import RemovedInDRF312Warning
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from home.models import *
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework.response import Response
# Create your views here.


class UserList(ListAPIView):
    def get_queryset(self):
        post_id = self.kwargs.get('file_id')
        users = list(Permission.objects.filter(post_id=post_id).values_list('userpermission',flat=True))
        users.append(self.request.user.id)
        users = User.objects.exclude(id__in=users)
        return users


    authentication_classes = [SessionAuthentication,]
    serializer_class = UserSerializer
   

class PermissionList(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    # users = User.objects.filter(username!=current_user.username)


class PermissionAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,]

    def post(self,request):
        data = request.data
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                Permission.objects.create(post_id=serializer.validated_data['post'],
                            userpermission_id=serializer.validated_data['user'],
                            permission_field=serializer.validated_data['permission']
                            )           
                return Response({'status':'created'},status=200)
            except Exception as e:
                print(e)
                return Response({'status':'error'},status=500)