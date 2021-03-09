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
    context['article'] = Articles.objects.filter(user_name2 = request.user).order_by('-date_Publish','-time')
    context['post'] = Quora.objects.filter(user = request.user).order_by("-created")
    return render(request,'Core/profile.html',context)
