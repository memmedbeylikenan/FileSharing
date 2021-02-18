from django.urls import path
from .views import *

urlpatterns = [
    # path('user/list')
    path('user/list/<int:file_id>',UserList.as_view()),
    path('permission/list/',PermissionList.as_view()),
    path('permission/create/',PermissionAPI.as_view())

]