from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Author)
class AuthorModel(admin.ModelAdmin):
    list_display = ['id','username','email', 'total_posts']
    
@admin.register(Post)
class PostModel(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'author']

@admin.register(Catagorie)
class CatagoryModel(admin.ModelAdmin):
    list_display = ['id', 'catagory','total_posts']
    

    