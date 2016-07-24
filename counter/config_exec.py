#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import time

app_config = {
    "1": {
        "adspotid": "10000002",
        "name": "maichang_android_jdt",
        "os": "2"
    },
    "2": {
        "adspotid": "10000003",
        "name": "maichang_android_chaping",
        "os": "2"
    },
    "3": {
        "adspotid": "10000001",
        "name": "maichang_android_kaiping",
        "os": "2"
    },
    "4": {
        "adspotid": "10000010",
        "name": "jiaxiao",
        "os": "2"
    },
    "5": {
        "adspotid": "10000020",
        "name": "meirenzhuang",
        "os": "2"
    },
    "6": {
        "adspotid": "10000012",
        "name": "bingdu_ios_native",
        "os": "1"
    },
    "7": {
        "adspotid": "10000026",
        "name": "bingdu_ios_jdt",
        "os": "1"
    },
    "8": {
        "adspotid": "10000028",
        "name": "bingdu_ios_chosenfeed",
        "os": "1"
    },
    "9": {
        "adspotid": "10000011",
        "name": "bingdu_android_native",
        "os": "2"
    },
    "10": {
        "adspotid": "10000025",
        "name": "bingdu_android_jdt",
        "os": "2"
    },
    "11": {
        "adspotid": "10000027",
        "name": "bingdu_android_chosenfeed",
        "os": "2"
    },
    "12": {
        "adspotid": "10000013",
        "name": "freebook",
        "os": "2"
    },
    "13": {
        "adspotid": "10000024",
        "name": "zhongxing_lancher",
        "os": "2"
    },
    "14": {
        "adspotid": "10000021",
        "name": "cooee_adspot_1",
        "os": "2"
    },
    "15": {
        "adspotid": "10000022",
        "name": "cooee_adspot_2",
        "os": "2"
    },
    "16": {
        "adspotid": "10000030",
        "name": "cooee_uni_lancher_banner",
        "os": "2"
    }
}
def is_valid_date(time_str):
    try:
        time.strptime(time_str, "%Y-%m-%d")
        return True
    except:
        return False

def run(rtime):
    for i in range(1, len(app_config)+1):
        cmd = '/bin/bash exec.sh {adspotid} {rtime} {name} {os}'.format(
            adspotid = app_config[str(i)]['adspotid'], 
            rtime = rtime, 
            name = app_config[str(i)]['name'],
            os = app_config[str(i)]['os']
        )
        output = os.popen(cmd)
        print output.read()

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        rtime = "today"
    elif argc == 2:
        rtime = str(sys.argv[1])

    if is_valid_date(rtime):
        run(rtime)
    else:
        print "invalid time"


    
