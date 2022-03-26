from django.db import models
from django.contrib.auth.models import *
# Create your models here.

class Author(AbstractUser):
    total_posts = models.PositiveIntegerField(null = True, default = 0)
    
    def __str__(self):
        return self.username

class Catagorie(models.Model):
    catagory = models.CharField(max_length=70)
    total_posts = models.PositiveIntegerField()
    
    def __str__(self):
        return self.catagory
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=1000)
    image = models.ImageField(upload_to = "uploadedImage")
    catagory = models.ForeignKey(Catagorie, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)

    
    def __str__(self):
        return self.title
    
    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()


        
