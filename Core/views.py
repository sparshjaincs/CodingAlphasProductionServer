from django.shortcuts import render
from django.http import HttpResponse
import json
from discuss.models import Quora
from discuss.models import Anwsers as AnsModel
from discuss.models import Comment as CommentSystem
from Core.models import *
#from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import date
from discuss.jobs import Jobs
from .forms import *
class MyPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = 'Core/snippets/password_reset.html'

    # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.is_anonymous
    def test_func(self):
        return self.request.user.is_anonymous  

# Create your views here.
def homepage(request):
    context = {}
    if request.user.is_authenticated:
        context['home'] = Homepage_Activity.objects.all().order_by('-id')
        context['day'] = date.today()
        context['activity'] = activity.objects.all().order_by('-id')[:5]
        #job = Jobs('SDE',"",1)
        #data = job.select()
        #context['jobs'] = data[:5]

        return render(request,"Core/homepage.html",context)
    else:
        return render(request,"Core/frontend.html")

def like(request):
    method = request.GET.get('method')
    instance = request.GET.get('instance')
    if method == 'discuss':
        ins = Quora.objects.get(id = instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    elif method == 'discussanwser':
        ins = AnsModel.objects.get(id=instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1  
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    elif method == 'discusscomment':
        ins = CommentSystem.objects.get(id=instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1  
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()


    return HttpResponse(json.dumps([status,likecount,dislikecount]))


def dislike(request):
    method = request.GET.get('method')
    instance = request.GET.get('instance')
    if method == 'discuss':
        ins = Quora.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    elif method == 'discussanwser':
        ins = AnsModel.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    elif method == 'discusscomment':
        ins = CommentSystem.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    return HttpResponse(json.dumps([status,dislikecount,likecount]))


def follow(request):
    us = request.GET.get('method')
    ins = User.objects.get(username = us)
    if request.user in ins.profile.following.all():
        ins.profile.following.remove(request.user)
        status = 0
    else:
        ins.profile.following.add(request.user)
        status = 1
    if ins in request.user.profile.follow.all():
        request.user.profile.follow.remove(request.user)
    else:
        request.user.profile.follow.add(request.user)
    return HttpResponse(json.dumps([status]))

def mark(request):
    method = request.GET.get('method')
    ins = request.GET.get('ins')
    if method == 'discuss':
        instance = Profile.objects.get(user = request.user)
        ins = Quora.objects.get(id = ins)
        if ins in instance.quora_discuss.all():
            instance.quora_discuss.remove(ins)
            status = 0
        else:
            instance.quora_discuss.add(ins)
            status = 1
    

    return HttpResponse(json.dumps([status]))

def profile(request,user):
    context = {}
    method = request.GET.get('method')
    if method is None or method == 'Profile':
        context['method'] = 'Profile'
    elif method == 'Timeline':
        context['method'] = 'Timeline'
        context['home'] = Homepage_Activity.objects.filter(user = request.user).order_by('-id')
        context['activity'] = activity.objects.all().order_by('-id')[:5]
    elif method == 'Photos':
        context['method'] = 'Photos'
        context['home'] = Homepage_Activity.objects.filter(user = request.user,category = 'Photo').order_by('-id')
    elif method == 'Videos':
        context['method'] = 'Videos'
        context['home'] = Homepage_Activity.objects.filter(user = request.user,category = 'Video').order_by('-id')
    elif method == 'Articles':
        context['method'] = 'Articles'
        context['home'] = Homepage_Activity.objects.filter(user = request.user,category = 'Blog').order_by('-id')
    else:
        context['method'] = method
    context['article'] = Articles.objects.filter(user_name2 = request.user).order_by('-date_Publish','-time')
    context['post'] = Quora.objects.filter(user = request.user).order_by("-created")
    return render(request,'Core/profile.html',context)


def photo_upload(request):
    if request.method == 'POST':
        data = request.FILES.getlist('photo_files')
        text = request.POST.get('photo_text')
        tags = request.POST.get('photo_taggs')
        ins = Photo(user = request.user,description = text,tags = tags)
        ins.save()
        for i in data:
            ins1 = Photo_Image(instance = ins,image = i)
            ins1.save()
        ins1 = Homepage_Activity(user=request.user,category = 'Photo',photo = ins)
        ins1.save()
        ins2 = activity(user = request.user,activity_icon = "fa fa-cloud-upload",user_activity=f"You have shared a <a href='/activities/photo/{ins.id}/'>photo</a>.")
        ins2.save()
        return HttpResponse(json.dumps("Success"))
    else:
        return HttpResponse(json.dumps("Error"))


def video_upload(request):
    if request.method == 'POST':
        data = request.FILES.get('video_file')
        text = request.POST.get('video_text')
        tags = request.POST.get('video_tags')
        ins = Video(user = request.user,description = text,tags = tags,video_file = data)
        ins.save()
        ins1 = Homepage_Activity(user=request.user,category = 'Video',video = ins)
        ins1.save()
        ins2 = activity(user = request.user,activity_icon = "fa fa-cloud-upload",user_activity=f"You have shared a <a href='/activities/video/{ins.id}/'>video</a>.")
        ins2.save()
        return HttpResponse(json.dumps("Success"))
    else:
        return HttpResponse(json.dumps("Error"))

def post_upload(request):
    if request.method == 'POST':
        text = request.POST.get('editor1')
        tags = request.POST.get('post_tags')
        image = request.FILES.getlist('post_photo_files')
        video = request.FILES.get('post_video_file')
        document = request.FILES.get('post_doc_file')
    
        ins = Post(user = request.user,description = text,tags = tags,video_file = video,attachment = document)
        ins.save()
        for i in image:
            ins1 = Post_Image(instance = ins,image = i)
            ins1.save()
        ins1 = Homepage_Activity(user=request.user,category = 'Post',post = ins)
        ins1.save()
        ins2 = activity(user = request.user,activity_icon = "fa fa-cloud-upload",user_activity=f"You have shared a <a href='/activities/post/{ins.id}/'>post</a>.")
        ins2.save()
        return HttpResponse(json.dumps("Success"))
    else:
       return HttpResponse(json.dumps("Error"))


