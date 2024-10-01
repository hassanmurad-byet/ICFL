from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Login.forms import ProfilePic
# Create your views here.

def sign_up(request):
    registered =False
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            return HttpResponse("Password not same")
        data = User.objects.create_user(username,email,pass1)
        data.save()
        registered = True
            
    dict = {'registered': registered}
    return render(request, 'Login/signup.html', context=dict)



def Login(request):

    Login = False
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
           Login = True
    dict = {'Login': Login}
    return render(request, 'Login/login.html', context=dict)


@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    return render(request, 'Login/profile.html', context={})


# @login_required
# def user_change(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
        
#         user = request.user
#         user.username = username
#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         user.save()
#         return HttpResponseRedirect(reverse('App_login:profile'))
#     else:
#         return render(request, 'App_login/cngprofile.html', {'user': request.user})
        
    
# @login_required  
# def update_password(request):
#     current_user = request.user
#     changed = False
#     form = PasswordChangeForm(current_user)
#     if request.method =='POST':
#         form = PasswordChangeForm(current_user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             changed = True

#     return render(request, 'App_login/changepass.html', context={'form':form, 'changed': changed})


@login_required
def add_propic(request):
    form = ProfilePic()
    if request.method =='POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user =request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('Login:profile'))
    return render(request, 'Login/pro_pic.html', context={'form': form})



@login_required
def change_propic(request):
    form = ProfilePic(instance = request.user.users)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance = request.user.users)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login:profile'))
    return render(request, 'Login/pro_pic.html',  {'form':form})