# _*_ coding: utf-8 _*_
# @time     : 2018/11/26
# @Author   : Amir
# @Site     : 
# @File     : email_test.py
# @Software : PyCharm


from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# 邮箱smtp服务器
smtp_server = 'smtp.exmail.qq.com'
# 发件人的邮箱账号
sender = '429771087@qq.com'
# pwd为邮箱的授权码,有的服务商和普通密码一样，有的需要额外设置
pwd = 'somtbcnnpenpbjef'
# 收件人邮箱
receivers = [
    '247769119@qq.com',
]

# 邮件的正文内容
mail_content = '过两天我把这个邮件自动回复装到网站上去,然后就可以愉快的装13了.'
# 邮件标题
mail_title = '来自lujianxin.cn的回复'

# ssl登录,有的不需要ssl直接实例化SMTP
smtp = SMTP_SSL(smtp_server)
smtp.set_debuglevel(0)
smtp.ehlo(smtp_server)
smtp.login(sender, pwd)

msg = MIMEText(mail_content, "plain", 'utf-8')  # 邮件内容
msg["Subject"] = Header(mail_title, 'utf-8')  # 邮件主题

msg["From"] = 'Amir'  # 发邮件的前缀或昵称
msg["To"] = 'dear'  # 收件人姓名或昵称

smtp.sendmail(sender, receivers, msg.as_string())
smtp.quit()

if __name__ == '__main__':
    pass

