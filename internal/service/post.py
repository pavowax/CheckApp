import internal.repository.post as post
from redis import Redis
import internal.model.transform as transform
import internal.model.messages as messages
from flask.sessions import SessionMixin
from flask import make_response
from Wappalyzer import WebPage, Wappalyzer
import pkg.waf.wafw00f.main as waf_script

class Service:
    def __init__(self, repository: post.Repository, redis: Redis):
        self.repository = repository
        self.redis = redis

    def register(self,transform_obj: transform.user_transform_object):
        if transform_obj.user_name is not None and transform_obj.password is not None and transform_obj.email is not None and transform_obj.phone_number is not None:
            uery = self.repository.find_user_with_username(transform_obj.user_name)
            if uery is None:
                new_user = self.repository.model_user(user_name=transform_obj.user_name, password=transform_obj.password, email=transform_obj.email, phone_number=transform_obj.phone_number)
                self.repository.create_new_db_object(new_user)
                return messages.response(f"{messages.status.OK}",f"{messages.status.ok_message}").dictionary,f"{messages.status.OK}"
            else:
                return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.user_already_exist}").dictionary,f"{messages.status.BadRequest}"
        else:
            return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.should_not_be_empty}").dictionary,f"{messages.status.BadRequest}"

    def index(self,session: SessionMixin):
        if self.redis.exists('session') and 'username' in session:
            user_name = session['username']
            if f"{session}"==f"{self.redis.get('session').decode('utf-8')}" and user_name is not None:

                uery = self.repository.find_user_with_username(user_name)   
                if uery is not None:
                    return messages.response_user_data(f"{messages.status.OK}",f"{messages.status.ok_message}",{"user_id:":f"{uery.id}","user_name:":f"{uery.user_name}","email:":f"{uery.email}","role:":f"{uery.role}","phone_number:":f"{uery.phone_number}"}).dictionary,f"{messages.status.OK}"
                else:
                    return messages.response(f"{messages.status.InternalServerError}",f"{messages.response_messages.user_not_exist}").dictionary,f"{messages.status.InternalServerError}"
            else:
                return messages.response(f"{messages.status.OK}",f"{messages.response_messages.unauthorized_access}").dictionary,f"{messages.status.OK}"#tekrar
        else:
            return messages.response(f"{messages.status.OK}",f"{messages.response_messages.unauthorized_access}").dictionary,f"{messages.status.OK}"

    def logout(self,session: SessionMixin):
        deleted=self.redis.delete('session')
        session.clear()
        if not deleted:
            return messages.response(f"{messages.status.BadRequest}",f"{messages.status.unauthorized_message}").dictionary,f"{messages.status.BadRequest}"
        else:
            return messages.response(f"{messages.status.OK}",f"{messages.status.ok_message}").dictionary, f"{messages.status.OK}"
        # if self.service.redis.exists('username'):
        #     deleted=self.service.redis.delete('username')
        #     if not deleted:
        #         return messages.response(f"{messages.status.BadRequest}",f"{messages.status.unauthorized_message}").dictionary,f"{messages.status.BadRequest}"
        #     else:
        #         return messages.response(f"{messages.status.OK}",f"{messages.status.ok_message}").dictionary, f"{messages.status.OK}"
        # else:
        #     return messages.response(f"{messages.status.Unauthorized}",f"{messages.status.unauthorized_message}").dictionary,f"{messages.status.Unauthorized}"

    def login(self,session: SessionMixin,user_name:str,password:str):

        if user_name is not None:
            uery = self.repository.find_user_with_username(user_name)
            if uery is not None and password == uery.password:
                
                resp=make_response(messages.response(f"{messages.status.OK}",f"{messages.status.ok_message}").dictionary, f"{messages.status.OK}")
                session['username'] = user_name
                self.redis.set('session', f'{session}')
                #resp.headers.add('Set-Cookie', f'session={session};')
                resp.set_cookie('session', f'{self.redis.get("session").decode("utf-8")}', secure=True, httponly=True)
                
                return  resp
            else:
                return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.wrong_username_or_password}").dictionary,f"{messages.status.BadRequest}"
        else:
            return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.wrong_username_or_password}").dictionary,f"{messages.status.BadRequest}"
        
    def waf_test(self,address:str):

        if address is not None:
            result=waf_script.waf_ps(address)
            if result is not None:
                return  messages.response(f"{messages.status.OK}",f"{messages.status.ok_message}",f"{result}").dictionary,f"{messages.status.OK}"
            else:
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"
        else:
            return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.no_address_parameter}").dictionary,f"{messages.status.BadRequest}"

    def wappalyzer_test(self,address:str):
        if address is not None:
            webpage = WebPage.new_from_url(address)
            wappalyzer = Wappalyzer.latest()
            return messages.response(f"{messages.status.OK}",f"{messages.status.ok_message}",f"{wappalyzer.analyze_with_versions_and_categories(webpage)}").dictionary,f"{messages.status.OK}"
        else:
            return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.no_address_parameter}").dictionary,f"{messages.status.BadRequest}"
