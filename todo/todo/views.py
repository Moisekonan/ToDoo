from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo.models import TODOO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return redirect('signup')

def signup(request):
    if request.method == 'POST':
        user_name, emailId, pwd = request.POST.get('fnm'), request.POST.get('emailid'), request.POST.get('pwd')
        print(user_name, emailId, pwd)
        if User.objects.filter(username=user_name).exists():
            print('Username already exists')
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })
        new_user = User.objects.create_user(
            username=user_name, 
            email=emailId, 
            password=pwd
        )
        new_user.save()
        return redirect('login')
    return render(request, 'signup.html')

def loginn(request):
    print('Login Page')
    if request.method == 'POST':
        user_name, pwd = request.POST.get('fnm'), request.POST.get('pwd') 
        user = authenticate(request, username=user_name, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('todopage') 
        else:
            return redirect('login')
    return render(request, 'login.html')

@login_required
def todo(request):
    print('todo page')
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = TODOO(title=title, user=user)
        obj.save()
        response = TODOO.objects.filter(user=user).order_by('-date')
        return redirect('todopage', {'response': response})
    response = TODOO.objects.filter(user=user).order_by('-date')
    return render(request, 'todo.html', {'response': response})

@login_required
def edit_todo(request, id_todo):
    if request.method == 'POST':
        upd_title = request.POST.get('title')
        obj = TODOO.objects.get(id_todo=id_todo)
        obj.title = upd_title
        obj.save()
        return redirect('todopage')
    obj = TODOO.objects.get(id_todo=id_todo)
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required
def delete_todo(request, id_todo):
    obj = TODOO.objects.get(id_todo=id_todo)
    obj.delete()
    return redirect('todopage')

def signout(request):
    logout(request)
    return redirect('login')