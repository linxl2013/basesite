# coding:utf-8
from django.db import models
from django.db import connection, transaction
from mysite2.Model import Model


class ProjectManager(models.Manager):

    # 获取项目数据
    def get_list(self, page=0, count=100, filter={}, where='where 1'):
        for (k, v) in filter.items():
            where = where + " and %s='%s'" % (k, v)

        sql = 'select count(id) from project_project a %s' % where
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        total = row[0]

        sql = '''
        select p.*,a.realname creater 
        from project_project p 
        left join backs_account a on p.createuserid=a.id 
        order by id asc 
        limit %s, %s
        ''' % ((int(page) - 1) * int(count), count)

        cursor = connection.cursor()
        cursor.execute(sql)
        fetchall = cursor.fetchall()

        ids = []
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
            dic["creater"] = obj[7]
            dic["responsibles"] = ''
            rows.append(dic)
            ids.append(str(obj[0]))

        sql = '''
        select p.projectid,a.account,a.realname 
        from project_projectresponsible p 
        left join backs_account a on p.responsible=a.account 
        where p.projectid in (%s)
        ''' % (",".join(ids))
        cursor = connection.cursor()
        cursor.execute(sql)
        fetchall = cursor.fetchall()

        res_name = {}
        res_account = {}
        for obj in fetchall:
            if not res_name.has_key(str(obj[0])):
                res_name[str(obj[0])] = []
                res_account[str(obj[0])] = []
            res_name[str(obj[0])].append(obj[2] != '' and obj[2] or obj[1])
            res_account[str(obj[0])].append(obj[1])

        for i in range(len(rows)):
            if res_name.has_key(str(rows[i]['id'])):
                rows[i]['responsibles'] = ", ".join(
                    res_name[str(rows[i]['id'])])

        return total, rows

# 项目模型


class Project(Model):
    projectname = models.CharField(max_length=255)
    projectcode = models.CharField(max_length=255)
    starttime = models.DateField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    createuserid = models.IntegerField()

    objects = ProjectManager()


class ProjectresponsibleManager(models.Manager):

    # 获取负责人数据
    def account_list(self, projectid):
        sql = '''
        select a.id, a.account, a.realname, a.nickname 
        from project_projectresponsible pr 
        left join backs_account a on pr.responsible=a.account 
        where pr.projectid=%s
        '''
        cursor = connection.cursor()
        cursor.execute(sql, [projectid])
        fetchall = cursor.fetchall()

        total = len(fetchall)
        rows = []
        for obj in fetchall:
            dic = {}
            dic["id"] = obj[0]
            dic["account"] = obj[1]
            dic["realname"] = obj[2]
            dic["nickname"] = obj[3]
            rows.append(dic)

        return total, rows


# 项目负责人模型
class Projectresponsible(Model):
    projectid = models.IntegerField()
    responsible = models.CharField(max_length=20)

    objects = ProjectresponsibleManager()


# 项目模块模型
class Projectmodule(Model):
    name = models.CharField(max_length=50)
    parentid = models.IntegerField()
    desc = models.TextField(blank=True, null=True)
    createuserid = models.IntegerField()


# 任务模型
class Task(Model):
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
