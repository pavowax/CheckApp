import internal.service.post as post
import internal.model.messages as messages
import internal.model.transform as transform
from flask import Flask,request, session, redirect, url_for,make_response
import traceback


class PostApi:
    def __init__(self, service: post.Service, app: Flask):
        self.service = service
        self.app = app

        @self.app.route("/api/merhaba", methods=['POST'])
        def merhaba():
            return "Merhaba"
        
        @self.app.before_request
        def before_request():
            try:
                if request.path == '/api/index' or request.path == '/api/login' or request.path == '/api':
                    pass
                elif request.path == '/api/register':
                    if self.service.redis.exists('session'):
                        if f"{session}"==f"{self.service.redis.get('session').decode('utf-8')}":
                            return messages.response(f"{messages.status.BadRequest}",f"{messages.response_messages.already_looged_in}").dictionary,f"{messages.status.BadRequest}"
                        else:
                            pass
                    else:
                        pass
                else:
                    if self.service.redis.exists('session'):
                        if f"{session}"==f"{self.service.redis.get('session').decode('utf-8')}":
                            pass
                        else:
                            return messages.response(f"{messages.status.Unauthorized}",f"{messages.status.unauthorized_message}").dictionary,f"{messages.status.Unauthorized}"
                    else:
                        return messages.response(f"{messages.status.Unauthorized}",f"{messages.status.unauthorized_message}").dictionary,f"{messages.status.Unauthorized}"
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                    # traceback.print_exc(file=file)
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"
        
        @self.app.route("/api/register", methods=['POST'])
        def register():
            try:
                user_name = request.form['username']
                password = request.form['password']
                email = request.form['email']
                phone_number = request.form['phone_number']
                params=transform.user_transform_object(user_name,password,email,phone_number)
                return self.service.register(params)
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"
       
       
        # @self.app.route('/api')
        # def home():
        #     try:
        #         return redirect(url_for('/api/index'))
        #     except:
        #         with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
        #             file.write(f"{traceback.format_exc()}\n")
        #         return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"

        @self.app.route('/api/login', methods=['POST'])
        def login():
            try:
                user_name = request.form['username']
                password = request.form['password']
                return self.service.login(session,user_name,password)
                
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"

        @self.app.route('/api/logout')
        def logout():
            try:
                return self.service.logout(session)
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"

        @self.app.route('/api/index', endpoint='/api/index')
        def index(): 
            try:
                return service.index(session)
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"
                

        @self.app.route('/api/waf_test')
        def waf_test():    
            try:
                address=request.args.get('address') #kontrol
                return self.service.waf_test(address)
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"

        @self.app.route('/api/wappalyzer_test')
        def wappalyzer_test():
            try:
                address=request.args.get('address') #kontrol
                return self.service.wappalyzer_test(address)
            except:
                with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
                    file.write(f"{traceback.format_exc()}\n")
                return messages.response(f"{messages.status.InternalServerError}",f"{messages.status.internal_server_error_message}").dictionary,f"{messages.status.InternalServerError}"

    def migrate(self):

        self.app.app_context().push()
        self.service.repository.db.create_all() 

        admin_username='admin'
        admin_user = self.service.repository.model_user.query.filter_by(user_name=admin_username).first()

        if admin_user is None:
            new_admin = self.service.repository.model_user(user_name=admin_username, password='admin123', email='admin@example.com', role='admin', phone_number='1234567890')
            self.service.repository.db.session.add(new_admin)
            self.service.repository.db.session.commit()
    

    