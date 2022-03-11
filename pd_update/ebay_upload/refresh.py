from getpass import getuser
from .ebayOauth.test.GetUserAccessToken import TestGetApplicationCredential
from product.models import *
import datetime
from django.utils import timezone
now = datetime.datetime.now()

def refresh_tokken():
    a = UserTokken.objects.filter(id = 1)
    update_date = a.values()[0]['update_date']
    if update_date +datetime.timedelta(minutes=100) >= timezone.now() :
        t = a.values()[0]['ebay_usertokken']
        return t 
    else :    
        refresh_tokken = a.values()[0]['ebay_refreshtokken']
        getUserToken = TestGetApplicationCredential.test_access_token(refresh_tokken).__dict__
        b = getUserToken['access_token']
        a.update(
            ebay_usertokken = b,
            update_date = timezone.now()
            )
        print('엑세스토큰이 새로 생성되었습니다')
        t = a.values()[0]['ebay_usertokken']
        return t