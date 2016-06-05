#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import uuid
import time

class Generator(object):
    def __init__(self, app_count):
        self.app_count = app_count
        self.gen_app_conf()
    
    def gen_app_conf(self):
        for app_name in range(0, self.app_count):
            self.do_gen_app_conf(app_name)

    def do_gen_app_conf(self, app_name):
        time.sleep(3)
        appid = uuid.uuid1().hex
        time.sleep(5)
        key = uuid.uuid1().hex
        time.sleep(5)
        lid = uuid.uuid1().hex
        print ("appname: %s, appid: %s, key: %s, lid: %s\n" % (app_name, appid, key, lid))

if __name__ == '__main__':
    generator = Generator(1)

