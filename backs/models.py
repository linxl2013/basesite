# coding:utf-8
from django.db import models
from django.db import connection, transaction
from django.db.models import Q
from mysite2.Model import Model
from datetime import date, datetime
from django.contrib.auth.hashers import make_password, check_password
import re


class AccountManager(models.Manager):

    # 用户名是否唯一
    def account_unique(self, name, id=0):
        if id == 0:
            user = Account.objects.get(account=name)
        else:
            user = Account.objects.filter(~Q(id=id), Q(account=name))
        
        if user:
            return False
        else:
            return True


    # 获取用户列表
    def get_list(self, page=0, count=100, filter={}, where='where 1'):
        # a = Account.objects
        # where = 'where 1'
        for (k, v) in filter.items():
            # w = "a.filter(%s='%s')" % (k, v)
            # eval(w)
            where = where + " and %s='%s'" % (k, v)
        # total = a.count()

        sql = 'select count(id) from backs_account a %s' % where
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        total = row[0]

        sql = '''
        select a.id, a.account, a.realname, a.nickname, a.email, a.phone, a.gender, a.visits, a.joined, a.locked, a.islock, g.name as gname 
        from backs_account a 
        left join backs_group g on a.role=g.id 
        %s 
        order by id asc
        limit %s, %s
        ''' % (where, (int(page) - 1) * int(count), count)

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
            dic["group"] = obj[11]
            rows.append(dic)

        return total, rows


# 用户模型
class Account(Model):
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

    objects = AccountManager()

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


# 用户组模型
class Group(Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    acl = models.TextField()
    parentid = models.IntegerField()
    orderby = models.IntegerField(blank=True, default='0')


class Grouppriv(Model):
    groupid = models.IntegerField()
    buttonid = models.IntegerField()


# 按钮模型
class Button(Model):
    parentid = models.IntegerField()
    buttontitle = models.CharField(max_length=30)
    buttonno = models.CharField(max_length=30)
    onclick = models.CharField(max_length=30)
    group = models.CharField(max_length=30)
    module = models.CharField(max_length=30)
    method = models.CharField(max_length=30)
    orderby = models.IntegerField()


# 菜单模型
class Menu(Model):
    parentid = models.IntegerField()
    menuname = models.CharField(max_length=30)
    menuurl = models.CharField(max_length=255)
    menuorder = models.IntegerField()
