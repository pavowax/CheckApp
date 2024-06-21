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
from pkg.sqli. dsss import scan_page as sqli_scan
import urllib.parse
import traceback
import hashlib
from typing import Tuple

import threading
from concurrent.futures import ThreadPoolExecutor


print_lock = threading.Lock()

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
            return create_response(2007)

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
        result=wappalyzer.analyze_with_versions_and_categories(webpage)
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
        # with open("/var/log/ssti.txt", "a",encoding='utf-8') as file:
        #     file.write(f"ssti: {address}\n")
        channel=ssti_map(address)

        if channel is not None:
            if channel.result:
                return channel.result
            else:
                return None
        else:
            return None
        
    def xss(self,address:str):
        result=xsstrike.func(address)
        if result:
            return result
        else:
            return None
        
    def sqli(self,address:str):
        result=sqli_scan(address)
        if result[0]:
            return result[1]
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
            return None

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
    
    def scanner(self,address,user_parameter,passive,active,reputation):
        data={}
        def task1(address,passive):
            with print_lock:    
                with open("/var/log/threads.txt", "a",encoding='utf-8') as file:
                    file.write(f"from task1 thread num: {threading.get_ident()}\n")
            passiv_dns_a={}
            passiv_dns_mx={}
            passiv_subdomains={}
            passiv_whois={}
            passiv_ssl={}
            if passive:
                passiv_dns_a=self.securitytrails_dns_a(address)
                passiv_dns_mx=self.securitytrails_dns_mx(address)
                passiv_subdomains=self.securitytrails_subdomains(address)
                passiv_whois=self.jsonwhois(address)
                passiv_ssl=self.certspotter(address)

                data["passive_dns_a"]=passiv_dns_a
                data["passive_dns_mx"]=passiv_dns_mx
                data["passive_subdomains"]=passiv_subdomains
                data["passive_whois"]=passiv_whois
                data["passive_ssl"]=passiv_ssl
        
        def task2(address,reputation):
            with print_lock:    
                with open("/var/log/threads.txt", "a",encoding='utf-8') as file:
                    file.write(f"from task2 thread num: {threading.get_ident()}\n")
            if reputation:
                reput_aa419={}
                reput_urlhaus={}
                reput_threadfox={}

                result_aa419=self.aa419(address)

                
                if result_aa419 is None:
                    reput_aa419['query_status']="no_results"
                    reput_aa419['ScamType']=None
                else:
                    reput_aa419['query_status']=result_aa419[0]
                    reput_aa419['ScamType']=None
                    if result_aa419[1] is not None:
                        reput_aa419['ScamType']=result_aa419[1]

                result_urlhaus=self.urlhuas_urls(address)
                if result_urlhaus is None:
                    reput_urlhaus['query_status']="no_results"
                    reput_urlhaus['threat']=None
                else:
                    reput_urlhaus['query_status']=result_urlhaus[0]
                    reput_urlhaus['threat']=None
                    if result_urlhaus[1] is not None:
                        reput_urlhaus['threat']=result_urlhaus[1]
                
                result_threadfox=self.threatfox_iocs(address)
                if result_threadfox is None:
                    reput_threadfox['query_status']="no_results"
                    reput_threadfox['threat_type']=None
                else:
                    reput_threadfox['query_status']=result_threadfox[0]
                    reput_threadfox['threat_type']=None
                    if result_threadfox[1] is not None:
                        reput_threadfox['threat_type']=result_threadfox[1]
                
                data["reputation_aa419"]=reput_aa419
                data["reputation_urlhaus"]=reput_urlhaus
                data["reputation_threadfox"]=reput_threadfox

        def task3(address,user_parameter,active):
            with print_lock:    
                with open("/var/log/threads.txt", "a",encoding='utf-8') as file:
                    file.write(f"from task3 thread num: {threading.get_ident()}\n")
            if active:
                xss={}
                ssti_r={}
                sqli={}
                if isinstance(user_parameter, list) is False:
                    return create_response(2303)
                if not user_parameter:
                    user_parameter=None

                # if not address.endswith("/"):
                #     address=f"{address}/"
                
                result_parameter=self.parameter(address)

                if user_parameter is not None:
                    for i in user_parameter:
                        result_parameter.append(i)

                if result_parameter is not None:
                    with ThreadPoolExecutor(max_workers=8) as executor:
                        [executor.submit(self.paralel_executer,address, item,result_parameter,xss,ssti_r,sqli) for item in result_parameter]
                else:
                    xss=None
                    ssti_r=None
                    sqli=None

                result_sub=self.sublister(address)
                data["sublister"]=result_sub

                result_wapp=self.wappalyzer(address)
                data["wappalyzer"]=result_wapp

                result_waf=self.waf(address)
                data["waf"]=result_waf

                data["xss"]=xss
                data["ssti"]=ssti_r
                data["sqli"]=sqli

        thread1 = threading.Thread(target=task1,args=(address,passive,))
        thread2 = threading.Thread(target=task2,args=(address,reputation,))
        thread3 = threading.Thread(target=task3, args=(address,user_parameter,active,))

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()
        
        return data




    def paralel_executer(self,address,parameter,result_parameter,xss,ssti_r,sqli):
        with print_lock:    
            with open("/var/log/threads.txt", "a",encoding='utf-8') as file:
                file.write(f"num: {threading.get_ident()}\n")

        
        if 'Submit' in result_parameter:
            if parameter != "submit" and parameter != "Submit":
                parameter =f"{parameter}&Submit"
                new_address=f"{address}?{parameter}="
            else:
                new_address=f"{address}?{parameter}="
        elif 'submit' in result_parameter:
            if parameter != "submit" and parameter != "Submit":
                parameter =f"{parameter}&submit"
                new_address=f"{address}?{parameter}="
            else:
                new_address=f"{address}?{parameter}="
        else:
            new_address=f"{address}?{parameter}="

        xss_result=self.xss(new_address)
        if xss_result is not None:
            xss[parameter]=xss_result
        else:
            xss[parameter]="None"

        ssti_result=self.ssti(new_address)
        if ssti_result is not None:
            ssti_r[parameter]=ssti_result
        else:
            ssti_r[parameter]="None"
        
        sqli_result=self.sqli(new_address)
        if sqli_result is not None:
            sqli[parameter]=sqli_result
        else:
            sqli[parameter]="None"