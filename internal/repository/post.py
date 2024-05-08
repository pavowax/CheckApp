from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime, timedelta
import internal.model.transform as transform



class Repository:
    def __init__(self,db: SQLAlchemy):
        self.db=db

    def find_user_with_username(self,user_name: str):
        users_table = self.db.Table('users', self.db.metadata, autoload=True, autoload_with=self.db.engine)
        uery = self.db.session.query(users_table).filter_by(user_name=user_name).first()
        return uery
    
    def find_user_with_username_email_phonenumber(self,transform_obj: transform.user_transform_object):
        # users_table = self.db.Table('users', self.db.metadata, autoload=True, autoload_with=self.db.engine)
        # uery = self.db.session.query(users_table).filter(or_(users_table.c.user_name==transform_obj.user_name, users_table.c.email==transform_obj.email, users_table.c.phone_number==transform_obj.phone_number)).first()
        # return uery
        users_table = self.db.Table('users', self.db.metadata, autoload=True, autoload_with=self.db.engine)
        uery = self.db.session.query(users_table).filter(or_(self.model_user.user_name==transform_obj.user_name, self.model_user.email==transform_obj.email, self.model_user.phone_number==transform_obj.phone_number)).first()
        return uery
        # matched_user = self.model_user.query.filter(or_(self.model_user.user_name==transform_obj.user_name, self.model_user.email==transform_obj.email, self.model_user.phone_number==transform_obj.phone_number)).first()
        # return matched_user 


    def create_new_db_object(self,db_object):
        self.db.session.add(db_object)
        self.db.session.commit()
    
    def migrate(self):

        class User(self.db.Model):
            __tablename__ = 'users'
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            user_name = self.db.Column(self.db.String(80), unique=True, nullable=False)
            password = self.db.Column(self.db.String(120), nullable=False)
            email = self.db.Column(self.db.String(120), unique=True, nullable=False)
            role = self.db.Column(self.db.String(40), nullable=False, default='user')
            phone_number = self.db.Column(self.db.String(40),unique=True, nullable=False)
            created_date = self.db.Column(self.db.DateTime(timezone=True), default=(datetime.now() + timedelta(hours=3)))
        # @event.listens_for(User, 'before_update')
        # def before_update_listener(mapper, connection, target):
        #     target.created_date = datetime.now() + timedelta(hours=3) 
        
        self.model_user=User
