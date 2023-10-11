'''
作者: 李展旗
Date: 2023-10-11 12:43:41
文件最后编辑者: 李展旗
LastEditTime: 2023-10-11 16:31:17
'''
from django.db import models
# from django.utils import timezone
from datetime import datetime
# Create your models here.


class info(models.Model):
    title=models.CharField(verbose_name="标题",max_length=64)
    info_text=models.TextField(verbose_name="文本",default=None)
    url=models.CharField(verbose_name="url(文本二选一填写)",max_length=256,default=None)
    # info_type=models.CharField(choices=((1,'文本'),(2,'超链接')),verbose_name="信息类型",max_length=32)
    gender_choices=((1,'文本'),(2,'超链接'))
    info_type=models.SmallIntegerField(verbose_name="信息类型",choices=gender_choices)
    def __str__(self) -> str:
        return self.title

class usr_log(models.Model):
    title_info=models.CharField(verbose_name="标题",max_length=64)
    time=models.DateTimeField(verbose_name="访问时间",default=datetime.now)
    ip=models.CharField(verbose_name="ip地址",max_length=32)
    ua=models.TextField(verbose_name="UA")

class usr_admin(models.Model):
    name=models.CharField(verbose_name="账号名",max_length=32)
    pwd=models.CharField(verbose_name="密码",max_length=64)




