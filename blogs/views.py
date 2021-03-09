from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from Core.models import Homepage_Activity
# Create your views here.
def homepage(request):
    context = {}
    data = Articles.objects.filter(status = 'published').order_by('-date_Publish','-time')
    if len(data) < 7:
        context['inbox'] = data[:6]
    elif len(data) < 11:
        context['carousel'] = data[:4]
        context['inbox'] = data[4:10]
    elif len(data) < 16:
        context['carousel'] = data[:4]
        context['inbox'] = data[4:10]
        context['box'] = data[10:16]
    else:
        context['carousel'] = data[:4]
        context['inbox'] = data[4:10]
        context['box'] = data[10:16]
        context['list'] = data[16:]

    return render(request,'blogs/homepage.html',context)

def create(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            ins = form.save(commit = False)
            ins.user_name2 = request.user
            data = form.cleaned_data['content'] 
            title = form.cleaned_data['title'].lower().replace(" ","-")
            ins.link = f"/blog/{title}/{ins.id}/"
            ins.status = 'draft'
            ins.save()
            home = Homepage_Activity(category = 'Blog',blog = ins)
            home.save()
            return HttpResponseRedirect(f'/blog/preview/content/{ins.id}/')
        else:
            context['error'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    context['data'] = Articles.objects.filter(user_name2 = request.user)
    return render(request,'blogs/create.html',context)

def inside(request,title,id):
    context = {}
    data = Articles.objects.get(id = id)
    context['data'] = data
 
    return render(request,'blogs/inside.html',context)
def preview(request,ids):
    context = {}
    context['data'] = Articles.objects.get(id = ids)
    return render(request,'blogs/preview.html',context)

def post(request,ids):
    ins = Articles.objects.get(id = ids)
    ins.status = 'published'
    ins.save()
    return HttpResponseRedirect("/blog/")

def edit(request,ids):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        
        ids = request.POST.get("iding")
        ins = Articles.objects.get(id = ids)
        ins.user_name2 = request.user
        data = request.POST.get("content")
        ins.content = data
        ins.tags = request.POST.get("tags")
        ins.title = request.POST.get("title")
        if not request.FILES.get('image') is None:
            ins.image = request.FILES.get('image')
        if not request.FILES.get('video') is None:
            ins.video = request.FILES.get("video")
        ins.status = 'draft'
        ins.quora = request.POST.get("quora")
        ins.facebook = request.POST.get("facebook")
        ins.medium = request.POST.get("medium")
        ins.instagram = request.POST.get("instagram")
        ins.twitter = request.POST.get("twitter")
        ins.other = request.POST.get("other")
        ins.description = request.POST.get('description')
        ins.save()
        return HttpResponseRedirect(f'/blog/preview/content/{ins.id}/')
        
    else:
        data = Articles.objects.get(id = ids)
        context['ids'] = data.id
        form = Article_form(initial = model_to_dict(data))
    context['form'] = form
    context['data'] = Articles.objects.filter(user_name2 = request.user)
    context['edit'] = True
    return render(request,'blogs/create.html',context)

def draft(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            ins = form.save(commit = False)
            ins.user_name2 = request.user
            data = form.cleaned_data['content'] 
            title = form.cleaned_data['title'].lower().replace(" ","-")
            ins.link = f"/blog/{title}/{ins.id}/"
            ins.status = 'draft'
            ins.description = form.cleaned_data['description']
            ins.save()
            return HttpResponseRedirect(f'/blog/')
        else:
            context['error'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    context['data'] = Articles.objects.filter(user_name2 = request.user)
    return render(request,'blogs/create.html',context)

def drafted(request,ids):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        
        ids = request.POST.get("iding")
        ins = Articles.objects.get(id = ids)
        ins.user_name2 = request.user
        data = request.POST.get("content")
        ins.content = data
        ins.tags = request.POST.get("tags")
        ins.title = request.POST.get("title")
        if not request.FILES.get('image') is None:
            ins.image = request.FILES.get('image')
        if not request.FILES.get('video') is None:
            ins.video = request.FILES.get("video")
        ins.status = 'draft'
        ins.quora = request.POST.get("quora")
        ins.facebook = request.POST.get("facebook")
        ins.medium = request.POST.get("medium")
        ins.instagram = request.POST.get("instagram")
        ins.twitter = request.POST.get("twitter")
        ins.other = request.POST.get("other")
        ins.description = request.POST.get("description")
        ins.save()
        return HttpResponseRedirect(f'/blog/')
        
    else:
        data = Articles.objects.get(id = ids)
        context['ids'] = data.id
        form = Article_form(initial = model_to_dict(data))
    context['form'] = form
    context['data'] = Articles.objects.filter(user_name2 = request.user)
    context['edit'] = True
    return render(request,'blogs/create.html',context)

def delete(request,ids):
    ins = Articles.objects.get(id = ids)
    ins.delete()
    return HttpResponseRedirect("/blog/")
