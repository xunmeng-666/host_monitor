#!/usr/bin/env python

# REDIS 服务器配置
REDIS_IP = '192.168.31.152'
REDIS_PORT = 6379
REDIS_PASS = ''
REDIS_TIMEOUT = 10  #REDIS 过期时间

#连接信息配置

CONN_TIMEOUT = 300       #连接超时时间
RE_CONN_TIME = 5    #重新连接时间
DATA_TO_REDIS_TIME = 3   #客户端数据发送至redis时间


