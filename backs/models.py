# coding:utf-8
from django.db import models
from datetime import date, datetime
from django.contrib.auth.hashers import make_password, check_password
import re


# 用户模型
class Account(models.Model):
    role = models.CharField(max_length=10)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=64)
    realname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=60)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=20)
    GENDER_LIST = (
        ('f', 'female'),
        ('m', 'male'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_LIST)
    visits = models.IntegerField()
    lastlogin = models.DateTimeField(blank=True, null=True)
    lastip = models.CharField(max_length=64)
    joined = models.DateTimeField()
    locked = models.DateTimeField(blank=True, null=True)
    IS_LOCK = (
        ('0', 'false'),
        ('1', 'true'),
    )
    islock = models.CharField(max_length=1, choices=IS_LOCK, default='0')
    IS_DELETE = (
        ('0', 'false'),
        ('1', 'true'),
    )
    deleted = models.CharField(max_length=1, choices=IS_DELETE, default='0')

    # 登录验证
    def authenticate(self, request, username=None, password=None):
        if username:
            try:
                # email
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", username) != None:
                    user = Account.objects.get(email=username)
                # mobile
                elif len(username) == 11 and re.match("^(1[3458]\d{9})$", username) != None:
                    user = Account.objects.get(phone=username)
                # username
                else:
                    user = Account.objects.get(account=username)

                if check_password(password, user.password) == True:
                    user.visits = user.visits + 1
                    user.lastlogin = datetime.now()
                    user.lastip = request.META.get("REMOTE_ADDR", None)
                    user.save()
                    return (0, user.get_dic())
                else:
                    return (2, '密码错误')
            except Account.DoesNotExist:
                return (1, '用户名错误')
        else:
            return (3, None)

    def is_authenticated(self):
        return False

    # 设置密码
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    # 检查密码
    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        # def setter(raw_password):
        # self.set_password(raw_password)
        # self.save(update_fields=["password"])
        return check_password(raw_password, self.password)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    # 获取数据
    def get_dic(self):
        dic = self.__dict__
        if dic.has_key('_state'):
            del dic['_state']
        dic['lastlogin'] = isinstance(dic['lastlogin'], datetime) and dic[
            'lastlogin'].strftime('%Y-%m-%d %H:%M:%S') or dic['lastlogin']
        dic['joined'] = isinstance(dic['joined'], datetime) and dic[
            'joined'].strftime('%Y-%m-%d %H:%M:%S') or dic['joined']
        dic['locked'] = isinstance(dic['locked'], datetime) and dic[
            'locked'].strftime('%Y-%m-%d %H:%M:%S') or dic['locked']
        return dic


# 用户组模型
class Group(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    acl = models.TextField()
    parentid = models.IntegerField()
    orderby = models.IntegerField()

    def get_dic(self):
        dic = self.__dict__
        if dic.has_key('_state'):
            del dic['_state']
        return dic


class Grouppriv(models.Model):
    groupid = models.IntegerField()
    buttonid = models.IntegerField()


# 按钮模型
class Button(models.Model):
    parentid = models.IntegerField()
    buttontitle = models.CharField(max_length=30)
    buttonno = models.CharField(max_length=30)
    onclick = models.CharField(max_length=30)
    group = models.CharField(max_length=30)
    module = models.CharField(max_length=30)
    method = models.CharField(max_length=30)
    orderby = models.IntegerField()


# 菜单模型
class Menu(models.Model):
    parentid = models.IntegerField()
    menuname = models.CharField(max_length=30)
    menuurl = models.CharField(max_length=255)
    menuorder = models.IntegerField()


# 项目模型
class Project(models.Model):
    projectname = models.CharField(max_length=255)
    projectcode = models.CharField(max_length=255)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
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
