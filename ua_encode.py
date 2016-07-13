#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib

def unquote(ua_str):
    result = urllib.unquote(ua_str)
    print ("ua unquote: %s" % result)

def quote(target):
    result = urllib.quote(target)
    print ("ua quote: %s" % result)

def main():
    origin = "Mozilla/5.0+(Windows+NT+6.3;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/37.0.2049.0+Safari/537.36"
    ua1 = "Mozilla%2F5.0+%28Windows+NT+6.3%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F37.0.2049.0+Safari%2F537.36"
    ua2 = "Mozilla%2F5.0%2B%28Windows%2BNT%2B6.3%3B%2BWin64%3B%2Bx64%29%2BAppleWebKit%2F537.36%2B%28KHTML%2C%2Blike%2BGecko%29%2BChrome%2F37.0.2049.0%2BSafari%2F537.36"
    quote(origin)
    unquote(ua2)

if __name__ == '__main__':
    main()
