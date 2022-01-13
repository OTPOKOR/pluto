from django.db import models
import json
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
    shipping_price=models.IntegerField()
    weight=models.TextField(blank=True)
    volume=models.TextField(blank=True)
    option=models.TextField()
    # 옵션 json 으로 만들기
    
    def set_option(self, x):
        self.option = json.dumps(x)
        
    def get_option(self,x):
        return json.loads(self.option)