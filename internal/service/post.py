import internal.repository.post as post
from redis import Redis
import internal.model.transform as transform
import internal.model.messages as messages
from flask.sessions import SessionMixin
from flask import make_response
from Wappalyzer import WebPage, Wappalyzer
import pkg.waf.wafw00f.main as waf_script
from pkg.utils.regex import pull_environment_and_check as regex_check
from pkg.utils.regex import pull_environment
import requests
import json

from pkg.utils.messages import create_response
from pkg.Sublist3r.sublist3r import main as sublist3r
from pkg.SSTImap.core.checks import scan_website as ssti_map
from pkg.ArjunMaster.arjun import __main__ as arjun
from pkg.XSStrike import xsstrike 
import urllib.parse
import traceback
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
        result=waf_script.waf_ps(address)
        if result is not None:
            return result
        else:
            return None


    def wappalyzer(self,address:str):
       
        webpage = WebPage.new_from_url(address)
        wappalyzer = Wappalyzer.latest()
        result=wappalyzer.analyze(webpage)
        if result:
            return result
        else:
            return None


    def sublister(self,address:str):
        parsed_url = urllib.parse.urlparse(address)
        address = parsed_url.netloc
        result=sublist3r(address, 36, ports= None, silent=True, verbose= False, enable_bruteforce= False, engines=None)
        if result:
            return result
        else:
            return None
        
        
    def parameter(self,address:str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }

        request={
            'url': address,
            'method': 'GET',
            'headers': headers,
        }
        passive=True    

        result= arjun.initialize(request,passive,True)
        if isinstance(result,list):
            return result
        else:
            return result
     
    def ssti(self,address:str):
        with open("/var/log/ssti.txt", "a",encoding='utf-8') as file:
            file.write(f"ssti: {address}\n")
        channel=ssti_map(address)

        if channel is not None:
            if channel.result:
                return channel.result
            else:
                return None
        else:
            return None
        
    def xss(self,address:str):
        with open("/var/log/XSS.txt", "a",encoding='utf-8') as file:
            file.write(f"XSS: {address}\n")

        result=xsstrike.func(address)
        if result:
            return result
        else:
            return None
        
    def threatfox_iocs(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='THREATFOX_API_URL'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        data = { "query": "search_ioc", "search_term": f"{domain}" }
        json_data=json.dumps(data)

        response = requests.post(url, data=json_data, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        if json_response['query_status']:
            if json_response['query_status'] == "ok":
                return json_response['query_status'],json_response['data'][0]['threat_type']
            else:
                return json_response['query_status'],None
        else:
            return None
        


    def urlhuas_urls(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='URLHAUS_URLS_API_URL'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        # data = { "query": "search_ioc", "search_term": f"{domain}" }
        # json_data=json.dumps(data)

        form_data = {
            'host': domain
        }

        response = requests.post(url, data=form_data, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        if json_response['query_status']:
            if json_response['query_status'] == "ok":
                return json_response['query_status'],json_response['urls'][0]['threat']
            else:
                return json_response['query_status'],None
        else:
            return None
            
    def aa419(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='AA419_API_URL'
        env_authID='AA419_AUTH_API_ID'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        authID,is_false=pull_environment(env_authID,from_variable)
        if is_false is False:
            return None

        url=f"{url}{domain}"

        headers = {
            'Auth-API-Id':f"{authID}"
        }
 
        response = requests.get(url,headers=headers, timeout=10)
        if(response.status_code != 200 and response.status_code != 201):
            return f"{response.status_code}"

        js_response=json.loads(response.content)

        if isinstance(js_response, list) and js_response[0]['Expired'] == "0":
            if js_response[0]['ScamType']:
                return "ok",js_response[0]['ScamType']
            else:
                return "ok",None
        else:
            return None
        

    def jsonwhois(self,address:str):
        from_variable=traceback.extract_stack()[-1].name

        env_url='JSONWHOIS_API_URL'
        env_api_key='JSONWHOIS_API_KEY'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        api_key,is_false=pull_environment(env_api_key,from_variable)
        if is_false is False:
            return None
        
        params={"identifier":f"{address}"}

        headers = {
            'Authorization':f"Basic {api_key}"
        }

        response = requests.get(url, params=params,headers=headers, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        return json_response
    
    def certspotter(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='CERTSPOTTER_API_URL'
        env_api_key='CERTSPOTTER_API_KEY'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        api_key,is_false=pull_environment(env_api_key,from_variable)
        if is_false is False:
            return None
        
        params={
            "domain":f"{domain}",
            "expand":"dns_names",
            "expand":"issuer",
            "expand":"revocation",
            "expand":"problem_reporting",
            "expand":"cert_der"
        }

        headers = {
            'Authorization':f"Bearer {api_key}"
        }

        response = requests.get(url, params=params,headers=headers, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        return json_response
    

    def securitytrails_subdomains(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='SECURITYTRAILS_API_URL'
        env_api_key='SECURITYTRAILS_API_KEY'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        api_key,is_false=pull_environment(env_api_key,from_variable)
        if is_false is False:
            return None
        
        params={
            "children_only":f"false",
            "include_ips":f"true"
        }

        headers = {
            'APIKEY':f"{api_key}",
            'Content-Type': 'application/json'
        }

        url=f"{url}{domain}/subdomains"

        response = requests.get(url, params=params,headers=headers, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        return json_response
    

    def securitytrails_dns_a(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='SECURITYTRAILS_DNS_API_URL'
        env_api_key='SECURITYTRAILS_DNS_API_KEY'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        api_key,is_false=pull_environment(env_api_key,from_variable)
        if is_false is False:
            return None

        headers = {
            'APIKEY':f"{api_key}",
            'Content-Type': 'application/json'
        }

        url=f"{url}{domain}/dns/a"

        response = requests.get(url,headers=headers, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        return json_response
    
    def securitytrails_dns_mx(self,address:str):
        parsed_url=urllib.parse.urlparse(address)
        domain=parsed_url.netloc
        from_variable=traceback.extract_stack()[-1].name

        env_url='SECURITYTRAILS_DNS_API_URL'
        env_api_key='SECURITYTRAILS_DNS_API_KEY'

        url,is_false=pull_environment(env_url,from_variable)
        if is_false is False:
            return None
        
        api_key,is_false=pull_environment(env_api_key,from_variable)
        if is_false is False:
            return None

        headers = {
            'APIKEY':f"{api_key}",
            'Content-Type': 'application/json'
        }

        url=f"{url}{domain}/dns/mx"

        response = requests.get(url,headers=headers, timeout=10)
        if(response.status_code != 200):
            return None
        
        json_response=json.loads(response.content)
        return json_response