#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
from logging.handlers import TimedRotatingFileHandler

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
