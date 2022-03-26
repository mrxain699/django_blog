from django.shortcuts import *
from django.http import *
from .models import *
from .forms import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.core.paginator import Paginator
import os



# create user / author
def signup(request):
    if request.method == "POST":
        fm = SignUpFrom(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect("/login/")
    else:
        fm = SignUpFrom()        
    return render(request, "blog/signup.html", context = {"form":fm})


# login  author /admin authentication
def login_user(request):
    if request.method == "POST":
        fm = LoginForm(request = request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            password = fm.cleaned_data["password"]
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return HttpResponseRedirect("/dashboard/")
                else:
                    return HttpResponseRedirect("/")
                    
    else:
        fm = LoginForm()
    return render(request, "blog/login.html", context={"form":fm})

# logout user / admin

def logout_user(request):
    if request.user:
        logout(request)
        return HttpResponseRedirect("/")



# Index page display all the post and recent post and navbar
def index(request):
    post = Post.objects.all().order_by("id").reverse()
    make_paginator = Paginator(post, 5)
    page_num = request.GET.get("page")
    page_obj = make_paginator.get_page(page_num)
    recent_post = Post.objects.all().order_by("id").reverse()[:5]
    navbar = Catagorie.objects.all().order_by("id").reverse()
    return render(request, "blog/index.html", context = {"posts" : page_obj,"recent_posts": recent_post, "navs":navbar})

# display post by  catagory
def post_catagory(request, id):
    get_posts = Post.objects.filter(catagory = id)
    recent_post = Post.objects.all().order_by("id").reverse()[:5]
    navbar = Catagorie.objects.all().order_by("id").reverse()
    return render(request, "blog/index.html", context = {"posts" :get_posts,"recent_posts": recent_post, "navs":navbar})

# display post details
def post_detail(request, id):
    post_details = Post.objects.get(pk = id)
    recent_post = Post.objects.all().order_by("id").reverse()[:5]
    navbar = Catagorie.objects.all().order_by("id").reverse()
    return render(request, "blog/post_detail.html", context = {"post_details":post_details,"recent_posts": recent_post, "navs":navbar})


# display all the author to admin 
@login_required(login_url = "/login/")
def dashboard(request):
    author  = Author.objects.all()
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    make_paginator = Paginator(author, 10)
    page_num = request.GET.get("page")
    page_obj = make_paginator.get_page(page_num)  
    return render(request, "blog/dashboard.html", context = {"authors":page_obj, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})

# display all the post to admin and author 
@login_required(login_url = "/login/")
def posts(request):
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if request.user.is_superuser:
        post = Post.objects.all()
        make_paginator = Paginator(post, 10)
        page_num = request.GET.get("page")
        page_obj = make_paginator.get_page(page_num)  
    else:
        post = Post.objects.filter(author = request.user)
        total_posts = Post.objects.filter(author = request.user)
        make_paginator = Paginator(post, 10)
        page_num = request.GET.get("page")
        page_obj = make_paginator.get_page(page_num)        
    return render(request, "blog/posts.html", context = {"posts":page_obj, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})


# display all the catagories to admin
@login_required(login_url = "/login/")
def catagories(request):
    catagory = Catagorie.objects.all()
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    make_paginator = Paginator(catagory, 10)
    page_num = request.GET.get("page")
    page_obj = make_paginator.get_page(page_num)   
    return render(request, "blog/catagories.html", context = {"catagories":page_obj, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})      


# add author! only admin can do that
@login_required(login_url = "/login/")
def add_author(request):
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if request.method == "POST":
        fm = SignUpFrom(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect("/dashboard/")
    else:
        fm = SignUpFrom()        
    return render(request, "blog/add_author.html", context = {"form":fm, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})        
        
# add post both author and admin can do that 
@login_required(login_url = "/login/")          
def add_posts(request):
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if not request.user.is_superuser:
        total_posts = Post.objects.filter(author = request.user)
    if request.method == "POST":
        fm = PostsForm(request.POST, request.FILES)
        if fm.is_valid():
            title = fm.cleaned_data["title"]
            desc = fm.cleaned_data["desc"]
            catagory = fm.cleaned_data["catagory"]
            img = fm.cleaned_data["image"]
            user = request.user
            post_create = Post.objects.create(title=title, desc=desc, image=img, catagory = catagory, author = user)
            if post_create:
                get_post_cat = Catagorie.objects.get(catagory=catagory)
                get_post_cat.total_posts += 1
                get_post_cat.save()
                get_user = Author.objects.get(pk = request.user.id)
                get_user.total_posts += 1
                get_user.save()    
    else:
        fm = PostsForm()   
    catagorie = Catagorie.objects.all()      
    return render(request, "blog/add_post.html", context = {"form":fm, "catagories":catagorie, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})

# add catagory! only admin can do that
@login_required(login_url = "/login/")
def add_catagories(request):
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if request.method == "POST":
        fm = CatagoriesForm(request.POST)
        if fm.is_valid():
            catagory = fm.cleaned_data["catagory"]
            cat = Catagorie.objects.create(catagory = catagory, total_posts = 0)
            cat.save()
    else:
        fm = CatagoriesForm()
    return render(request, "blog/add_catagory.html", context = {"form":fm, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})  

   
# delete author! only admin can do that
@login_required(login_url = "/login/")
def delete_author(request, id):
    delete_author = Author.objects.get(pk=id)
    auhtor_posts = Post.objects.filter(author =  delete_author.username)
    if delete_author:
        if auhtor_posts:
            for post in auhtor_posts:
                post_category = post.catagory
                get_post_cat = Catagorie.objects.get(catagory = post_category )
                get_post_cat.total_posts -= 1
                get_post_cat.save()
                post.delete()
        delete_author.delete()
        return HttpResponseRedirect('/dashboard/')
    
# delete post author and admin can do that
@login_required(login_url = "/login/")
def delete_post(request, id):
    delete_post = Post.objects.get(pk=id)
    delete_post_cat = delete_post.catagory
    delete_post_author = delete_post.author
    if delete_post and delete_post_cat and delete_post_author:
        if len(delete_post.image) > 0:
            os.remove(delete_post.image.path)
        delete_post.delete()
        get_post_cat = Catagorie.objects.get(catagory=delete_post_cat)
        get_post_cat.total_posts -= 1
        get_post_cat.save()
        get_user = Author.objects.get(username = delete_post_author)
        get_user.total_posts -= 1
        get_user.save()  
        return HttpResponseRedirect('/posts/')
        
            
# delete catagory! only admin can do that
@login_required(login_url = "/login/")
def delete_catagory(request, id):
    delete_catagory = Catagorie.objects.get(pk=id)
    delete_cat_posts = Post.objects.filter(catagory = delete_catagory.id)
    if delete_catagory:
        for del_post in delete_cat_posts:
            get_post_user = Author.objects.get(username  = del_post.author)
            get_post_user.total_posts -= 1
            get_post_user.save()
            del_post.delete()
        delete_catagory.delete()
        return HttpResponseRedirect('/catagories/')
    
# update author only admin can do that
@login_required(login_url = "/login/")
def update_author(request, id):
    author  = Author.objects.get(pk = id)
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if request.method == "POST":
        fm = UpdateAuthorForm(request.POST, instance = author)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect("/dashboard/")
    else:
        fm = UpdateAuthorForm(instance = author)
    return render(request, "blog/update_author.html", context = {"form":fm, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})


# update post both auhtor and admin can do that
@login_required(login_url = "/login/")
def update_post(request, id):
    post = Post.objects.get(pk = id)
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if not request.user.is_superuser:
        total_posts = Post.objects.filter(author = request.user)
    if request.method == 'POST':
        fm = PostsForm(request.POST , instance = post)
        if fm.is_valid():
            if len(request.FILES) != 0:
                if len(post.image) > 0:
                    os.remove(post.image.path)
                    image_name = request.FILES["image"]
                    post.image = image_name
                    post.save()
            fm.save()
            return HttpResponseRedirect("/posts/")
    else:
        fm = PostsForm(instance = post)
    return render(request, "blog/add_post.html", context = {"form":fm, "update":True, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})        

# delete account /  deactivate account
@login_required(login_url = "/login/")        
def delete_account(request, id):
    delete_account = Author.objects.get(pk=id)
    account_posts = Post.objects.filter(author =  delete_account.username)
    if delete_account:
        if account_posts:
            for post in account_posts:
                post_category = post.catagory
                get_post_cat = Catagorie.objects.get(catagory = post_category )
                get_post_cat.total_posts -= 1
                get_post_cat.save()
                post.delete()
        delete_account.delete()
        return HttpResponseRedirect('/')
    
# chnage password     
@login_required(login_url = "/login/")
def changePassword(request):
    total_authors = Author.objects.all()
    total_posts = Post.objects.all()
    total_catagories = Catagorie.objects.all()
    if not request.user.is_superuser:
        total_posts = Post.objects.filter(author = request.user)
    if request.method == "POST":
        fm = ChangePassword(user = request.user, data = request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        fm = ChangePassword(user = request.user)
    return render(request, 'blog/change_password.html', context={"form":fm, "total_authors": total_authors, "total_posts":total_posts, "total_catagories":total_catagories})