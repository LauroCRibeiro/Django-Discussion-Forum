from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .forms import LoginForm,SignUpForm
from .models import ForumThread,ThreadReply,Setting
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic

# SignUp
class SignUpView(generic.CreateView):
    form_class=SignUpForm
    success_url=reverse_lazy('login')
    template_name='registration/signup.html'
# Home Page
def home(request):
    threads=ForumThread.objects.annotate(replies=Count('threadreply'))
    # return HttpResponse(threads)
    return render(request,'home.html',{'threads':threads})

# Get Threads By Tag
def get_by_tag(request,tag):
    threads=ForumThread.objects.filter(tags__contains=tag).annotate(replies=Count('threadreply'))
    # return HttpResponse(threads)
    return render(request,'tag.html',{'threads':threads,'tag':tag})

# Get Threads By User
def get_by_user(request,user):
    threads=ForumThread.objects.filter(user_id=request.user).annotate(replies=Count('threadreply'))
    # return HttpResponse(threads)
    return render(request,'user-threads.html',{'threads':threads,'user':request.user})

# Thread Detail
def thread_detail(request,id):
    detail=ForumThread.objects.get(pk=id)
    detail.views=F('views') + 1
    detail.save()
    replies=ThreadReply.objects.order_by('-id').filter(thread_id=id)
    return render(request,'thread-detail.html',{'detail':detail,'replies':replies})

# Create Thread
@login_required
def create_thread(request):
    return render(request,'create-thread.html')

# Submit thread
@login_required
def submit_thread(request):
    user=request.user
    title=request.POST.get('thread_title')
    detail=request.POST.get('thread_detail')
    tags=request.POST.get('thread_tags')
    thread=ForumThread.objects.create(user_id=user,title=title,description=detail,tags=tags)
    messages.success(request,'New thread has been created.')
    return redirect('create-thread')

# Submit Reply
@login_required
def submit_reply(request,thread_id):
    user=request.user
    thread=ForumThread.objects.get(pk=thread_id)
    title=request.POST.get('reply_title')
    detail=request.POST.get('reply_detail')
    reply=ThreadReply.objects.create(user_id=user,thread_id=thread,title=title,description=detail)
    messages.success(request,'New reply has been created.')
    return redirect('/thread/'+str(thread.id))


# User Login
def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        if form.is_valid():
            cl_d=form.cleaned_data
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username/Password Invalid!!')
    form=LoginForm()
    return render(request,'registration/login.html',{'form':form})

# User Profile
@login_required
def user_profile(request):
    return render(request,'registration/profile.html')

# User Setting
@login_required
def user_setting(request):
    if request.method=='POST':
        user=request.user
        signature=request.POST.get('signature')
        if Setting.objects.filter(user_id=request.user).exists():
            Setting.objects.update(user_id=request.user,signature=signature)
        else:
            Setting.objects.create(user_id=request.user,signature=signature)
        messages.info(request,'Setting has been saved.')
    settings=Setting.objects.filter(user_id=request.user).first()
    return render(request,'registration/setting.html',{'setting':settings})

# User Threads
@login_required
def user_threads(request):
    threads=ForumThread.objects.filter(user_id=request.user)
    return render(request,'registration/threads.html',{'threads':threads})

# User Replies
@login_required
def user_replies(request):
    replies=ThreadReply.objects.filter(user_id=request.user)
    return render(request,'registration/replies.html',{'replies':replies})

# Change Password
@login_required
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Password has been changed')
            return redirect('change-password')
        else:
            messages.error(request,'Something went wrong!!')
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'registration/change-password.html',{'form':form})
    

    
