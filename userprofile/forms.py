from django import forms


# 登录表单，继承了 forms.Form 类, 需要手动配置每个字段，它适用于不与数据库进行直接交互的功能
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
