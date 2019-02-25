# _*_ coding: utf-8 _*_
# @time     : 2018/11/27
# @Author   : Amir
# @Site     : 
# @File     : qq_email_test.py
# @Software : PyCharm


from email.mime.text import MIMEText
from smtplib import SMTP_SSL


SERVER_HOST = 'smtp.qq.com'
SERVER_PORT = 465 # 587也可以

# 你在自己做的时候把这两个换成你自己的就行了
SERVER_EMAIL = '429771087@qq.com' # 你要发送邮件的邮箱
SERVER_PWD = 'somtbcnnpenpbjef' # 需要去qq邮箱生成授权码


SUBJECT = '测试邮件'
RECEIVERS = [
    'email@lujianxin.cn',
    'cn.lujianxin@gmail.com',
    '247769119@qq.com',
]

# 创建smtp服务
smtp_server = SMTP_SSL(
    host=SERVER_HOST,
    port=SERVER_PORT,
)

smtp_server.login(SERVER_EMAIL, SERVER_PWD)

# 创建msg对象
msg = '我爱中华人民共和国'
mime_text = MIMEText(msg, 'plain', 'utf-8')
mime_text['From'] = SERVER_EMAIL
mime_text['Subject'] = SUBJECT

smtp_server.sendmail(SERVER_EMAIL, RECEIVERS, mime_text.as_string())
smtp_server.quit()
