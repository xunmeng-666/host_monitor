#!/usr/bin/env python

import os,sys

BASE_PASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PASH)
print(BASE_PASH)

from core.client_info import conn_w_redis

if __name__ =="__main__":

    conn_data = conn_w_redis()
    print('conn_data',conn_data)