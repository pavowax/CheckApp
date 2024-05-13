import internal.repository.post as post
from redis import Redis
import internal.model.transform as transform
import internal.model.messages as messages
from flask.sessions import SessionMixin
from flask import make_response
from Wappalyzer import WebPage, Wappalyzer
import pkg.waf.wafw00f.main as waf_script
from pkg.utils.regex import pull_environment_and_check as regex_check
from pkg.utils.messages import create_response
from pkg.Sublist3r.sublist3r import main as sublist3r
from pkg.ArjunMaster.arjun import __main__ as arjun


import hashlib
from typing import Tuple


class Service:
    def __init__(self, repository: post.Repository):
        self.repository = repository
        # self.redis = redis

    def register(self,transform_obj: transform.user_transform_object):
        if transform_obj.user_name is not None and transform_obj.password is not None and transform_obj.email is not None and transform_obj.phone_number is not None:
            if regex_check('username_regex',transform_obj.user_name) is False:
                return create_response(2200)
            elif regex_check('password_regex',transform_obj.password) is False:
                return create_response(2201)
            elif regex_check('email_regex',transform_obj.email) is False:
                return create_response(2202)
            elif regex_check('phone_number_regex',transform_obj.phone_number) is False:
                return create_response(2203)
            
            uery = self.repository.find_user_with_username_email_phonenumber(transform_obj)
            if uery is None:
                hashed_password = hashlib.sha256(transform_obj.password.encode()).hexdigest()
                new_user = self.repository.model_user(user_name=transform_obj.user_name, password=hashed_password, email=transform_obj.email, phone_number=transform_obj.phone_number)
                self.repository.create_new_db_object(new_user)
                return create_response(100)
            else:
                if uery.user_name == transform_obj.user_name:
                    return create_response(2004)
                elif uery.email == transform_obj.email:
                    return create_response(2005)
                elif uery.phone_number == transform_obj.phone_number:
                    return create_response(2006)
                else:
                    return create_response(2007)
        else:
            return create_response(2008)

    def login(self,user_name:str,password:str) ->  Tuple[bool, str]:

        if user_name is not None:
            uery = self.repository.find_user_with_username(user_name)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if uery is not None and hashed_password == uery.password:

                return True, uery.role
            else:
                return False,""
        else:
            return False,""

    def waf(self,address:str):
        if regex_check('url_regex',address) is False:
            return create_response(2204)
        if address is not None:
            result=waf_script.waf_ps(address)
            if result is not None:
                return  create_response(100,data=result)
            else:
                return create_response(7107)
        else:
            return create_response(2009)

    def wappalyzer(self,address:str):
        if regex_check('url_regex',address) is False:
            return create_response(2204)
        if address is not None:
            webpage = WebPage.new_from_url(address)
            wappalyzer = Wappalyzer.latest()
            return create_response(100,data=wappalyzer.analyze(webpage))
        else:
            return create_response(2009)


    def sublister(self,address:str):
        # if regex_check('url_regex',address) is False:
        #     return create_response(2204)
        if address is not None:
            result=sublist3r(address, 36, ports= None, silent=True, verbose= False, enable_bruteforce= False, engines=None)
            if result:
                return  create_response(100,data=result)
            else:
                return create_response(7107)
        else:
            return create_response(2009)
        


    def parameter(self,address:str):
        if regex_check('url_regex',address) is False:
            return create_response(2204)
        if address is not None:
            url="https://cyrops.com"
            # wordlist="wordlist.txt"

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'close',
                'Upgrade-Insecure-Requests': '1'
            }

            request={
                'url': url,
                'method': 'GET',
                'headers': headers,
            }
            passive=True    
            result=arjun.initialize(request,passive,True)            
            if result:
                return  create_response(100,data=result)
            else:
                return create_response(7107)
        else:
            return create_response(2009)