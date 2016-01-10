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

    total, rows = Project.objects.get_list(page, count)

    data = {'total': total, 'rows': rows}
    return HttpResponse(Json.encode(data), content_type='application/json')


class project_add(View):

    # 添加项目页面
    @authenticated
    def get(self, request):
        a = Account.objects.all()
        account = []
        for v in a:
            row = v.get_dic()
            row['selected'] = False
            account.append(row)

        return render(request, 'project_add.html', {'title': '新增项目', 'url': '/admin/project/add', 'account': account})

    # 添加项目操作
    @authenticated
    @transaction.atomic
    def post(self, request):
        form = GetForm(request)
        form.post("projectname", text="项目名称", required=True)
        form.post("projectcode")
        form.post("starttime")
        form.post("endtime")
        form.post("desc")
        (ret, data) = form.check()

        charger = request.POST.getlist("charger")

        try:
            with transaction.atomic():
                p = Project()
                p.projectname = data["projectname"]
                p.createuserid = request.session.get('user_id')
                if data["projectcode"]:
                    p.projectcode = data["projectcode"]
                if data["starttime"]:
                    p.starttime = data["starttime"]
                if data["endtime"]:
                    p.endtime = data["endtime"]
                if data["desc"]:
                    p.desc = data["desc"]
                p.save()
                projectid = p.id

                for v in charger:
                    p = Projectresponsible(projectid=projectid, responsible=v)
                    p.save()

                json_data = Json.encode({'error': 0, 'id': projectid})
                return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


class project_edit(View):

    # 编辑项目页面
    @authenticated
    def get(self, request, id):
        p = Project.objects.get(id=id)
        dic = p.get_dic()

        total, rows = Projectresponsible.objects.account_list(id)
        responsibles = []
        for v in rows:
            responsibles.append(v['account'])

        a = Account.objects.all()
        account = []
        for v in a:
            row = v.get_dic()
            row['selected'] = False
            if row['account'] in responsibles:
                row['selected'] = True
            account.append(row)

        return render(request, 'project_add.html', {'title': '编辑项目',
                                                    'url': '/admin/project/edit', 'data': dic, 'account': account})

    # 编辑用户操作
    # @transaction.commit_manually
    @authenticated
    @transaction.atomic
    def post(self, request):
        id = request.POST.get("id")

        form = GetForm(request)
        form.post("projectname", text="项目名称", required=True)
        form.post("projectcode")
        form.post("starttime")
        form.post("endtime")
        form.post("desc")
        (ret, data) = form.check()

        charger = request.POST.getlist("charger")

        try:
            with transaction.atomic():
                p = Project.objects.get(id=id)
                p.projectname = data["projectname"]
                if data["projectcode"]:
                    p.projectcode = data["projectcode"]
                if data["starttime"]:
                    p.starttime = data["starttime"]
                if data["endtime"]:
                    p.endtime = data["endtime"]
                if data["desc"]:
                    p.desc = data["desc"]
                p.save()

                Projectresponsible.objects.filter(projectid=id).delete()
                for v in charger:
                    p = Projectresponsible(projectid=id, responsible=v)
                    p.save()

                # transaction.commit()

                json_data = Json.encode({'error': 0, 'id': id})
                return HttpResponse(json_data, content_type='application/json')
        except Exception, e:
            print e
            # transaction.rollback()
            json_data = Json.encode(
                {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
            return HttpResponse(json_data, content_type='application/json')


# 删除用户组
@authenticated
@transaction.atomic
def project_del(request):
    id = request.POST.get("id")
    id = id.split(",")

    try:
        with transaction.atomic():
            Project.objects.filter(id__in=id).delete()
            Projectresponsible.objects.filter(projectid__in=id).delete()

            json_data = Json.encode({'error': 0, 'id': id})
            return HttpResponse(json_data, content_type='application/json')
    except Exception, e:
        print e
        json_data = Json.encode(
            {'error': 1, 'info': [{'name': '', 'msg': '数据更新错误'}]})
        return HttpResponse(json_data, content_type='application/json')
