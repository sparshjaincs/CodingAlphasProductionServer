from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from Core.models import Homepage_Activity
# Create your views here.
def blog(request):
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

def inside(request,user,title,ids):
    context = {}
    context['data'] = Articles.objects.get(id = ids)
    return render(request,'Blogs/inside.html',context)
def create(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            ins = form.save(commit = False)
            ins.user_name2 = request.user
           
            ins.save()
            ins = Homepage_Activity(category = 'Blog',blog = ins)
            ins.save()
            return HttpResponseRedirect("/blog/")
        else:

            context['errors'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    return render(request,'Blogs/create.html',context)

def preview(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            ins = form.save(commit = False)
            ins.user_name2 = request.user
            ins.status = 'draft'
            ins.save()
            return HttpResponseRedirect(f"/blog/preview/{ins.id}/")
        else:

            context['errors'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    #context['data'] = Articles.objects.get(id = ids)
    return render(request,'Blogs/preview.html',context)
def draft(request):
    context = {}
    if request.method == 'POST':
        form = Article_form(request.POST,request.FILES)
        if form.is_valid():
            ins = form.save(commit = False)
            ins.user_name2 = request.user
            ins.status = 'draft'
            ins.save()
            return HttpResponseRedirect(f"/profile/{request.user}/#article")
        else:

            context['errors'] = form.errors
    else:
        form = Article_form()
    context['form'] = form
    #context['data'] = Articles.objects.get(id = ids)
    return render(request,'Blogs/preview.html',context)
def preview_data(request,ids):
    context = {}
    context['data'] = Articles.objects.get(id = ids)
    return render(request,'Blogs/preview.html',context)

def post(request,ids):
    ins = Articles.objects.get(id = ids)
    ins.status = 'published'
    ins.save()
    ins = Homepage_Activity(category = 'Blog',blog = ins)
    ins.save()
    return HttpResponseRedirect("/blog/")

def edit(request,ids):
    context = {}
    ins = Articles.objects.get(id = ids)
    context['form'] = Article_form(initial = model_to_dict(ins))
    context['edit'] = True
    context['link'] = ins.image
    context['id'] = ins.id
    return render(request,'Blogs/create.html',context)

def posting(request):
    context = {}
    if request.method == 'POST':
     
        ids = request.POST.get("iding")
        ins = Articles.objects.get(id = ids)
        ins.title = request.POST.get('title')
        ins.description = request.POST.get('description')
        ins.content = request.POST.get('content')
        if request.FILES.get('image') is not None:
            ins.image = request.FILES.get('image')
        ins.status = 'published'
        ins.save()
        ins = Homepage_Activity(category = 'Blog',blog = ins)
        ins.save()
        return HttpResponseRedirect("/blog/")
       

def previewing(request):
    context = {}
    if request.method == 'POST':
     
        ids = request.POST.get("iding")
        ins = Articles.objects.get(id = ids)
        ins.title = request.POST.get('title')
        ins.description = request.POST.get('description')
        ins.content = request.POST.get('content')
        if request.FILES.get('image') is not None:
            ins.image = request.FILES.get('image')
        ins.status = 'draft'
        ins.save()
        return HttpResponseRedirect(f"/blog/preview/{ins.id}/")
        
    return render(request,'Blogs/preview.html',context)

def drafting(request):
    context = {}
    if request.method == 'POST':
        try:
            ids = request.POST.get("iding")
            ins = Articles.objects.get(id = ids)
            ins.title = request.POST.get('title')
            ins.description = request.POST.get('description')
            ins.content = request.POST.get('content') 
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            ins.status = 'draft'
            ins.save()
        except exception as exp:
            context['errors'] = str(exp)
    return HttpResponseRedirect(f"/profile/{request.user}/#article")
            

        


   


