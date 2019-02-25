# _*_ coding: utf-8 _*_
# @time     : 2018/11/26
# @Author   : Amir
# @Site     : 
# @File     : signals.py
# @Software : PyCharm

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Org, UserProfile


@receiver(post_save, sender=Org)
def create_org(sender, instance=None, created=False, **kwargs):
    # 当认证状态改变时
    if instance.status == '2':
        user = instance.user
        user.if_cer = True
        user.org_name = instance.name
        user.save()


@receiver(post_save, sender=UserProfile)
def create_uesr(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()

