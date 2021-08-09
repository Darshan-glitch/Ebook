from django.contrib.auth.models import User
from django.contrib.messages.api import success
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.utils.regex_helper import Choice

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id=models.AutoField
    book_name=models.CharField(max_length=50)
    author=models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="",default="")
    
    @staticmethod
    def book_by_category(category_id):
        if category_id:
            return Book.objects.filter(category=category_id)
        else:
            return Book.objects.all()    


    def __str__(self):
        return self.book_name
class Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
     
    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'
         
    def __str__(self):
        return self.title


    @staticmethod
    def book_by_categories(categoryid):
        if categoryid:
            return Book.objects.filter(categoryid=categoryid)
        else:
           return Book.objects.all()
class Payment(models.Model):
    book=models.ForeignKey(Book,on_delete=CASCADE)
    user=models.ForeignKey(User,on_delete=CASCADE)
    orderid=models.CharField(max_length=100,null=True,blank=True)
    paymentid=models.CharField(max_length=100,null=True,blank=True)
    status_choice={
        ("SUCCESS","SUCCESS"),
        ("FAIL","FAIL")
    }
    status=models.CharField(choices=status_choice ,max_length=100)
class Myorder(models.Model):
     book=models.ForeignKey(Book,on_delete=CASCADE)
     user=models.ForeignKey(User,on_delete=CASCADE)

