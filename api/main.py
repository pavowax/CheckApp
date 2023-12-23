import redis
import app.initialize as initialize
from flask import Flask,request, session, redirect, url_for,make_response, jsonify  
import secrets
import app.messages as my_app
import traceback 
import waf.wafw00f.main as waf_script
from Wappalyzer import WebPage, Wappalyzer

app = Flask(__name__)

app_redis = redis.Redis(host='redis', port=6379, db=0)

app.secret_key = secrets.token_hex(64).encode('utf-8')


@app.before_request
def before_request():
    try:
        if request.path == '/index' or request.path == '/login' or request.path == '/':
            pass
        elif request.path == '/register':
            if app_redis.exists('session'):
                if f"{session}"==f"{app_redis.get('session').decode('utf-8')}":
                    return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.response_messages.already_looged_in}").dictionary,f"{my_app.status.BadRequest}"
                else:
                    pass
            else:
                pass
        else:
            if app_redis.exists('session'):
                if f"{session}"==f"{app_redis.get('session').decode('utf-8')}":
                    pass
                else:
                    return my_app.response(f"{my_app.status.Unauthorized}",f"{my_app.status.unauthorized_message}").dictionary,f"{my_app.status.Unauthorized}"
            else:
                return my_app.response(f"{my_app.status.Unauthorized}",f"{my_app.status.unauthorized_message}").dictionary,f"{my_app.status.Unauthorized}"
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
            # traceback.print_exc(file=file)
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"


@app.route("/register", methods=['POST'])
def register():
    user_name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone_number = request.form['phone_number']

    if user_name is not None and password is not None and email is not None and phone_number is not None:
        users_table = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)
        uery = db.session.query(users_table).filter_by(user_name=user_name).first()
        if uery is None:
            new_user = class_user(user_name=user_name, password=password, email=email, phone_number=phone_number)
            db.session.add(new_user)
            db.session.commit()
            return my_app.response(f"{my_app.status.OK}",f"{my_app.status.ok_message}").dictionary,f"{my_app.status.OK}"
        else:
            return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.response_messages.user_already_exist}").dictionary,f"{my_app.status.BadRequest}"
    else:
        return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.response_messages.should_not_be_empty}").dictionary,f"{my_app.status.BadRequest}"


@app.route('/')
def home():
    try:
        return redirect(url_for('index'))
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"

@app.route('/login', methods=['POST'])
def login():
    try:
        user_name = request.form['username']
        password = request.form['password']
        if user_name is not None:
            users_table = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)
            uery = db.session.query(users_table).filter_by(user_name=user_name).first()
            if uery is not None and password == uery.password:
                
                resp=make_response(my_app.response(f"{my_app.status.OK}",f"{my_app.status.ok_message}").dictionary, f"{my_app.status.OK}")
                session['username'] = user_name
                app_redis.set('session', f'{session}')
                #resp.headers.add('Set-Cookie', f'session={session};')
                resp.set_cookie('session', f'{app_redis.get("session").decode("utf-8")}', secure=True, httponly=True)
                
                return  resp
            else:
                return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.response_messages.wrong_username_or_password}").dictionary,f"{my_app.status.BadRequest}"
        else:
            return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.response_messages.wrong_username_or_password}").dictionary,f"{my_app.status.BadRequest}"
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"

@app.route('/logout')
def logout():
    try:
        deleted=app_redis.delete('session')
        session.clear()
        if not deleted:
            return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.status.unauthorized_message}").dictionary,f"{my_app.status.BadRequest}"
        else:
            return redirect(url_for('index'))
        # if app_redis.exists('username'):
        #     deleted=app_redis.delete('username')
        #     if not deleted:
        #         return my_app.response(f"{my_app.status.BadRequest}",f"{my_app.status.unauthorized_message}").dictionary,f"{my_app.status.BadRequest}"
        #     else:
        #         return redirect(url_for('index'))
        # else:
        #     return my_app.response(f"{my_app.status.Unauthorized}",f"{my_app.status.unauthorized_message}").dictionary,f"{my_app.status.Unauthorized}"
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"

@app.route('/index')
def index(): 
    try:
        if app_redis.exists('session') and 'username' in session:
            user_name = session['username']
            if f"{session}"==f"{app_redis.get('session').decode('utf-8')}" and user_name is not None:
                users_table = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)
                uery = db.session.query(users_table).filter_by(user_name=user_name).first()
                
                if uery is not None:
                    return my_app.response_user_data(f"{my_app.status.OK}",f"{my_app.status.ok_message}",{"user_id:":f"{uery.id}","user_name:":f"{uery.user_name}","email:":f"{uery.email}","role:":f"{uery.role}","phone_number:":f"{uery.phone_number}"}).dictionary,f"{my_app.status.OK}"
                else:
                    return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.response_messages.user_not_exist}").dictionary,f"{my_app.status.InternalServerError}"
            else:
                return my_app.response(f"{my_app.status.OK}",f"{my_app.response_messages.unauthorized_access}").dictionary,f"{my_app.status.OK}"#tekrar
        else:
            return my_app.response(f"{my_app.status.OK}",f"{my_app.response_messages.unauthorized_access}").dictionary,f"{my_app.status.OK}"
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"
        

@app.route('/waf_test')
def waf_test():    
    try:
        address=request.args.get('address')
        if address is not None:
            result=waf_script.waf_ps(address)
            return jsonify(result)
        else:
            return jsonify({"error":f"address parametresi eksik"}),400
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"

@app.route('/wappalyzer_test')
def wappalyzer_test():
    try:
        address=request.args.get('address') #kontrol
        if address is not None:
            webpage = WebPage.new_from_url(address)
            wappalyzer = Wappalyzer.latest()
            return wappalyzer.analyze_with_versions_and_categories(webpage)
        else:
            return jsonify({"error":f"address parametresi eksik"}),400
    except:
        with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
            file.write(f"{traceback.format_exc()}\n")
        return my_app.response(f"{my_app.status.InternalServerError}",f"{my_app.status.internal_server_error_message}").dictionary,f"{my_app.status.InternalServerError}"




if __name__ == '__main__':
    db,class_user=initialize.initialize(app)
    app.run(host='0.0.0.0',port=8080,debug=True)

