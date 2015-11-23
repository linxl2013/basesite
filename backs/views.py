# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.db import connection, transaction
from backs.models import *
from backs.LoginBackend import *
from mysite2.GetForm import *
from mysite2.utils import *
from functools import wraps


@authenticated
def index(request):
    # m = Menu.objects.all()
    # m_list = {}
    # for obj in m:
    #     m_list[obj.id] = obj

    # menu = {}
    # parent = {}
    node = {}
    # for obj in m:
    #     if not parent.has_key(obj.parentid):
    #         parent[obj.parentid] = []
    #     node = {}
    #     node["id"] = obj.id
    #     node["parentid"] = obj.parentid
    #     node["menuname"] = obj.menuname
    #     node["menuurl"] = obj.menuurl
    #     node["menuorder"] = obj.menuorder
    #     parent[obj.parentid].append(node)
    
    # print parent

    return render(request, 'base.html', {"node": node})


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
    total = Account.objects.filter(deleted=0).count()

    page = request.POST.get('page')
    count = request.POST.get('rows')

    sql = '''
    select id, account, realname, nickname, email, phone, gender, visits, joined, locked, islock
    from backs_account
    where deleted = 0
    limit %s, %s
    ''' % ((int(page) - 1) * int(count), count)

    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()

    rows = []
    for obj in fetchall:
        dic = {}
        dic["id"] = obj[0]
        dic["account"] = obj[1]
        dic["realname"] = obj[2]
        dic["nickname"] = obj[3]
        dic["email"] = obj[4]
        dic["phone"] = obj[5]
        dic["gender"] = obj[6]
        dic["visits"] = obj[7]
        dic["joined"] = obj[8]
        dic["locked"] = obj[9]
        dic["islock"] = obj[10]
        rows.append(dic)

    data = {'total': total, 'rows': rows}
    return HttpResponse(Json.encode(data), content_type='application/json')


class user_add(View):

    @authenticated
    def get(self, request):
        return render(request, 'user_add.html', {'title': '新增用户', 'url': '/admin/user/add'})

    @authenticated
    def post(self, request):
        form = GetForm(request)
        form.post("role", required=True)
        form.post("account", text="用户名", required=True)
        form.post("password", text="密码", required=True)
        form.post("rpwd", text="重复密码")
        form.post("realname")
        form.post("nickname")
        form.post("email", text="电子邮件", required=True, validType="email")
        form.post("phone", text="手机号码", required=True, validType="mobile")
        form.post("gender", required=True)
        form.post("islock", required=True)
        (ret, data) = form.check()

        if ret == 1:
            json_data = Json.encode({'error': ret, 'info': data})
            return HttpResponse(json_data, content_type='application/json')

        if data["rpwd"] != data["password"]:
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': 'rpwd', 'msg': '重复密码不一致'}]})
            return HttpResponse(json_data, content_type='application/json')

        joined = datetime.now()
        locked = datetime.now()
        visits = 0

        password = make_password(data["password"])

        try:
            a = Account(role=data["role"], account=data["account"], password=password, realname=data["realname"], nickname=data["nickname"], email=data[
                        "email"], phone=data["phone"], gender=data["gender"], visits=0, joined=joined, locked=locked, islock=data["islock"])
            a.save()
            userid = a.id
            json_data = Json.encode({'error': 0, 'id': userid})
            return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


class user_edit(View):

    @authenticated
    def get(self, request):
        id = request.GET.get("id")
        a = Account.objects.get(id=id)
        dic = {}
        dic["id"] = a.id
        dic["account"] = a.account
        dic["realname"] = a.realname
        dic["nickname"] = a.nickname
        dic["email"] = a.email
        dic["phone"] = a.phone
        dic["gender"] = a.gender
        dic["visits"] = a.visits
        dic["islock"] = a.islock
        dic["role"] = a.role
        return render(request, 'user_add.html', {'title': '编辑用户', 'url': '/admin/user/edit', 'data': dic})

    @authenticated
    def post(self, request):
        id = request.POST.get("id")

        form = GetForm(request)
        form.post("role", required=True)
        form.post("account", text="用户名", required=True)
        form.post("password", text="密码")
        form.post("rpwd", text="重复密码")
        form.post("realname")
        form.post("nickname")
        form.post("email", text="电子邮件", required=True, validType="email")
        form.post("phone", text="手机号码", required=True, validType="mobile")
        form.post("gender", required=True)
        form.post("islock", required=True)
        (ret, data) = form.check()

        if ret == 1:
            json_data = Json.encode({'error': ret, 'info': data})
            return HttpResponse(json_data, content_type='application/json')

        if data["rpwd"] != data["password"]:
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': 'rpwd', 'msg': '重复密码不一致'}]})
            return HttpResponse(json_data, content_type='application/json')

        try:
            a = Account.objects.get(id=id)
            a.role = data["role"]
            a.realname = data["realname"]
            a.nickname = data["nickname"]
            a.email = data["email"]
            a.phone = data["phone"]
            a.gender = data["gender"]
            if data["password"] != None and data["password"] != "":
                a.password = make_password(data["password"])
            a.islock = data["islock"]
            if data["islock"] == "1":
                a.locked = datetime.now()
            a.save()
            json_data = Json.encode({'error': 0, 'id': id})
            return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


@authenticated
def user_del(request):
    id = request.POST.get("id")
    id = id.split(",")

    try:
        Account.objects.filter(id__in=id).update(deleted=1)
        json_data = Json.encode({'error': 0, 'id': id})
        return HttpResponse(json_data, content_type='application/json')
    except Exception, e:
        print e
        json_data = Json.encode(
            {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
        return HttpResponse(json_data, content_type='application/json')


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))
