#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import requests
import uuid
import random
import urllib
import json
import urlparse
import datetime
import time
import hashlib
import copy
import os
import sys
import chardet
import threading
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
import template.bridge_demo_json as bridge_demo_json

class LoggerAllocator(object):

    def __init__(self):
        logfile_path = os.popen('pwd').read().strip()
        log_dir = os.path.join(logfile_path, 'test_log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        #test
        logfile_name = os.path.join(logfile_path, 'test_log/test.log')
        file_fmt = logging.Formatter('%(asctime)s - [%(name)s]: %(message)s')
        file_handler = logging.handlers.TimedRotatingFileHandler(logfile_name, when='midnight', interval=1)
        file_handler.setFormatter(file_fmt)
        self.logger = logging.getLogger('test')
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

        #win
        win_logfile_name = os.path.join(logfile_path, 'test_log/win.log')
        win_file_fmt = logging.Formatter('%(asctime)s - [%(name)s]: %(message)s')
        win_file_handler = logging.handlers.TimedRotatingFileHandler(win_logfile_name, when='midnight', interval=1)
        win_file_handler.setFormatter(win_file_fmt)
        self.win_logger = logging.getLogger('win')
        self.win_logger.addHandler(win_file_handler)
        self.win_logger.setLevel(logging.INFO)

        #click
        click_logfile_name = os.path.join(logfile_path, 'test_log/click.log')
        click_file_fmt = logging.Formatter('%(asctime)s - [%(name)s]: %(message)s')
        click_file_handler = logging.handlers.TimedRotatingFileHandler(click_logfile_name, when='midnight', interval=1)
        click_file_handler.setFormatter(click_file_fmt)
        self.click_logger = logging.getLogger('click')
        self.click_logger.addHandler(click_file_handler)
        self.click_logger.setLevel(logging.INFO)

        # error.log
        error_logfile_name = os.path.join(logfile_path, 'test_log/error.log')
        error_file_fmt = logging.Formatter('%(asctime)s - [%(name)s]: %(message)s')
        error_file_handler = logging.handlers.TimedRotatingFileHandler(error_logfile_name, when='midnight', interval=1)
        error_file_handler.setFormatter(error_file_fmt)
        self.error_logger = logging.getLogger('error')
        self.error_logger.addHandler(error_file_handler)
        self.error_logger.setLevel(logging.ERROR)

        #count
        logfile_name = os.path.join(logfile_path, 'test_log/count.log')
        file_fmt = logging.Formatter('%(asctime)s - [%(name)s]: %(message)s')
        file_handler = logging.handlers.TimedRotatingFileHandler(logfile_name, when='midnight', interval=1)
        file_handler.setFormatter(file_fmt)
        self.count_logger = logging.getLogger('count')
        self.count_logger.addHandler(file_handler)
        self.count_logger.setLevel(logging.INFO)

    def log_test(self, msg):
        self.logger.debug(msg)

    def log_win(self, msg):
        self.win_logger.info(msg)

    def log_click(self, msg):
        self.click_logger.info(msg)

    def log_count(self, msg):
        self.count_logger.info(msg)

    def error(self, msg):
        self.error_logger.error(msg)

LOGGER = LoggerAllocator()


class ReqSimulator(object):

    def __init__(self, demo_req, app_conf):
        self.req = copy.deepcopy(demo_req)
        self.adtype = self.get_adtype()
        self.update_req_validation(app_conf)
        self.has_extra_process = True
        self.req_url = 'http://127.0.0.1:8999'
        self.req_succ = 0
        self.req_fail = 0
        self.send_win = 0
        self.send_win_succ = 0
        self.send_win_fail = 0
        self.send_clk = 0
        self.send_clk_succ = 0
        self.send_clk_fail = 0
        self.win_rate = 100
        self.click_rate = 100
        self.is_test_pv = True
        self.bridge_version = "1.0"
        self.vendor_id = "brssp"

    def run(self, req_count):
        try:
            self.send_requests(req_count)
        except Exception, ex:
            error_msg = self.get_traceback_msg(ex)
            LOGGER.error('sid: %s, exception: %s' % (self.sid, error_msg))

    def send_requests(self, req_count):
        for count in range(0, req_count):
            self.do_send_request()
            time.sleep(1)

        print ("succ:%d, fail:%d, win_count:%d, click_count:%d, win_succ:%d, click_succ:%d" % 
            (self.req_succ, self.req_fail, self.send_win, self.send_clk, self.send_win_succ, self.send_clk_succ))
        LOGGER.log_count("succ:%d, fail:%d, win_count:%d, click_count:%d, win_succ:%d, click_succ:%d" % 
            (self.req_succ, self.req_fail, self.send_win, self.send_clk, self.send_win_succ, self.send_clk_succ))

    def do_send_request(self):
        try:
            self.sid = uuid.uuid1().hex
            req_headers = self.get_req_headers()
    
            json_str = json.dumps(self.req, ensure_ascii=False, encoding='utf-8')
            start_time = time.time()
            rsp = requests.post(self.req_url, data=json_str, headers=req_headers, timeout=1)
            end_time = time.time()
            rsp_content = json.loads(rsp.content)
    
            if rsp.status_code == 200 and rsp_content['code'] == 0:
                LOGGER.log_test("succeed, spend time: %s ms, rsp.status_code: %s, rsp.text: %s" % (
                    int((end_time - start_time) * 1000),
                    rsp.status_code, 
                    json.dumps(json.loads(rsp.text), sort_keys=False, indent=4, separators=(',', ': '))))

                self.req_succ += 1
                win_urls, clk_urls = self.get_callback_urls(rsp_content)
                self.call_urls(win_urls, clk_urls)
            else:
                self.req_fail += 1
                LOGGER.log_test("failed, spend time: %s ms, rsp.status_code: %s, rsp.text: %s" % (
                    int((end_time - start_time) * 1000), rsp.status_code, rsp.text))

        except Exception, ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback

    def get_req_headers(self):
        headers = {}
        headers['content-type'] = 'application/json'
        headers['x-bridge-version'] = self.bridge_version
        headers['x-vendor-id'] = self.vendor_id
        if self.is_test_pv:
            headers['x-is-test'] = 'Y'
        return headers

    def get_adtype(self):
        adtype = 'banner'
        for imp in self.req['imp']:
            if 'native' in imp.keys():
                adtype = 'native'
                break
        return adtype

    def update_req_validation(self, app_conf):
        try:
            self.req['app']['id'] = app_conf['appid']
            self.req['time'] = str(int(time.time() * 1000))

            md5 = hashlib.md5()
            md5.update(app_conf['appid']+ app_conf['key'] + self.req['time'])
            self.req['token'] = md5.hexdigest()

            self.req['imp'][0][self.adtype]['id'] = app_conf['lid']
            if self.has_extra_process:
                self.extra_process()
        except Exception, ex:
            error_msg = self.get_traceback_msg(ex)
            LOGGER.error('init exception: %s' % error_msg)

    def extra_process(self):
        self.req['imp'][0]['banner']['w'] = 320
        self.req['imp'][0]['banner']['h'] = 50
        
    def get_traceback_msg(self, ex):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        msg = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error_str = ''
        for item in msg:
            error_str += item
        return error_str

    def get_callback_urls(self, rsp):
        try:
            win_urls = []
            clk_urls = []
            if self.adtype == 'banner':
                for imp in rsp['adsimp'][0]['impbanner']['impreport']:
                    win_urls.append(imp['url'])
                for click in rsp['adsimp'][0]['impbanner']['clickreport']:
                    clk_urls.append(click['url'])
            elif self.adtype == 'native':
                for imp in rsp['adsimp'][0]['impnative']['impreport']:
                    win_urls.append(imp['url'])
                for click in rsp['adsimp'][0]['impnative']['clickreport']:
                    clk_urls.append(click['url'])
            return win_urls, clk_urls
        except Exception, ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback
    
    def call_urls(self, win_urls, clk_urls):
        try:
            randomNum = random.randint(1, 100)

            if randomNum <= self.win_rate:
                if len(win_urls) != 0:
                    for win_url in win_urls:
                        start_time = time.time()
                        rsp_win = requests.get(win_url)
                        end_time = time.time()
                        self.send_win += 1
                        result = ''
                        if rsp_win.status_code != 200:
                            self.send_win_fail += 1
                            result = 'failed'
                        else:
                            self.send_win_succ += 1
                            result = 'succeed'

                        LOGGER.log_win("sid: %s, send result: %s, spend time: %s ms, url: %s" % (
                            self.sid, result, int((end_time - start_time) * 1000), win_url))
    
            if randomNum < self.click_rate:
                if len(clk_urls) != 0:
                    for clk_url in clk_urls:
                        start_time = time.time()
                        rsp_click = requests.get(clk_url)
                        end_time = time.time()
                        self.send_clk += 1
                        result = ''
                        if rsp_click.status_code != 200:
                            self.send_clk_fail += 1
                            result = 'failed'
                        else:
                            self.send_clk_succ += 1
                            result = 'succeed'

                        LOGGER.log_click("sid: %s, send result: %s, spend time: %s ms, url: %s" % (
                            self.sid, result, int((end_time - start_time) * 1000), clk_url))
        except Exception, ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback


def main():
    app_conf = {
        'appid': '5e9a8fe4e75211e5a337001c42998040',
        'key': '4114636ce75211e5a337001c42998040',
        'lid': '522c9530e75211e5a337001c42998040'
    }

    #req_simulator = ReqSimulator(bridge_demo_json.bridge_demo_banner_req, app_conf)
    req_simulator = ReqSimulator(bridge_demo_json.bridge_demo_native_req, app_conf)
    req_simulator.run(1)

if __name__ == '__main__':
    main()
