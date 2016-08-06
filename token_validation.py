#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import hashlib

def token_validation(config):
    time_str = "1467359117630"
    md5 = hashlib.md5()
    md5.update(config['appid']+ config['key'] + time_str)
    return md5.hexdigest()

def main():
    test = {
        'appid': '100001',
        'key': '19ff40c43e9811e68440fa163e9d827b',
        'lid': ''
    }
    print "token: %s" % token_validation(test)

if __name__ == '__main__':
    main()
