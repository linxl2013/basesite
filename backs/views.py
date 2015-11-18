# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from backs.models import *
from backs.LoginBackend import *
from backs.GetForm import *
from functools import wraps
from datetime import *
import json
# import time


@authenticated
def index(request):
    return render(request, 'base.html')


@authenticated
def menu(request):
    return render(request, 'menu.html')


@authenticated
def home(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    return render(request, 'home.html', {'TutorialList': TutorialList, 'info_dict': info_dict, 'text': request.user})


class login(View):

    def get(self, request):
        if request.is_ajax():
            return HttpResponse("<srcipt>top.location.href='/admin/login';</srcipt>")
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('user-name', '')
        password = request.POST.get('user-password', '')
        account = Account()
        (state, data) = account.authenticate(username, password)
        print state
        if state == 0:
            request.session['user_id'] = data['id']
            request.session['user'] = data
            return HttpResponseRedirect('/admin')
        else:
            return render(request, 'login.html', {'state': state, 'info': data, 'name': username})


def logout(request):
    try:
        del request.session['user_id']
        del request.session['user']
        return HttpResponseRedirect('/admin/login')
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


@authenticated
def user(request):
    return render(request, 'user.html')


@authenticated
def user_list(request):
    rows = [
        {
            'id': 1,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 2,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }, {
            'id': 3,
            'account': '帐号',
            'realname': '真实姓名',
            'realname': '昵称',
            'email': '电子邮件',
            'phone': '手机',
            'gender': '性别',
            'visits': '访问次数',
            'joined': '加入时间',
            'locked': '锁定时间',
        }
    ]

    data = {'total': len(rows), 'rows': rows}
    # data = {'total': 0, 'rows': []}

    return HttpResponse(json.dumps(data))


class user_add(View):

    @authenticated
    def get(self, request):
        return render(request, 'user_add.html', {'title': '新增用户'})

    @authenticated
    def post(self, request):
        form = GetForm(request)
        form.post("role", required=True)
        form.post("account", text="用户名", required=True)
        form.post("password", text="密码", required=True)
        form.post("realname")
        form.post("nickname")
        form.post("email", text="电子邮件", required=True, validType="email")
        form.post("phone", text="手机号码", required=True, validType="mobile")
        form.post("gender")
        (ret, data) = form.check()

        json_data = json.dumps({'error': ret, 'info': data})
        return HttpResponse(json_data, content_type='application/json')

        # error = []
        # role = request.POST.get('role', None)
        # account = request.POST.get('name', None)
        # password = request.POST.get('password', None)
        # realname = request.POST.get('realname', None)
        # nickname = request.POST.get('nickname', None)
        # email = request.POST.get('email', None)
        # phone = request.POST.get('phone', None)
        # gender = request.POST.get('gender', None)
        # joined = datetime.now()
        # locked = datetime.now()
        # visits = 0

        # if role == '':
        #     erro.append({'name': 'role', 'value': '请选择用户组'})
        # if account == '':
        #     error.append({'name': 'name', 'value': '请输入用户名'})
        # if password == '':
        #     error.append({'name': 'password', 'value': '请输入密码'})
        # if password == '':
        #     error.append({'name': 'email', 'value': '请输入电子邮件'})
        # if len(error) > 0:
        #     json_data = json.dumps({'error': 1, 'info': error})
        #     return HttpResponse(json_data, content_type='application/json')

        # password = make_password(password)

        # a = Account(role=role, account=account, password=password, realname=realname, nickname=nickname,
        #             email=email, phone=phone, gender=gender, joined=joined, visits=0, locked=locked)
        # a.save()
        # userid = a.id
        # json_data = json.dumps({'error': 0, 'id': userid})
        # return HttpResponse(json_data, content_type='application/json')


@authenticated
def user_edit(request):
    return HttpResponse("")


@authenticated
def user_del(request):
    return HttpResponse("")


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))
