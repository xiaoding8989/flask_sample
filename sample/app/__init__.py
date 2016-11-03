# coding=utf-8
from flask import Flask
import pymysql
from views import init__views
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db,login_manager
from flask_login import current_user
from os import path
from flask_gravatar import Gravatar
from flask_pagedown import PageDown
from flask_babel import Babel,gettext as _

myapp = Flask(__name__)
pymysql.install_as_MySQLdb()
#实例化Bable()
babel=Babel()
nav=Nav()
#实例化pageDown
pagedown=PageDown()
def create_app():
    #myapp.config.from_pyfile('config')
    #防跨域请求配置文件
    myapp.secret_key="hard to guess string"
    #全球化配置文件
    #配置成中文
    myapp.config['BABEL_DEFAULT_LOCALE']='zh'
    # 获取绝对路径
    basedir = path.abspath(path.dirname(__file__))
    # 数据库的配置
    myapp.config['SQLALCHEMY_DATABASE_URI'] = \
       'mysql://root:123456@localhost:3306/sample'
        #'sqlite:///' + path.join(basedir, 'data.sqlite')
    myapp.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    #引用nav
    nav.register_element('top',Navbar(u'flask入门',
                                View(u'主页','index'),
                                View(u'项目', 'about'),
                               View(u'注册', 'register'),
                               View(u'登录', 'login'),
                                      ))

    @myapp.template_test('current_link')
    def is_current_link(link):
        return link == request.path
    #注册
    Gravatar(myapp,size=40)
    #注册nav
    nav.init_app(myapp)
    #调用视图函数里的init__views方法
    init__views(myapp)
    #注册bootstrap
    Bootstrap(myapp)
    #注册数据ku
    db.init_app(myapp)
    #注册登录的扩展
    login_manager.init_app(myapp)
    #注册pagedown
    pagedown.init_app(myapp)
    #注册babel
    babel.init_app(myapp)
    # #使用current_user
    # @babel.localeselector
    # def get_locale():
    #     return current_user.locale
    return myapp




