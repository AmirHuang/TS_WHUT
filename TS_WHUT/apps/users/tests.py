from django.test import TestCase

# Create your tests here.

# for index, i in enumerate(['a', 'b', 'c', 'd']):
#     print(index, i)


# for i in ['a', 'b', 'c', 'd'][::-1]:
#     print(i)

# 下面的QQ邮件发送也是对的

# 配置发送QQ邮件
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 后面这个必须为False否则也是发不成功的
# EMIAL_USE_TLS = True
EMIAL_USE_TLS = False
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 25
EMAIL_HOST_USER = '429771087@qq.com'  # 帐号
EMAIL_HOST_PASSWORD = 'somtbcnnpenpbjef'  # QQ邮箱的独立授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# 这里的是前缀，也就是头
# EMAIL_SUBJECT_PREFIX = u'[Sercheif]'