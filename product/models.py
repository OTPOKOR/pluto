from unicodedata import category
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import IntegerField
# HTML PARSER기 설정 - 사용안함
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields
# 범용모델키 설정
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

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
    product_title = models.TextField(null=True)
    stock=models.BooleanField()
    price=models.IntegerField()
    sale_price=models.IntegerField(null=True)
    shipping_price=models.IntegerField(null=True)
    weight=models.TextField(blank=True)
    volume=models.TextField(blank=True)
    option=ArrayField(models.CharField(max_length=200,blank=True),size=100)
    policy_number = models.IntegerField(null=True)
    
class ProductOption(models.Model):
    foreign_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    option = models.TextField(null=True)
    stock = models.IntegerField(null=True)
    
class Ebay (models.Model):
    foreign_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    # 카테고리분류
    # 카테고리아이디
    brand=models.TextField(null=True)
    style=models.TextField(null=True)
    color=models.TextField(null=True)
    department=models.TextField(null=True)
    pattern=models.TextField(null=True)
    features=models.TextField(null=True)
    fabricType=models.TextField(null=True)
    occasion=models.TextField(null=True)
    material=models.TextField(null=True)
    
class UserTokken (models.Model):
    ebay_usertokken = models.TextField(null=True)
    ebay_refreshtokken = models.TextField(null=True)
    update_date=models.DateTimeField(null=True)
    refresh_expired = models.TextField(null=True)

class Description_Middle(models.Model):
    foreign_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.TextField(null=True)

class Description_Bottom(models.Model):
    title = models.TextField(null=True)
    description = models.TextField(null=True)


#  카테고리 분류
class Item_Category(models.Model):
    category_name = models.TextField(null=True)

class Ebay_Required_Spec_Name(models.Model):
    foreign_category = models.ForeignKey(Item_Category,on_delete=models.CASCADE)
    spec_name = models.TextField(null=True)
    spec_contain = GenericRelation('Ebay_Required_Spec_Contain', related_query_name='ebay_spec_name')
    
class Ebay_Required_Spec_Contain(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField() 
    content_object = GenericForeignKey('content_type', 'object_id')
    spec_contain = models.TextField(null=True)
    foreign_product = models.ForeignKey(Product,on_delete=models.CASCADE)