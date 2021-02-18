from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('upload_file/', upload_file, name='upload_file'),
    path('detail/<int:id>', detail, name='detail'),
]