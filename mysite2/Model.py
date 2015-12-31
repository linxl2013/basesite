# coding:utf-8
from django.db import models
from datetime import date, datetime


class Model(models.Model):

    # 获取数据字典
    def get_dic(self):
        dic = self.__dict__
        if dic.has_key('_state'):
            del dic['_state']
        for (k, v) in dic.items():
            if isinstance(v, datetime):
                dic[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, date):
                dic[k] = v.strftime('%Y-%m-%d')
        return dic

    class Meta:
        abstract = True
