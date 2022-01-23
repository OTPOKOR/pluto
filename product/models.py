from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Product (models.Model):

    product_number=models.TextField()
    identy_number= models.TextField()
    regist_date=models.DateTimeField()
    update_date=models.DateTimeField()
    site=models.TextField()
    brand=models.TextField(blank=True)
    product_url=models.URLField()
    product_name=models.TextField()
    stock=models.BooleanField()
    price=models.IntegerField()
    shipping_price=models.IntegerField(null=True)
    weight=models.TextField(blank=True)
    volume=models.TextField(blank=True)
    option=ArrayField(models.CharField(max_length=200,blank=True),size=100)
