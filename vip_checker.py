import os
import subprocess
import time
import logging
import logging.handlers

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)

#Configuration items
vip = '' #secondary IP address to use a VIP e.g 192.168.1.3
mask = '' #subnet mask e.g. 24
device = '' #network interface as device name e.g. eth0
redis_auth_password = '' #redis authentication password to check info replication e.g. Password1
time_to_sleep = 60 #seconds between checks

#os shell check to see if output of ip addr contains the vip address
def do_i_have_vip():
    try:
        output = str(subprocess.check_output(('ip addr'), shell=True))
        if output.__contains__(vip):
            return True
        else:
            return False
    except Exception as e:
        logger.debug('redis_vip_checker: ',e)
        print('redis_vip_checker: ',e)

#os shell check to see if output of redis info replication contains the role:master string
def am_i_redis_master():
    try:
        command_string = f'redis-cli -a {redis_auth_password} info replication'
        output = str(subprocess.check_output((command_string), shell=True))
        if output.__contains__('role:master'):
            return True
        else:
            return False
    except Exception as e:
        print('Redis is not responding')
        print(e)

#os shell to add vip as secondary ip
def add_vip_if_master():
    logger.debug('redis_vip_checker: Attempting to add VIP')
    print('redis_vip_checker: Attempting to add VIP')
    try:
        argument = f'sudo ip addr add {vip}/{mask} dev {device}'
        subprocess.call((argument), shell=True)
        logger.debug('redis_vip_checker: Added Redis VIP')
        print('redis_vip_checker: Added Redis VIP')
    except Exception as e:
        print(e)

#os shell to delete vip as secondary ip
def delete_vip_if_not_master():
    print('redis_vip_checker: Attempting to delete VIP')
    logger.debug('redis_vip_checker: Attempting to delete VIP')
    try:
        argument = f'sudo ip addr delete {vip}/{mask} dev {device}'
        print(argument)
        subprocess.call((argument), shell=True)
        logger.debug('redis_vip_checker: Deleted Redis VIP')
        print('redis_vip_checker: Deleted Redis VIP')
    except Exception as e:
        print(e)

#start loop for logic checks
while True:
    logger.debug('redis_vip_checker: Checking for Master and VIP...')
    if am_i_redis_master() and do_i_have_vip():
        logger.debug('redis_vip_checker: I am master and I have VIP')
        print('I am master and I have VIP')
    elif am_i_redis_master() and not do_i_have_vip():
        logger.debug('redis_vip_checker: I am master but I do not have VIP')
        print('I am master but I do not have VIP')
        add_vip_if_master()
    elif am_i_redis_master() is False and do_i_have_vip() is True:
        logger.debug('redis_vip_checker: I am not master but I do have VIP')
        print('I am not master but I do have VIP')
        delete_vip_if_not_master()
    elif am_i_redis_master() is False and do_i_have_vip() is False:
        logger.debug('redis_vip_checker: I am not master and I do not have VIP')
        print('I am not master and I do not have VIP')
    else:
        logger.debug('redis_vip_checker: error')
        print('error')
    #pause between loop runs
    logger.debug('redis_vip_checker: sleeping...')
    print('sleeping...')
    time.sleep(time_to_sleep)
