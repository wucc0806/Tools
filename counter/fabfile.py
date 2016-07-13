#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from fabric.api import run, cd, roles, execute
from fabric.context_managers import env, settings
import traceback

PV = 0
WIN = 0
CLICK = 0

env.roledefs = { 
    'bridge_server': ['work@180.76.147.42', 'work@180.76.188.212', 'work@180.76.148.249'],  
    'hig_server': ['work@180.76.183.134']
}

@roles('bridge_server')
def do_bridge_task(appid, time, os):
    global PV
    with cd('/home/work/pyrun_env/bridge/log'):
        if time == 'today':
            cmd = "cat pv.st?.log pv.st10.log | grep -c \"%s\"" % appid
        else:
            #cmd = "cat pv.st*.log.%s | grep -c \"%s\"" % (time, appid)
            cmd = "cat pv.st*.log.%s | grep \"%s\" | grep -c \"\\\\\"os\\\\\": %s\"" % (time, appid, os)
        output = run(cmd)
        if output.succeeded:
            PV += int(output)

@roles('hig_server')
def do_hig_task(appid, time, supplier, os):
    global WIN
    global CLICK
    with cd('/home/work/pyrun_env/hig/callback_server/log'):
        cmd = "cat win/win.st*.log.%s* | grep \"%s\" | grep \"%s\" | grep  \"\\\\\"os\\\\\": \\\\\"%s\\\\\"\"\
            | cut -d \" \" -f 40 | sort | uniq -u | wc -l" % (time, appid, supplier, os)
        output = run(cmd)
        if output.succeeded:
            WIN += int(output)
        cmd = "cat click/click.st*.log.%s* | grep \"%s\" | grep \"%s\" | grep \"\\\\\"os\\\\\": \\\\\"%s\\\\\"\"\
            | cut -d \" \" -f 40 | sort | uniq -u | wc -l" % (time, appid, supplier, os)
        output = run(cmd)
        if output.succeeded:
            CLICK += int(output)

def print_info(appid, time, supplier):
    print ("appid: %s, time: %s, pv: %s, supplier: %s, win: %s, click: %s" % (
        appid, time, PV, supplier, WIN, CLICK))

def task(appid, time, supplier, os):
    try:
        execute(do_bridge_task, appid, time, os)
        execute(do_hig_task, appid, time, supplier, os)
        print_info(appid, time, supplier)
    except:
        traceback.print_exc()


    
    

