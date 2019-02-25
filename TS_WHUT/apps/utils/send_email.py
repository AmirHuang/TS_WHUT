# _*_ coding: utf-8 _*_
# @time     : 2018/11/26
# @Author   : Amir
# @Site     : 
# @File     : send_email.py
# @Software : PyCharm


import random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from TS_WHUT.settings import DEFAULT_FROM_EMAIL


def generate_code(randomlength=8):
    seeds = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random_str = []
    for i in range(randomlength):
        random_str.append(random.choice(seeds))
    return ''.join(random_str)


def send_xx_email(email, send_type='register'):
    """
    email: 目标邮箱
    send_type: 相应类型，默认为注册(register)类型
    """
    email_record = EmailVerifyRecord()
    code = generate_code(16)

    # 将每一次发的邮件内容保存在数据库中
    email_record.code = code
    email_record.send_email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = 'Amir'
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/users/active/?active_code={0}".format(code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "图说理工网网密码重置链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
        if send_status:
            pass

    # elif send_type == "update_email":
    #     email_title = "图说理工网邮箱修改验证码"
    #     email_body = "你的邮箱验证码为：{0}".format(code)
    #
    #     send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    #     if send_status:
    #         pass

# send_xx_email('247769119@qq.com')