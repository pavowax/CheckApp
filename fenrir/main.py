import redis
from flask import Flask 
import secrets
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.append("/app")

import internal.repository.post as postRepository
import internal.service.post as postService
import internal.api.post as postApi


class Fenrir:
    def __init__(self):
        self.app = Flask(__name__)
        
    def initialize(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/my-flask-app'
        self.db = SQLAlchemy(self.app)

        self.redis = redis.Redis(host='redis', port=6379, db=0)
        self.app.secret_key = secrets.token_hex(64).encode('utf-8')


    def run(self,port = 6700):
        self.app.run(host='0.0.0.0',port=port,debug=True)


    def init_post_api(self):
        post_repository=postRepository.Repository(self.db)
        post_repository.migrate()
        post_service=postService.Service(post_repository,self.redis)
        post_api=postApi.PostApi(post_service,self.app)
        post_api.migrate()

if __name__ == '__main__':
    a=Fenrir()
    a.initialize()
    a.init_post_api()
    a.run()
