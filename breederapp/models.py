from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=20)
    viewpassword=models.CharField(max_length=20)
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    district = models.CharField(max_length=255)
    password=models.CharField(max_length=100,default=0)
    status=models.CharField(max_length=100,default='pending')
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)

class Breeder(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    district = models.CharField(max_length=255)
    password=models.CharField(max_length=100,default=0)
    status=models.CharField(max_length=100,default='pending')
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
class Breederdog(models.Model):
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=20)
    medication = models.CharField(max_length=255)
    age=models.CharField(max_length=100,default=0)
    description=models.CharField(max_length=100)
    image=models.ImageField(upload_to="uploadimage",max_length=None,null=True)
    Certificate = models.ImageField(null=True)
    price=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='pending')
    gender=models.CharField(max_length=100,default=0)
    breeder=models.ForeignKey(Breeder,on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(null=True)
class Customerdog(models.Model):
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=20)
    medication = models.CharField(max_length=255)
    age=models.CharField(max_length=100,default=0)
    description=models.CharField(max_length=100)
    image=models.ImageField(upload_to="uploadimage",max_length=None,null=True)
    Certificate = models.ImageField(null=True,default=None)
    status=models.CharField(max_length=100,default='pending')
    gender=models.CharField(max_length=100,default=0)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)

class Breeding(models.Model):
    customerdog=models.ForeignKey(Customerdog,on_delete=models.CASCADE,null=True)
    breederdog=models.ForeignKey(Breederdog,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    startdate = models.DateTimeField(null=True)
    enddate = models.DateTimeField(null=True)
    amount=models.CharField(null=True,max_length=100)
    admincommission=models.IntegerField(null=True)
    breederpayment=models.IntegerField(null=True)
    breeder=models.ForeignKey(Breeder,on_delete=models.CASCADE,null=True)
    paymentstatus=models.CharField(max_length=100,default='pending')
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)

class Offspring(models.Model):
    breeding=models.ForeignKey(Breeding,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    date = models.DateTimeField(auto_now_add=True,null=True)
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=20)
    medication = models.CharField(max_length=255)
    description=models.CharField(max_length=100)
    image=models.ImageField(upload_to="uploadimage",max_length=None,null=True)
    status=models.CharField(max_length=100,default='pending')
    gender=models.CharField(max_length=100,default=0)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    breeder=models.ForeignKey(Breeder,on_delete=models.CASCADE,null=True)
class Chat(models.Model):
    breeding=models.ForeignKey(Breeding,on_delete=models.CASCADE,null=True) 
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    breeder=models.ForeignKey(Breeder,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    message=models.CharField(max_length=100)
    reply=models.CharField(max_length=100,null=True)
class Feedback(models.Model):
    feedback=models.CharField(max_length=100)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)


# class Products(models.Model):
#     name = models.CharField(max_length=20)
#     price = models.CharField(max_length=20)
#     desc = models.CharField(max_length=20)
#     img = models.ImageField(null=True)


# class Cart(models.Model):
#     pid = models.ForeignKey(Products,on_delete=models.CASCADE)
#     uid = models.ForeignKey(Customer,on_delete=models.CASCADE)
#     qty = models.IntegerField()
#     amt = models.IntegerField()
#     status = models.CharField(max_length=20)


# class Payment(models.Model):
#     uid = models.ForeignKey(Customer,on_delete=models.CASCADE)
#     amt = models.IntegerField()
#     date = models.DateField(auto_now_add=True)
    

    
    
# class Rate(models.Model):
#     uid=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
#     wid=models.ForeignKey(Breederdog,on_delete=models.CASCADE,null=True)
#     rating=models.FloatField(null=True)