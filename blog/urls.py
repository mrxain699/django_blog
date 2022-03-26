from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import *



urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('', index, name='index'),
    path("dashboard/", dashboard, name="dashboard"),
    path("post_catagory/<int:id>", post_catagory, name="post_catagory"),
    path('posts/', posts, name='posts'),
    path('post_detail/<int:id>', post_detail, name="post_detail"),
    path('catagories/', catagories, name='catagories'),
    path('add_author/', add_author, name='add_author'),
    path('add_posts/', add_posts, name='add_posts'),
    path('add_catagories/', add_catagories, name='add_catagories'),
    path('delete_author/<int:id>', delete_author, name='delete_author'),
    path('delete_post/<int:id>', delete_post, name='delete_post'),
    path('delete_catagory/<int:id>', delete_catagory, name='delete_catagory'),
    path("update_author/<int:id>", update_author, name='update_author'),
    path("update_post/<int:id>", update_post, name='update_post'),
    path("delete_account/<int:id>", delete_account, name='delete_account'),
    path("change_password/", changePassword, name='change_password'),
    
    
] 