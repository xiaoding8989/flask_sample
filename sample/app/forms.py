# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from flask.ext.pagedown.fields import PageDownField
#加入校验器
from wtforms.validators import DataRequired,EqualTo,Email,Regexp,Length


class LoginForm(Form):
    username=StringField( label=u'用户名',validators=[DataRequired()])
    password=PasswordField(label=u'密码',validators=[DataRequired()])
    submit=SubmitField(label=u'提交')

#validators代表校验器
class RegistrationForm(Form):
    email=StringField(label=u'邮箱地址',validators=[DataRequired(),Length(1,64),Email()])

    username=StringField(label=u'用户名',validators=[DataRequired(),Length(1,64),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                   u'用户名必须由字母数、字数、下划线或 . 组成')])

    password=PasswordField(label=u'密码',validators=[DataRequired(),
                                             EqualTo('password2',message=u'密码必须一致')])

    password2=PasswordField(label=u'确认密码',validators=[DataRequired()])

    submit=SubmitField(label=u'马上注册')

#评论表单
class PostForm(Form):
    title = StringField(label=u"标题", validators=[DataRequired()])
    body = PageDownField(label=u"正文", validators=[DataRequired()])
    submit = SubmitField(u"发表")


class CommentForm(Form):
    body = PageDownField(label=u'评论', validators=[DataRequired()])
    submit = SubmitField(label=u'发表')

