# coding=utf-8
from flask import render_template,redirect,url_for,request
from forms import RegistrationForm,LoginForm,CommentForm,PostForm
from app.models import *
from flask_login import login_user,logout_user,current_user,login_required
from flask_babel import gettext as _


def init__views(app):
    #主页
    @app.route('/')
    def index():
        #文章数据的获取
        #posts=Post.query.all()
        #获得当前页面的索引第几页
        #page为url的参数，默认值为1，相当于page=page_index,默认为page=1
        page_index=request.args.get('page',1,type=int)
        #定义一个查询，反向排序
        query=Post.query.order_by(Post.created.desc())
        #定义一个分页
        pagination=query.paginate(page_index,per_page=20,error_out=False)
        #items为pagination的参数
        posts=pagination.items
        return render_template('index.html',title=u"欢迎来到avin的博客系统",
                               posts=posts,pagination=pagination)

    @app.route('/about')
    def about():
        return render_template('about.html',title=u'关于')

#登录的页面
    @app.route('/login',methods=['GET','POST'])
    def login():
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(name=form.username.data, password=form.password.data).first()
            if user is not None:
                login_user(user)
                return redirect(url_for('.index'))
        return render_template('login.html',
                               title=u'登录',
                               form=form)
#注销页面
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('.login'))

# #注册的页面
    @app.route('/register',methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        name=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('.login'))
        return render_template('register.html', title=u'注册', form=form)

#文章详情的页面
    @app.route('/posts/<int:id>',methods=['GET','POST'])
    def post(id):
        #Detail详情页
        post=Post.query.get_or_404(id)
        #评论表单
        form=CommentForm()
        #保存评论
        if form.validate_on_submit():
            comment=Comment(author=current_user,
                            body=form.body.data,
                            post=post)
            db.session.add(comment)
            db.session.commit()
        return render_template('detail.html',title=post.title,
                               form=form,post=post)

    @app.route('/edit',methods=['GET','POST'])
    @app.route('/edit/<int:id>',methods=['GET','POST'])
    @login_required
    def edit(id=0):
        form =PostForm()
        if id==0:
            post=Post(author=current_user)
        else:
            post=Post.query.get_or_404(id)

        if form.validate_on_submit():
            post.body=form.body.data
            post.title=form.title.data

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('.post',id=post.id))

        form.title.data=post.title
        form.body.data=post.body

        title=u'添加新文章'
        if id >0:
            mode=u'编辑-%'%post.title

        return render_template('posts/edit.html',
                               title=title,
                               form=form,post=post)
















