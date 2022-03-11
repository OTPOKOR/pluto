from asyncio import subprocess
from quopri import decodestring
import requests
import json
from product.models import *

# 보내기실험
import subprocess
import re
import os
# 리프레쉬토큰

from .refresh import refresh_tokken
USER_TOKEN = refresh_tokken()

class Getinfo:
    def __init__(self,id):
        self.id = id
        self.item = Product.objects.filter(id = self.id).values()[0]
        self.ebay = Ebay.objects.filter(foreign_product = self.id).values()[0]
        self.option = ProductOption.objects.filter(foreign_product = self.id).values()
        self.description_middle = Description_Middle.objects.filter(foreign_product = self.id).values()[0]
        self.description_bottom = Description_Bottom.objects.filter(id = 1).values()[0]
class UploadingEbay(Getinfo):
    def get_files_count(self):
        pn = self.item['product_number']
        dirListing = os.listdir(f'D:\DB\IMG\{pn}')
        return len(dirListing)

    def image_upload(self):
        image_list = []
        pnNumber = UploadingEbay.get_files_count(self)
        
        for i in range(pnNumber):
            auth = USER_TOKEN.replace('^','$')
            picNameIn = self.item['product_number']
            file = f'D:/DB/IMG/{picNameIn}/{i}.jpg'
            text = f"php C:/Users/wldnj/Desktop/pluto/test/pd_update/ebay_upload/UploadSiteHostedPictures/UploadSiteHostedPictures.php {auth} {file} {picNameIn}"
            result = subprocess.Popen(text,shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE,universal_newlines=True)
            result.wait()
            out = result.stdout.read().strip().replace('\n','')
            p = re.compile('(https.+?.?<)')
            word = p.search(out).group().replace('<','')
            image_list.append(word)

        return image_list
        
    def createOrReplaceInventoryItem(self,imgls):
        for i in range(len(self.option)):
            try:
                headers = {"Authorization":"Bearer "+USER_TOKEN,"Accept":"application/json","Content-Type": "application/json","Content-Language":"en-US"}
                data = { 
            "product": { 
                "title": self.item['product_title'],
                "description": self.ebay['description'],
                "aspects":{
                    "Brand":[self.ebay['brand']],
                    "Pattern":[self.ebay['pattern']],
                    "Department":[self.ebay['department']],
                    "Size":[self.option[i]['option']],
                    "Color":[self.ebay['color']],
                    "Style":[self.ebay['style']],
                    "Material":[self.ebay['material']],
                    "Features":[self.ebay['features']],
                    "Fabric type":[self.ebay['fabricType']],
                    "Occasion":[self.ebay['occasion']]
                    },
                "imageUrls": [
                    imgls[0]
                ]
            },
            "condition": "NEW",
                "availability": { 
                "shipToLocationAvailability": 
                    { 
                    "quantity": self.option[i]['stock']
                    },
                
            },
            } 
                json_data = json.dumps(data)
                pdUrl = self.item['product_number']+ '-' + self.option[i]['option']
                res = requests.put(f'https://api.ebay.com/sell/inventory/v1/inventory_item/{pdUrl}',headers=headers,data=json_data)
                print(res.json())
            except ConnectionError as e:
                print(e)
                print(e).response.dict()
            except ValueError as e:
                print('CreateInventoryItem Completed')
                print(e)
                
    def createOffer(self):
        """
        SKU : option-'Size'
        CategoryId : "number"
        
        """
        
        for i in range(len(self.option)):
            
            headers = {"Authorization":"Bearer "+USER_TOKEN,"Accept":"application/json","Content-Type": "application/json","Content-Language":"en-US"}
            item_spec = {
                "SKU" : "N225AHA740099-L",
                "categoryId" : "52365",
                "listingDescription" : "offer testing Description",
                "availableQuantity": 1,
                "price" : "92"
            }
            #  Category Id , policy 는 분류해야함 일단 정의해놓지는 않음
            #  listing description도 체크해볼것
            data = {
                "sku": self.item['product_number']+'-'+self.option[i]['option'],
                "marketplaceId": "EBAY_US",
                "format": "FIXED_PRICE",
                "availableQuantity": self.option[i]['stock'],
                "categoryId": '52365',
                "merchantLocationKey" : "kraddress",
                "listingDescription": "listingDescription",
                "listingPolicies": {
                    "fulfillmentPolicyId": "192893723019",
                    "paymentPolicyId": "191374098019",
                    "returnPolicyId": "191373944019",
                },
                "pricingSummary": {
                    "price": {
                        "currency": "USD",
                        "value": self.ebay['price']
                    }
                },
            }
            try:
                json_data = json.dumps(data)
                res = requests.post('https://api.ebay.com/sell/inventory/v1/offer',headers=headers,data = json_data)
                print(res.json())
                # offerId를 생성함 나중에 필요하면 DB에 저장해놔야겠음
            except ConnectionError as e:
                print(e)
                print(e).response.dict()
            except ValueError as e:
                print('CreateInventoryItem Completed')
                print(e)
                
    def createOrReplaceInventoryItemGroup(self,imgls):
        headers = {"Authorization":"Bearer "+USER_TOKEN,"Accept":"application/json","Content-Type": "application/json","Content-Language":"en-US"}

        # 옵션 만들기 
        skus = []
        option = []
        for i in range(len(self.option)):
            v = self.item['product_number']+'-'+self.option[i]['option']
            o = self.option[i]['option']
            option.append(o)
            skus.append(v)

        data = {
            "aspects":{
                "Brand":[self.ebay['brand']],
                "Pattern":[self.ebay['pattern']],
                "Department":[self.ebay['department']],
                "Color":[self.ebay['color']],
                "Style":[self.ebay['style']],
                "Material":[self.ebay["material"]],
                "Features":[self.ebay["features"]],
                "Fabric type":[self.ebay["fabricType"]],
                "Occasion":[self.ebay["occasion"]],
                },
            "title":self.item['product_title'],
            "description": self.description_middle['description'] + self.description_bottom['description'],
            "imageUrls": imgls,
            "variantSKUs": skus,
            "variesBy":{
                "aspectsImageVariesBy": ["Size"],
                "specifications":[{
                    "name":"Size",
                    "values":option
                }]
            }
        }
        json_data = json.dumps(data)
        try:
            res = requests.put('https://api.ebay.com/sell/inventory/v1/inventory_item_group/'+ self.item['product_number'],headers=headers, data = json_data)
            print(res.json())
        except ConnectionError as e:
            print(e).response.dict()
            print(e)
        except ValueError as e:
            print('CreateInventoryItem Completed')
            print(e)
        
    def publishOfferByInventoryItemGroup(self):
        
        headers = {"Authorization":"Bearer "+USER_TOKEN,"Accept":"application/json","Content-Type": "application/json"}
        
        data = {
            "inventoryItemGroupKey" : self.item['product_number'],
            "marketplaceId" : "EBAY_US"
        }
        json_data = json.dumps(data)
        try:
            res = requests.post('https://api.ebay.com/sell/inventory/v1/offer/publish_by_inventory_item_group/',headers=headers, data = json_data)
            print(res.json())
        except ConnectionError as e:
            print(e).response.dict()
            print(e)
        except ValueError as e:
            print('publishOfferByInventoryItemGroup Completed')
            print(e)
            # 리스팅아이디가 도출됨
        
        
        
        
        
def getInventoryItem(self):
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8','Authorization':'Bearer '+USER_TOKEN,}
        res = requests.get(f"https://api.ebay.com/sell/inventory/v1/inventory_item/{self.item['product_number']}", headers=headers)
        
        print(res.json())

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        
def getInventoryItems():
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8','Authorization':'Bearer '+USER_TOKEN,}
        res = requests.get('https://api.ebay.com/sell/inventory/v1/inventory_item?limit=2&offset=0', headers=headers)
        
        print(res.json())

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def bulkMigrateListing():
    try:
        headers = {'Authorization':'Bearer '+USER_TOKEN,'Accept':'application/json','Content-Type': 'application/json','Content-Language':'en-US'}
        
        json = {
    "requests":[
        {
            "listingId":"294194039343"
        }
    ]
}
        
        res = requests.post("https://api.ebay.com/sell/inventory/v1/bulk_migrate_listing",json = json,headers = headers)
        print(res.json())
        
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
