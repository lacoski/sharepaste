from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views import generic
from .models import Paste
from .forms import PasteCreateForm,PasteFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .helper import FileIO
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.

NUMBER_ITEM_PER_PAGE = 5
SUPPORT_LANGUAGE = ['Apache', 'Bash', 'C#', 'C++', 'CSS', 'CoffeeScript', 'Diff', 'HTML', 'XML', 'HTTP', 'Ini',  
                    'JSON', 'Java', 'JavaScript', 'Makefile', 'Markdown', 'Nginx', 'Objective-C', 'PHP', 'Perl',  
                    'Python', 'Ruby', 'SQL', 'Shell Session'] 

def index(request):
    if request.user.is_authenticated:
        return redirect('list_paste_template')
    return redirect('create_paste_guest_template')


@login_required
def list_paste_template(request):
    Pastes = Paste.objects.filter(user_own=request.user.username)
    paginator = Paginator(Pastes, NUMBER_ITEM_PER_PAGE)
    page = request.GET.get('page')
    Pastes_with_paginator = paginator.get_page(page)
    return render(request, 'userzone/paste_lists.html',{'Pastes':Pastes_with_paginator,
                                                        'title':'Lists Paste' ,'sub_title':'All your code'} )
@login_required
def search_paste_template(request):    
    search_text = request.GET.get('id')
    Pastes = Paste.objects.filter(user_own=request.user.username, paste_name__contains=search_text)    
    paginator = Paginator(Pastes, NUMBER_ITEM_PER_PAGE)
    page = request.GET.get('page')
    Pastes_with_paginator = paginator.get_page(page)
    return render(request, 'userzone/paste_lists.html',{'Pastes':Pastes_with_paginator, 'title':'Search Paste',
                                                        'sub_title':'Search your code','search_text':search_text,})
@login_required
def go_to_paste_template(request):    
    short_link = request.GET.get('id')            
    return redirect('review_paste_template', id=short_link)

def go_to_paste_guest_template(request):    
    short_link = request.GET.get('id')    
    #print(short_link)        
    #return redirect('create_paste_guest_template')
    return redirect('review_paste_guest_template', id=short_link)

@login_required
def create_paste_template(request):
    form = PasteFileForm(request.POST or None)
    list_syntax = SUPPORT_LANGUAGE
    if form.is_valid():        
        obj = form.save(commit=False)
        obj.user_own = request.user.username
        obj.save()
        content = request.POST.get('content_paste')
        target = Paste.objects.get(id=obj.id)     
        FileIO.writeToFile(content, target.short_link)           
        return redirect('review_paste_template', id=target.short_link)

    return render(request, 'userzone/paste_create.html', {'form': form, 'title':'Create Paste', 
                                                        'sub_title':'Lets Sharing your code','list_syntax':list_syntax})

@login_required
def update_paste_template(request,id):
    #Paste_ = Paste.objects.get(id=id)   
    Paste_ = get_object_or_404(Paste, id=id) 
    list_syntax = SUPPORT_LANGUAGE
    form = PasteFileForm(request.POST or None, instance=Paste_)
    content = FileIO.readFile(Paste_.short_link)  

    if form.is_valid():
        form.save()        
        content = request.POST.get('content_paste')        
        FileIO.writeToFile(content, Paste_.short_link)

        return redirect('review_paste_template', id=Paste_.short_link)
    return render(request, 'userzone/paste_create.html', {'form': form, 'paste': Paste_, 'title':'Update Paste' ,
                                                        'sub_title':'Changing your code','list_syntax':list_syntax,
                                                        'content_paste':content })

@login_required
def delete_paste_template(request,id):
    Paste_ = get_object_or_404(Paste, id=id)
    #Paste_ = Paste.objects.get(id=id)
    if request.method == 'POST':
        Paste_.delete()
        return redirect('list_paste_template')
    
    return render(request, 'userzone/paste_delete.html', {'paste': Paste_, 'title':'Delete Paste' ,'sub_title':'Remote your code'})

@login_required
def review_paste_template(request,id):
    Paste_ = get_object_or_404(Paste, short_link=id)
    #Paste_ = Paste.objects.get(short_link=id)  
    content = FileIO.readFile(Paste_.short_link)  
    return render(request, 'userzone/paste_review.html', {'paste': Paste_, 'title':'Review Paste' ,
                                                        'sub_title':'See your code', 'content_paste':content})

@csrf_exempt
def create_paste_guest_template(request):
    form = PasteFileForm(request.POST or None)
    list_syntax = SUPPORT_LANGUAGE
    if form.is_valid():        
        obj = form.save(commit=False)         
        obj.save()
        target = Paste.objects.get(id=obj.id)        

        content_paste = request.POST.get('content_paste')
        #print(content_paste)
        FileIO.writeToFile(content_paste, target.short_link)        

        return redirect('review_paste_guest_template', id=target.short_link)
    return render(request, 'userzone/paste_create_guest.html', {'form': form, 'title':'Create Paste', 
                                                                'sub_title':'Lets Sharing your code','list_syntax':list_syntax})

@csrf_exempt
def create_paste_tool_guest_template(request):
    form = PasteFileForm(request.POST or None)
    list_syntax = SUPPORT_LANGUAGE
    if form.is_valid():        
        obj = form.save(commit=False)         
        obj.save()
        target = Paste.objects.get(id=obj.id)        

        content_paste = request.POST.get('content_paste')
        #print(content_paste)
        FileIO.writeToFile(content_paste, target.short_link)        

        return HttpResponse(target.short_link, status=200)
    return HttpResponse('FAIL TO CREATE PASTE', status=400)

def review_paste_guest_template(request,id):
    Paste_ = get_object_or_404(Paste, short_link=id)
    #Paste_ = Paste.objects.get(short_link=id)    
    content= FileIO.readFile(Paste_.short_link)    
    str_content = str(content)
    return render(request, 'userzone/paste_review_guest.html', {'paste': Paste_, 'title':'Review Paste' ,'sub_title':'See your code', 
                                                                'content_paste':content, 'str_content': str_content})

def create_paste_file_guest_template(request):
    form = PasteCreateForm(request.POST or None)
    list_syntax = SUPPORT_LANGUAGE
    if form.is_valid():        
        obj = form.save(commit=False)        
        #obj.save()
        #target = Paste.objects.get(id=obj.id)        
        #return redirect('review_paste_guest_template', id=target.short_link)
    return render(request, 'userzone/paste_create_guest.html', {'form': form, 'title':'Create Paste', 
                                                                'sub_title':'Lets Sharing your code','list_syntax':list_syntax})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'userzone/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'userzone/simple_upload.html')

def read_content_file(request):        
    get_file = os.path.join(settings.MEDIA_ROOT, 'README.md')
    #print(get_file)
    file = open(get_file, "r") 
    content= file.read()
    return render(request, 'userzone/review_upload_file.html',{
        'content':content,
    })


