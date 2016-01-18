# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from status.models import *
from backs.filter import *
from mysite2.utils import *


class status(View):

    # 状态设置
    @authenticated
    def get(self, request, statustype):
        return render(request, 'status.html', {'page_id': 'status', 'statustype': statustype})

    # 新增编辑
    def post(self, request, statustype):
        json = request.POST.get("data")
        data = Json.decode(json)

        try:
            if len(data) > 0:
                for v in data:
                    if v['id'] != '':
                        s = Status.objects.get(id=v['id'])
                    else:
                        s = Status()
                    s.statustype = statustype
                    s.name = v['name']
                    s.code = v['code']
                    s.save()

            return HttpResponse('1')

        except Exception, e:
            return HttpResponse('0')


# 状态列表
@authenticated
def list(request, statustype):
    total = rows = Status.objects.filter(statustype=statustype).count()
    fetchall = Status.objects.filter(statustype=statustype).all()

    rows = []
    for obj in fetchall:
        dic = obj.get_dic()
        rows.append(dic)

    data = {'total': total, 'rows': rows}
    return HttpResponse(Json.encode(data), content_type='application/json')


# 删除状态
def delete(request):
    statustype = request.POST.get("type")
    id = request.POST.get("id")
    try:
        Status.objects.filter(id=id, statustype=statustype).delete()

        return HttpResponse('1')

    except Exception, e:
        return HttpResponse('0')
