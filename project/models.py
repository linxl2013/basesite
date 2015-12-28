# coding:utf-8
from django.db import models


# 项目模型
class Project(models.Model):
    projectname = models.CharField(max_length=255)
    projectcode = models.CharField(max_length=255)
    starttime = models.DateField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    createuserid = models.IntegerField()


# 项目模块模型
class Projectmodule(models.Model):
    name = models.CharField(max_length=50)
    parentid = models.IntegerField()
    desc = models.TextField(blank=True, null=True)
    createuserid = models.IntegerField()


# 任务模型
class Task(models.Model):
    title = models.CharField(max_length=255)  # 名称
    desc = models.TextField(blank=True, null=True)  # 描述
    projectid = models.IntegerField()  # 项目id
    createuserid = models.IntegerField()  # 提出人
    attnid = models.IntegerField()  # 经办人
    starttime = models.DateTimeField(blank=True, null=True)  # 开始时间
    estimatetime = models.DateTimeField(blank=True, null=True)  # 预计完成时间
    endtime = models.DateTimeField(blank=True, null=True)  # 完成时间
    version = models.CharField(max_length=20)  # 项目版本
    status = models.CharField(max_length=10)
    PRIORITY = (
        ('urgent', 'urgent'),
        ('priority', 'priority'),
        ('general', 'general'),
        ('behind', 'behind'),
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY, default='general')  # 优先级S
