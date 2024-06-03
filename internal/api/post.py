import internal.service.post as post
import internal.model.messages as messages
import internal.model.transform as transform
from flask import Flask,request,redirect, url_for,make_response,jsonify
from redis import Redis
from pkg.utils.messages import create_response  
from pkg.utils.regex import pull_environment_and_check as regex_check
import logging

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


from flask_jwt_extended import create_access_token,jwt_required,get_jwt,JWTManager

from datetime import timedelta

from fenrir.main import ACCESS_EXPIRES

from pkg.utils.error_handling import log_error

logger = logging.getLogger('post_api')


class PostApi:
    def __init__(self, service: post.Service, app: Flask, redis: Redis):
        self.service = service
        self.app = app
        self.redis = redis

        self.limiter = Limiter(get_remote_address,app=self.app)

        @self.app.route("/api/merhaba", methods=['POST'])
        def merhaba():
            return "Merhaba"
        
        @self.app.before_request
        @jwt_required(optional=True)
        def before_request():
            try:
                claims = get_jwt()
                if claims and self.redis.get(claims["jti"]) is not None:
                    return create_response(2300)
                
                if request.path == '/api/index' or request.path == '/api':
                    pass
                elif request.path == '/api/register' or request.path == '/api/login':
                    if claims:
                        return create_response(2008)
                    else:
                        pass
            except:
                log_error()
                return create_response(7107)
        
        @app.after_request
        @jwt_required(optional=True)
        def after_request(response):
            try:
                claims = get_jwt()
                if claims and self.redis.get(claims["jti"]) is None:
                    if claims["fresh"] is False:
                        additional_claims = {"role": claims["role"]}
                        jti = get_jwt()["jti"]
                        access_token=create_access_token(identity=claims["sub"],additional_claims=additional_claims,fresh=timedelta(hours=23))
                        response.headers['Authorization'] = f"Bearer {access_token}"
                        self.redis.set(jti, "", ex=ACCESS_EXPIRES)
                    else:
                        pass

                return response
            except:
                log_error()
                response.status_code = f"{500}"
                response.data= messages.response(f"{messages.status.InternalServerError}",{}).dictionary
                return response





        @self.app.route("/api/register", methods=['POST'])
        def register():
            try:
                user_name = request.json.get("username",None)
                password = request.json.get("password",None)
                email = request.json.get("email",None)
                phone_number = request.json.get("phone_number",None)
               

                params=transform.user_transform_object(user_name,password,email,phone_number)
                return self.service.register(params)
            except:
                log_error()
                return create_response(7107)
       
       
        # @self.app.route('/api')
        # def home():
        #     try:
        #         return redirect(url_for('/api/index'))
        #     except:
        #         log_error()
        #         return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"


        @self.app.route('/api/login', methods=['POST'])
        @self.limiter.limit('5/minute')        
        def login():
            try:
                user_name = request.json.get("username",None)
                password = request.json.get("password",None)
                is_true,role=self.service.login(user_name,password)
                if is_true:
                    resp=make_response(create_response(100))
                    additional_claims = {"role": role}
                    resp.headers['Authorization'] = f"Bearer {create_access_token(identity=user_name,additional_claims=additional_claims,fresh=timedelta(hours=23))}"
                    return resp
                else:
                    return create_response(2000)
                
            except:
                log_error()
                return create_response(7107)

        @self.app.route('/api/logout',methods=['DELETE']) 
        @jwt_required()
        def logout():
            try:
                jti = get_jwt()["jti"]
                self.redis.set(jti, "", ex=ACCESS_EXPIRES)
                return create_response(100)
            except:
                log_error()
                return create_response(7107)

        @self.app.route('/api/index', endpoint='/api/index')
        @jwt_required(optional=True)
        def index(): 
            try:
                claims = get_jwt()
                if claims:
                    return create_response(100,data={"Username": claims['sub'], "Role": claims['role']})
                else:
                    return create_response(100)
            except:
                log_error()
                return create_response(7107)
            
                
        @self.app.route('/api/scanner',methods=['POST'])
        @jwt_required()
        # @self.limiter.limit('1/minute')        
        def scanner():
            try:
                parameters=None
                data={}
                xss={}
                ssti_r={}
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                # address=request.args.get('address')
                content = request.json
    
                address = content.get('address')
                parameters = content.get('parameters')

                if isinstance(parameters, list) is False:
                    return create_response(2303)
                if not parameters:
                   parameters=None
                
                if address is None:
                    return create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                if not address.endswith("/"):
                    address=f"{address}/"
                
                result=self.service.parameter(address)

                if result is not None:
                    for i in result:
                        with open("/var/log/paramlog.txt", "a",encoding='utf-8') as file:
                            file.write(f"PARAMETER2: {i}\n")
                        # logger.info(f"SOLO PARAMETER: {i}\n")


                if parameters is not None:
                    for i in parameters:
                        result.append(i)

                if result is not None:
                    for i in result:
                        if 'Submit' in result:
                            if i != "submit" and i != "Submit":
                                i =f"{i}&Submit"
                                new_address=f"{address}?{i}="
                            else:
                                new_address=f"{address}?{i}="
                        elif 'submit' in result:
                            if i != "submit" and i != "Submit":
                                i =f"{i}&submit"
                                new_address=f"{address}?{i}="
                            else:
                                new_address=f"{address}?{i}="
                        else:
                            new_address=f"{address}?{i}="

                        xss_result=self.service.xss(new_address)
                        if xss_result is not None:
                            xss[i]=xss_result
                        else:
                            xss[i]="None"

                        ssti_result=self.service.ssti(new_address)
                        if ssti_result is not None:
                            ssti_r[i]=ssti_result
                        else:
                            ssti_r[i]="None"
                else:
                    xss=result

                result_sub=self.service.sublister(address)
                data["sublister"]=result_sub

                result_wapp=self.service.wappalyzer(address)
                data["wappalyzer"]=result_wapp

                result_waf=self.service.waf(address)
                data["waf"]=result_waf

                data["xss"]=xss
                data["ssti"]=ssti_r
                return create_response(100,data=data)
                
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/parameter',methods=['GET'])
        @jwt_required()
        def parameter():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address')
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)
                
                result=self.service.parameter(address)
                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/ssti')
        @jwt_required()
        def ssti():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result=self.service.ssti(address)
                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/waf')
        @jwt_required()
        def waf_test():    
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)                

                result= self.service.waf(address)
                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)

        @self.app.route('/api/wappalyzer')
        @jwt_required()
        def wappalyzer():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result= self.service.wappalyzer(address)
                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/sublist')
        @jwt_required()
        def sublister():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result= self.service.sublister(address)
                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/xss')
        @jwt_required()
        def xss():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result= self.service.xss(address)
                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/reputation_threadfox')
        @jwt_required()
        def reputation_threadfox():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result=self.service.threatfox_iocs(address)

                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        @self.app.route('/api/reputation_urlhaus')
        @jwt_required()
        def reputation_urlhaus():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result=self.service.urlhuas_urls(address)

                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
        
        @self.app.route('/api/reputation_aa419')
        @jwt_required()
        def reputation_aa419():
            try:
                claims = get_jwt()
                if claims["role"] != "admin":
                    return create_response(4104)
                
                address=request.args.get('address') #kontrol
                if address is None:
                    create_response(2009)
                # if regex_check('url_regex',address) is False:
                #     return create_response(2204)

                result=self.service.aa419(address)

                return create_response(100,data=result)
            except:
                log_error()
                return create_response(7107)
            
        
    def migrate(self):

        self.app.app_context().push()
        self.service.repository.db.create_all() 

        admin_username='admin'
        admin_user = self.service.repository.model_user.query.filter_by(user_name=admin_username).first()

        if admin_user is None:
            new_admin = self.service.repository.model_user(user_name=admin_username, password='240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', email='admin@example.com', role='admin', phone_number='1234567890')
            self.service.repository.db.session.add(new_admin)
            self.service.repository.db.session.commit()
    

    