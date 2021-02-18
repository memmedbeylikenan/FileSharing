from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def login(request):
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['psw']

        user = auth.authenticate(username=username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, 'account/login.html')

    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    

def register(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['psw']
        repassword = request.POST['psw-repeat']
       
        if password == repassword:
            if User.objects.filter(username=username).exists():
                print('bu username-le qeydiyyatdan kecilib')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    print('bu emaille qeydiyyatdan kecilib')
                    return redirect('register')
                else:
                    #create new user
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    print('Yeni user elave edilmiwdir')
                    return redirect('login')

        else:
            print('parol eyni deyil')
            return redirect('register')
    else:
        return render(request, 'account/register.html') 
