from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SELLER', 'Seller'),
        ('CUSTOMER', 'Customer'),)
    phone_number=models.CharField(max_length=11)
    address=models.CharField(max_length=100)
    profile_image=models.ImageField(upload_to='profile_image',null=True,blank=True)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    date_login=models.DateField()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    customer_id=models.ForeignKey(User,on_delete=models.CASCADE)
    category_name=models.CharField(max_length=20) 
    category_description=models.CharField(max_length=200)
    category_image=models.ImageField(upload_to='category/',null=True,blank=True)
    created_at=models.DateField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,)
    subcategory_name = models.CharField(max_length=50)
    subcategory_description = models.CharField(max_length=200)
    subcategory_image = models.ImageField(upload_to='subcategory/',null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

