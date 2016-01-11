# coding:utf-8
from django.db import models
from django.db import connection, transaction
from mysite2.Model import Model


class Status(Model):
    TYPE = (
        ('task', 'task'),
        ('deploy', 'deploy'),
    )
    statustype = models.CharField(max_length=50, choices=TYPE, default='task')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)


class Statusproject(Model):
    projectid = models.IntegerField(blank=True, default=0)
    statusid = models.CharField(max_length=50)
    attnid = models.TextField(blank=True, null=True)


class Statusmodule(Model):
    moduleid = models.IntegerField(blank=True, default=0)
    statusid = models.CharField(max_length=50)
    attnid = models.TextField(blank=True, null=True)


class Statustask(Model):
    taskid = models.IntegerField(blank=True, default=0)
    statusid = models.CharField(max_length=50)
    attnid = models.TextField(blank=True, null=True)
