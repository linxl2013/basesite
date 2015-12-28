# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.db import connection, transaction
from project.models import *
from backs.filter import *
from mysite2.GetForm import *
from mysite2.utils import *


# 项目页面
@authenticated
def project(request):
    return render(request, 'project.html', {'page_id': 'project_list'})


# 项目列表数据
def project_list(request):
    total = Project.objects.count()

    page = request.POST.get('page')
    count = request.POST.get('rows')

    sql = '''
    select p.* 
    from project_project p 
    order by id asc 
    limit %s, %s
    ''' % ((int(page) - 1) * int(count), count)

    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()

    rows = []
    for obj in fetchall:
        dic = {}
        dic["id"] = obj[0]
        dic["projectname"] = obj[1]
        dic["projectcode"] = obj[2]
        dic["starttime"] = obj[3]
        dic["endtime"] = obj[4]
        dic["desc"] = obj[5]
        dic["createuserid"] = obj[6]
        rows.append(dic)

    data = {'total': total, 'rows': rows}
    return HttpResponse(Json.encode(data), content_type='application/json')


class project_add(View):

    # 添加项目页面
    @authenticated
    def get(self, request):
        return render(request, 'project_add.html', {'title': '新增项目', 'url': '/admin/project/add'})

    # 添加项目操作
    @authenticated
    def post(self, request):
        form = GetForm(request)
        form.post("role", required=True)
        form.post("account", text="项目名", required=True)
        form.post("password", text="密码", required=True)
        form.post("rpwd", text="重复密码")
        form.post("realname")
        form.post("nickname")
        form.post("email", text="电子邮件", required=True, validType="email")
        form.post("phone", text="手机号码", required=True, validType="mobile")
        form.post("gender", required=True)
        form.post("islock", required=True)
        (ret, data) = form.check()
