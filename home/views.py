from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


@login_required(login_url="/")
def index(request):
    post = Post.objects.filter(user=request.user)
    permission = Permission.objects.filter(userpermission = request.user)
    # permission_field = Permission.objects.filter(permission_field='show')
    context = {
        'post':post,
        'permission':permission,
    }
    return render(request, 'home/index.html', context=context)


@login_required(login_url="/")
def upload_file(request):
    if request.method == 'POST':
        filename = request.FILES['filename']
        title = request.POST['title']
        desc = request.POST['desc']
        
        upload_post = Post(user=request.user, title=title, file_field=filename, desc=desc)
        upload_post.save()
        
    return render(request, 'home/upload_file.html')

@login_required(login_url="/")
def detail(request, id):
    post = get_object_or_404(Post, id=id)
    permission = Permission.objects.filter(userpermission=request.user, post=post)
    comments =Comment.objects.filter(post_comment_id=id).order_by('-date')
    context = {
        'post':post,
        'permission':permission,
        'comments':comments
    }
    return render(request, 'home/detail.html', context=context)    