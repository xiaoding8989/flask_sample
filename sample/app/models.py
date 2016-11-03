# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,AnonymousUserMixin,LoginManager
from datetime import datetime
from markdown import markdown
from flask_babel import gettext as _
#使用flask_login完成登录功能
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='.login'

db=SQLAlchemy()
#设计数据库模型
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=True)
    user=db.relationship('User',backref='role')

    @staticmethod
    def seed():
        db.session.add_all(map(lambda r:Role(name=r),['Guests','Administrators']))
        db.session.commit()

class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=True)
    email=db.Column(db.String(50))
    password=db.Column(db.String(30),nullable=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    posts=db.relationship('Post',backref='author')
    comments=db.relationship('Comment',backref='author')

    locale=db.Column(db.String(80),default='zh')

    @staticmethod
    def on_created(target,value,oldvalue,initiator):
        target.role=Role.query.filter_by(name='Guests').first()

class AnonymousUser(AnonymousUserMixin):
    @property
    def locale(self):
        return 'zh'

    def is_administrator(self):
        return False
login_manager.anonymous_user=AnonymousUser

#user_loader回调接受用户id返回用户对象
@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

db.event.listen(User.name,'set',User.on_created)


class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text)
    body=db.Column(db.Text)
    body_html=db.Column(db.Text)
    created=db.Column(db.DateTime,index=True,default=datetime.utcnow)

    comments=db.relationship('Comment',backref='post')
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    @staticmethod
    def on_body_changed(target,value,oldvalue,initiator):
        if value is None or (value is ''):
            target.body_html=''
        else:
            #调用markdown插件，数据转换
            target.body_html=markdown(value)

#事件监听当Post.body被设置的时候，调用后面的方法
db.event.listen(Post.body,'set',Post.on_body_changed)

#评论模型
class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    created=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'))
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))




















