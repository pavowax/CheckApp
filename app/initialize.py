from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime, timedelta




def initialize(app: Flask):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/my-flask-app'
    db = SQLAlchemy(app)

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        user_name = db.Column(db.String(80), unique=True, nullable=False)
        password = db.Column(db.String(120), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        role = db.Column(db.String(40), nullable=False, default='user')
        phone_number = db.Column(db.String(40),unique=True, nullable=False)
        created_date = db.Column(db.DateTime(timezone=True), default=(datetime.now() + timedelta(hours=3)))
    # @event.listens_for(User, 'before_update')
    # def before_update_listener(mapper, connection, target):
    #     target.created_date = datetime.now() + timedelta(hours=3) 

    app.app_context().push()
    db.create_all()     

    admin_username='admin'
    admin_user = User.query.filter_by(user_name=admin_username).first()

    if admin_user is None:
        new_admin = User(user_name=admin_username, password='admin123', email='admin@example.com', role='admin', phone_number='1234567890')
        db.session.add(new_admin)
        db.session.commit()

    return db,User
