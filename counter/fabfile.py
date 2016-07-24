#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from fabric.api import run, cd, roles, execute, env, hide
from fabric.context_managers import env, settings
import traceback
import time

PV = 0
WIN = 0
CLICK = 0

env.roledefs = { 
    'bridge_server': ['work@180.76.147.42', 'work@180.76.188.212', 'work@180.76.148.249'],  
    'hig_server': ['work@180.76.183.134']
}

@roles('bridge_server')
def do_bridge_task(adspotid, rtime, os):
    global PV
    with cd('/home/work/pyrun_env/bridge/log'):
        if rtime == 'today':
            #cmd = "cat pv.st?.log pv.st10.log | grep -c \"%s\" " % (adspotid)
            cmd = "find . -name \"pv.st*.log\" | grep -v \"2016\" | xargs grep \"%s\" | grep -c \"\\\\\"os\\\\\": %s\"" % (adspotid, os)
        else:
            cmd = "cat pv.st*.log.%s | grep \"%s\" | grep -c \"\\\\\"os\\\\\": %s\"" % (rtime, adspotid, os)
        with settings(hide('running', 'stdout'), warn_only=True):
            output = run(cmd)
        if output.succeeded:
            PV += int(output)

@roles('hig_server')
def do_hig_task(adspotid, rtime, os):
    global WIN
    global CLICK
    with cd('/home/work/pyrun_env/hig/callback_server/log'):
        if rtime == "today":
            ptime = time.strftime("%Y-%m-%d", time.localtime())
            win_cmd = "cat win/win.st*.log win/win.st*.log.%s_* | grep \"%s\" | grep  \"\\\\\"os\\\\\": \\\\\"%s\\\\\"\"\
                | grep -E -o \"\\\\\"auction\\\\\": \\\\\".*\\\\\"\" | cut -d \" \" -f 2 | sort | uniq -u | wc -l" % (ptime, adspotid, os)
            click_cmd = "cat click/click.st*.log click/click.st*.log.%s_* | grep \"%s\" | grep \"\\\\\"os\\\\\": \\\\\"%s\\\\\"\"\
                | grep -E -o \"\\\\\"auction\\\\\": \\\\\".*\\\\\"\" | cut -d \" \" -f 2 | sort | uniq -u | wc -l" % (ptime, adspotid, os)
        else:
            win_cmd = "cat win/win.st*.log.%s* | grep \"%s\" | grep  \"\\\\\"os\\\\\": \\\\\"%s\\\\\"\"\
                | grep -E -o \"\\\\\"auction\\\\\": \\\\\".*\\\\\"\" | cut -d \" \" -f 2 | sort | uniq -u | wc -l" % (rtime, adspotid, os)
            click_cmd = "cat click/click.st*.log.%s* | grep \"%s\" | grep \"\\\\\"os\\\\\": \\\\\"%s\\\\\"\"\
                | grep -E -o \"\\\\\"auction\\\\\": \\\\\".*\\\\\"\" | cut -d \" \" -f 2 | sort | uniq -u | wc -l" % (rtime, adspotid, os)

        with settings(hide('running', 'stdout'), warn_only=True):
            output = run(win_cmd)
        if output.succeeded:
            WIN += int(output)

        with settings(hide('running', 'stdout'), warn_only=True):
            output = run(click_cmd)
        if output.succeeded:
            CLICK += int(output)

def get_rate(denominator, numerator):
    if denominator and numerator:
        return (numerator*1.0/denominator) * 100
    else:
        return 0

def print_info(adspotid, rtime, name):
    ptime = rtime
    if rtime == 'today':
        ptime = time.strftime("%Y-%m-%d", time.localtime())

    f = open('report_' + ptime + '.log', 'a')
    f.write("adspotid: %s, name: %-30s, time: %s, pv: %-10s, win: %-8s, click: %-6s, winrate: %6.2f%%, clickrate: %6.2f%%\n" % (
        adspotid, name, ptime, PV, WIN, CLICK, get_rate(PV, WIN), get_rate(PV, CLICK)))
    f.close()

def task(adspotid, rtime, name, os):
    try:
        execute(do_bridge_task, adspotid, rtime, os)
        execute(do_hig_task, adspotid, rtime, os)
        print_info(adspotid, rtime, name)
    except:
        traceback.print_exc()


    
    

