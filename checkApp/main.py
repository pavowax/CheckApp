import redis
from flask import Flask, jsonify
import secrets
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.append("/app")
from jwt import ExpiredSignatureError

import internal.repository.post as postRepository
import internal.service.post as postService
import internal.api.post as postApi
from flask_jwt_extended import JWTManager

from datetime import timedelta

ACCESS_EXPIRES = timedelta(days=1)


class checkApp:
    def __init__(self):
        self.app = Flask(__name__)
        
    def initialize(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/my-flask-app'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app.config["JWT_SECRET_KEY"] = "asdasd??..123125DSGSDG.."  # Change this!
        self.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

        self.db = SQLAlchemy(self.app)

        self.jwt = JWTManager(self.app)
        
        self.redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        # self.app.secret_key = secrets.token_hex(64).encode('utf-8')


    def run(self,port = 6700):
        self.app.run(host='0.0.0.0',port=port,debug=True)


    def init_post_api(self):
        post_repository=postRepository.Repository(self.db)
        post_repository.migrate()
        post_service=postService.Service(post_repository)
        post_api=postApi.PostApi(post_service,self.app,self.redis)
        post_api.migrate()

if __name__ == '__main__':
    a=checkApp()
    a.initialize()
    a.init_post_api()
    a.run()
