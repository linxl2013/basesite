# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.db import connection, transaction
from backs.models import *
from backs.filter import *
from mysite2.GetForm import *
from mysite2.utils import *
import copy


# 首页
@authenticated
def index(request):
    menus = Menu.objects.all()

    def gettree(nodes):
        def getchildren(parentid):
            child_nodes = []
            for obj in nodes:
                if obj.parentid == parentid:
                    obj.children = getchildren(obj.id)
                    child_nodes.append(obj)
            sorted_nodes = sorted(child_nodes, key=lambda elem: "%s" %
                                  elem.menuorder, reverse=False)
            return sorted_nodes
        return getchildren(0)

    menu_tree = gettree(menus)

    def treenode(node):
        html = ""
        if node.children:
            html = html + "<ul>"
            for child in node.children:
                options = child.menuurl and " data-options=\"attributes:{'url':'" + \
                    child.menuurl + "'}\"" or ""
                html = html + "<li" + options + ">"
                html = html + "<span>" + child.menuname + "</span>"
                html = html + treenode(child)
                html = html + "</li>"
            html = html + "</ul>"
        return html

    html = ""
    for obj in menu_tree:
        html = html + "<li>"
        html = html + "<span>" + obj.menuname + "</span>"
        html = html + treenode(obj)
        html = html + "</li>"

    return render(request, 'base.html', {"menu_tree": html})


@authenticated
def home(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    return render(request, 'home.html', {'TutorialList': TutorialList, 'info_dict': info_dict, 'text': request.user, 'title': 'sdsd'})


class login(View):

    # 登录页面
    def get(self, request):
        if request.is_ajax():
            return HttpResponse("<script type='text/javascript'>top.location.href='/admin/login';</script>")
        else:
            return render(request, 'login.html')

    # 提交登录
    def post(self, request):
        username = request.POST.get('user-name', '')
        password = request.POST.get('user-password', '')
        account = Account()
        (state, data) = account.authenticate(request, username, password)
        print state
        if state == 0:
            request.session['user_id'] = data['id']
            request.session['user'] = data
            return HttpResponseRedirect('/admin')
        else:
            return render(request, 'login.html', {'state': state, 'info': data, 'name': username})


# 登出
def logout(request):
    try:
        del request.session['user_id']
        del request.session['user']
        return HttpResponseRedirect('/admin/login')
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


# 用户页面
@authenticated
def user(request):
    return render(request, 'user.html', {'page_id': 'user_list'})


# 用户列表数据
@authenticated
def user_list(request):
    page = request.POST.get('page')
    count = request.POST.get('rows')

    total, rows = Account.objects.get_list(page, count, filter={'deleted': 0})

    data = {'total': total, 'rows': rows}
    return HttpResponse(Json.encode(data), content_type='application/json')


class user_add(View):

    # 添加用户页面
    @authenticated
    def get(self, request):
        return render(request, 'user_add.html', {'title': '新增用户', 'url': '/admin/user/add'})

    # 添加用户操作
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
        form.post("islock", default=0)
        (ret, data) = form.check()

        if ret == 1:
            json_data = Json.encode({'error': ret, 'info': data})
            return HttpResponse(json_data, content_type='application/json')

        if data["rpwd"] != data["password"]:
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': 'rpwd', 'msg': '重复密码不一致'}]})
            return HttpResponse(json_data, content_type='application/json')

        if not Account.objects.account_unique(data["account"]):
            json_data = Json.encode({'error': ret, 'info': '用户名已被使用'})
            return HttpResponse(json_data, content_type='application/json')

        joined = datetime.now()
        visits = 0

        password = make_password(data["password"])

        try:
            a = Account(role=data["role"], account=data["account"], password=password, realname=data["realname"], nickname=data["nickname"], email=data[
                        "email"], phone=data["phone"], gender=data["gender"], visits=0, joined=joined, islock=data["islock"])
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

    # 编辑用户页面
    @authenticated
    def get(self, request, id):
        a = Account.objects.get(id=id)
        dic = a.get_dic()
        del dic["password"]
        del dic["deleted"]

        json = copy.copy(dic)
        del json["islock"]

        return render(request, 'user_add.html', {'title': '编辑用户', 'url': '/admin/user/edit', 'data': dic})

    # 编辑用户操作
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
        form.post("islock", default=0)
        (ret, data) = form.check()

        if ret == 1:
            json_data = Json.encode({'error': ret, 'info': data})
            return HttpResponse(json_data, content_type='application/json')

        if data["rpwd"] != data["password"]:
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': 'rpwd', 'msg': '重复密码不一致'}]})
            return HttpResponse(json_data, content_type='application/json')

        if not Account.objects.account_unique(data["account"], id):
            json_data = Json.encode({'error': 1, 'info': [{'name': 'account', 'msg': '用户名已被使用'}]})
            return HttpResponse(json_data, content_type='application/json')

        try:
            a = Account.objects.get(id=id)
            a.role = data["role"]
            a.account = data["account"]
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


# 删除用户
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


# 用户组页面
@authenticated
def group(request):
    return render(request, 'group.html', {'page_id': 'group_list'})


# 用户组列表数据
@authenticated
def group_list(request):
    total = Group.objects.count()

    page = request.POST.get('page')
    count = request.POST.get('rows')

    sql = "select `id`, `name`, `role`, `desc`, `parentid`, `orderby` from backs_group limit %s, %s" % (
        (int(page) - 1) * int(count), count)
    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()

    tree = []

    def gettree(nodes):
        def getchildren(parentid):
            child_nodes = []
            for obj in nodes:
                if obj[4] == parentid:
                    child_nodes.append(obj)
                    child_nodes.extend(getchildren(obj[0]))
            sorted_nodes = sorted(child_nodes, key=lambda elem: "%s" %
                                  elem[5], reverse=False)
            return sorted_nodes
        return getchildren(0)

    tree.extend(gettree(fetchall))

    # parentId
    rows = []
    for obj in tree:
        dic = {}
        dic["id"] = obj[0]
        dic["name"] = obj[1]
        dic["role"] = obj[2]
        dic["desc"] = obj[3]
        dic["orderby"] = obj[5]
        if obj[4] != 0:
            dic["_parentId"] = obj[4]
        rows.append(dic)

    data = {'total': total, 'rows': rows}
    return HttpResponse(Json.encode(data), content_type='application/json')


class group_add(View):

    # 添加用户组页面
    @authenticated
    def get(self, request):
        return render(request, 'group_add.html', {'title': '新增用户组', 'url': '/admin/group/add'})

    # 添加用户组操作
    @authenticated
    def post(self, request):
        form = GetForm(request)
        form.post("name", text="用户组名", required=True)
        form.post("role")
        form.post("desc")
        form.post("parentid", required=True)
        (ret, data) = form.check()

        if ret == 1:
            json_data = Json.encode({'error': ret, 'info': data})
            return HttpResponse(json_data, content_type='application/json')

        try:
            g = Group(role=data["role"], name=data[
                      "name"], desc=data["desc"], acl="", parentid=data["parentid"])
            g.save()
            groupid = g.id
            json_data = Json.encode({'error': 0, 'id': groupid})
            return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


class group_edit(View):

    # 编辑用户组页面
    @authenticated
    def get(self, request, id):
        g = Group.objects.get(id=id)
        dic = g.get_dic()
        del dic["acl"]

        return render(request, 'group_add.html', {'title': '编辑用户组', 'url': '/admin/group/edit', 'data': dic})

    # 编辑用户组操作
    @authenticated
    def post(self, request):
        id = request.POST.get("id")

        form = GetForm(request)
        form.post("name", text="用户组名", required=True)
        form.post("role")
        form.post("desc")
        form.post("parentid", required=True)
        (ret, data) = form.check()

        if ret == 1:
            json_data = Json.encode({'error': ret, 'info': data})
            return HttpResponse(json_data, content_type='application/json')

        try:
            g = Group.objects.get(id=id)
            g.name = data["name"]
            g.role = data["role"]
            g.desc = data["desc"]
            g.parentid = data["parentid"]
            g.save()
            json_data = Json.encode({'error': 0, 'id': id})
            return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


# 删除用户组
@authenticated
def group_del(request):
    id = request.POST.get("id")
    id = id.split(",")

    try:
        Group.objects.filter(id__in=id).delete()
        json_data = Json.encode({'error': 0, 'id': id})
        return HttpResponse(json_data, content_type='application/json')
    except Exception, e:
        print e
        json_data = Json.encode(
            {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
        return HttpResponse(json_data, content_type='application/json')


# 用户组排序
@authenticated
def group_order(request):
    id = request.GET.get("id")
    orderby = request.GET.get("orderby")

    g = Group.objects.get(id=id)
    g.orderby = orderby
    g.save()

    return HttpResponse("ok")


class group_priv(View):

    # 用户组权限页面
    @authenticated
    def get(self, request, id):
        g = Group.objects.get(id=id)
        dic = g.get_dic()
        acl = dic['acl'].split(',')

        buttons = Button.objects.all()

        def gettree(nodes):
            def getchildren(parentid):
                child_nodes = []
                for obj in nodes:
                    if obj.parentid == parentid:
                        obj.children = getchildren(obj.id)
                        child_nodes.append(obj)
                sorted_nodes = sorted(child_nodes, key=lambda elem: "%s" %
                                      elem.orderby, reverse=False)
                return sorted_nodes
            return getchildren(0)

        tree = gettree(buttons)

        def treenode(node):
            html = ""
            if node.children:
                html = html + "<ul>"
                for child in node.children:
                    checked = str(child.id) in acl and ',checked:true' or ''
                    options = " data-options=\"attributes:{'id':'%s','no':'%s'}%s\"" % (
                        child.id, child.buttonno, checked)
                    html = html + "<li" + options + ">"
                    html = html + "<span>" + child.buttontitle + "</span>"
                    html = html + treenode(child)
                    html = html + "</li>"
                html = html + "</ul>"
            return html

        html = ""
        for obj in tree:
            checked = str(obj.id) in acl and ',checked:true' or ''
            options = " data-options=\"attributes:{'id':'%s','no':'%s'}%s\"" % (
                obj.id, obj.buttonno, checked)
            html = html + "<li" + options + ">"
            html = html + "<span>" + obj.buttontitle + "</span>"
            html = html + treenode(obj)
            html = html + "</li>"

        return render(request, 'priv.html', {"tree": html, 'title': '用户组权限', 'id': id})

    # 用户组权限修改
    @authenticated
    def post(self, request, id):
        acl = request.POST.get('acl')
        try:
            g = Group.objects.get(id=id)
            g.acl = acl
            g.save()
            json_data = Json.encode({'error': 0, 'id': id})
            return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


# 用户组列表数据
@authenticated
def group_tree(request):
    top = request.GET.get('top', None)
    g = Group.objects.all()

    def gettree(nodes):
        def getchildren(parentid):
            child_nodes = []
            for obj in nodes:
                if obj.parentid == parentid:
                    obj.children = getchildren(obj.id)
                    child_nodes.append(obj)
            sorted_nodes = sorted(child_nodes, key=lambda elem: "%s" %
                                  elem.orderby, reverse=False)
            return sorted_nodes
        return getchildren(0)

    tree_obj = gettree(g)

    def treenode(nodes):
        def getchildren(nodes):
            child_nodes = []
            for obj in nodes:
                dic = {}
                dic["id"] = obj.id
                dic["text"] = obj.name
                dic["children"] = getchildren(obj.children)
                child_nodes.append(dic)
            return child_nodes
        return getchildren(nodes)

    tree = treenode(tree_obj)

    if top != None:
        json = [{"id": 0, "text": "顶级用户组", "children": tree}]
    else:
        json = tree

    json_data = Json.encode(json)
    return HttpResponse(json_data, content_type='application/json')
