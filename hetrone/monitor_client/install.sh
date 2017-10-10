#!/bin/bash



while [[ true ]]; do
    #statements
    which python3
    if [ $? -eq 0 ];then
        ps -ef|grep python3 |grep -v grep | awk '{print $2}' |xargs kill
        echo $?
        which pip3
        if [ $? -eq 0 ];then
            pip3 install psutil
            pip3 install redis
            python3 /tmp/monitor_client/bin/start.py
            exit 0
        else
            yum install gcc gcc-c++ python34-devel -y
            python3 get-pip.py
            return 0
        fi
    else
        SYSTEM="uname -a 2>&1|awk '{print $3}' |awk -F '.' '{print $1}'"
        if [[ '$SYSTEM'=7 ]];then
            echo '系统为7'
            echo 'yum安装Python34'
            yum install -y epel-release && yum install -y python34
            return 0
        elif [[ '$SYSTEM'=6 ]]; then
            echo '系统为6'
            echo 'yum安装Python34'
            yum install -y python34
            return 0
        fi
    fi
done