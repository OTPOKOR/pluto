# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

"""

import os, sys
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from oauthclient.oauth2api import oauth2api
from .TestUtil import *
from oauthclient.credentialutil import credentialutil
from oauthclient.model.model import environment
import unittest

app_scopes = ['https://api.ebay.com/oauth/api_scope','https://api.ebay.com/oauth/api_scope/sell.marketing','https://api.ebay.com/oauth/api_scope/sell.inventory','https://api.ebay.com/oauth/api_scope/sell.account','https://api.ebay.com/oauth/api_scope/sell.fulfillment','https://api.ebay.com/oauth/api_scope/sell.finances','https://api.ebay.com/oauth/api_scope/commerce.notification.subscription']

class TestGetApplicationCredential(unittest.TestCase):
    def test_generate_authorization_url(self):
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        credentialutil.load(app_config_path)
        oauth2api_inst = oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(environment.PRODUCTION, app_scopes)
        # self.assertIsNotNone(signin_url)
        print ('\n *** test_get_signin_url ***: \n', signin_url)
    
    def test_exchange_authorization_code(self):
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        credentialutil.load(app_config_path)
        oauth2api_inst = oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(environment.PRODUCTION, app_scopes)
        code = get_authorization_code(signin_url)
        user_token = oauth2api_inst.exchange_code_for_access_token(environment.PRODUCTION, code)
        self.assertIsNotNone(user_token.access_token)
        self.assertTrue(len(user_token.access_token) > 0)
        print ('\n *** test_get_user_access_token ***:\n', user_token)

    def test_exchange_refresh_for_access_token(self):
        """리프레쉬 토큰 생성하기 ngrok로 호스트 안열어도되고 그냥 테스트시 등록되는 url 만 가져와서 넣기
        """
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        credentialutil.load(app_config_path)
        oauth2api_inst = oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(environment.PRODUCTION, app_scopes)
        code = get_authorization_code(signin_url)
        user_token = oauth2api_inst.exchange_code_for_access_token(environment.PRODUCTION, code)
        # self.assertIsNotNone(user_token.refresh_token)
        # self.assertTrue(len(user_token.refresh_token) > 0)
        
        user_token = oauth2api_inst.get_access_token(environment.PRODUCTION, user_token.refresh_token, app_scopes)
        # self.assertIsNotNone(user_token.access_token)
        # self.assertTrue(len(user_token.access_token) > 0)

        print ('\n *** test_refresh_user_access_token ***:\n', user_token,'\n\n',user_token.refresh_token)

    def test_access_token(refresh_token):
        """유저엑세스토큰생성
        """
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        credentialutil.load(app_config_path)
        oauth2api_inst = oauth2api()
        # code = get_authorization_code(signin_url)
        # signin_url = oauth2api_inst.generate_user_authorization_url(environment.PRODUCTION, app_scopes)
        user_token = oauth2api_inst.get_access_token(environment.PRODUCTION, refresh_token, app_scopes)
        
        return user_token
        
if __name__ == '__main__':
    unittest.main()