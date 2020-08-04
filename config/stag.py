# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import  * # noqa

# 预发布环境
RUN_MODE = 'STAGING'

# 正式环境的日志级别可以在这里配置
# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 预发布环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': APP_CODE,  # 数据库名
            'USER': 'jiangming',  # 数据库用户
            'PASSWORD': 'jmdjsj903291A',  # 数据库密码
            'HOST': 'pc-bp1n46641xsxo3heco.rwlb.rds.aliyuncs.com',  # 数据库主机
            'PORT': '3306',  # 数据库端口
        },
    }
)

