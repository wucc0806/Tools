#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from jsonschema import Draft4Validator
#from jsonschema import ValidationError
import traceback
import time

            #"banner": {
            #    "w": 640,
            #    "h": 100,
            #    "id": "82edc8b0e5ec11e5a92ba45e60c539c5"
            #}
bridge_demo_banner_req = {
    "api": "1.0",
    "time": "1414764477867",       
    "token": "2c38ec54777641d9687aa8b65e7fa621",
    "reqid": "2c38ec54777641d9687aa8bgrefef343",
    "imp": [
        {
            "id": "60a9b20ce5ec11e5af66a45e60c539c5",
            "banner": {
                "w": "640",
                "h": "100",
                "id": "82edc8b0e5ec11e5a92ba45e60c539c5"
            }
        },
        {
            "id": "60a9b20ce5ec11e5af66a45e60c539c5",
            "banner": {
                "w": 640,
                "h": 100,
                "id": "82edc8b0e5ec11e5a92ba45e60c539c5"
            }
        }
    ],
    "app": {
        "id": "8b3bf4f8e5ec11e59e50a45e60c539c5",
        "ver": "1.0.1",
        "bundle": "com.package.java",
        "name": "test_name",
        "cat": [
            "IAB1-1"
        ]
    },
    "device": {
        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257",
        "ip": "58.53.67.42",
        "geo": {
            "lat": 31.167,
            "lon": 112.582,
            "country": "CHN",
            "type": 1
        },
        "sw": 1080,
        "sh": 1920,
        "sd": 428,
        "make": "HUAWEI",
        "brand": "HUAWEI",
        "model": "HUAWEI Y600-U00",
        "os": 2,
        "osv": 7,
        "did": "d625c3e923fc057afbfa942e90b7212",
        "mac": "38:bc:1a:c7:3b:11",
        "adid": "d625c3e923fc057afbfa942e90b77511",
        "carrier": "46000",
        "connectiontype": 2,
        "devicetype": 1
    }
}

bridge_demo_native_req = {
    "api": "1.0",
    "time": "1414764477867",       
    "token": "2c38ec54777641d9687aa8b65e7fa621",
    "reqid": "2c38ec54777641d9687aa8bgrefef343",
    "imp": [
        {
            "id": "60a9b20ce5ec11e5af66a45e60c539c6",
            "native": {
                "id": "82edc8b0e5ec11e5a92ba45e60c539c5",
                "adtype": 14,
                "session": {
                    "id": "82edc8b0e5ec11e5a92ba45e60c539c5",
                    "context": ["001", "002"],
                    "isunique": 1,
                    "seq": 5,
                },
                "adslot": {
                    "image": [
                        {
                            "id": "1",
                            "imgtyp": 2,
                            "w": 640,
                            "h": 200
                        }
                    ],
                    "word": [
                        {
                            "id": "1",
                            "wtyp": 2,
                            "max": 22
                        },
                        {   
                            "id": "2",
                            "wtyp": 3,
                            "max": 20
                        },
                        {   
                            "id": "3",
                            "wtyp": 4,
                            "max": 20
                        }
                    ]
                }
            }
        }
    ],
    "app": {
        "id": "8b3bf4f8e5ec11e59e50a45e60c539c5", 
        "ver": "1.0.1",
        "bundle": "com.package.java",
        "name": "Book",
        "cat": [
            "IAB1-1"
        ]
    },
    "device": {
        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257",
        "ip": "58.53.67.42",
        "geo": {
            "lat": 31.167,
            "lon": 112.582,
            "country": "CHN",
            "type": 1
        },
        "sw": 1080,
        "sh": 1920,
        "sd": 428,
        "make": "HUAWEI",
        "brand": "HUAWEI",
        "model": "HUAWEI Y600-U00",
        "os": 2,
        "osv": "7.1",
        "mac": "38:bc:1a:c7:3b:11",
        "did": "d625c3e923fc057afbfa942e90b7212",
        "adid": "d625c3e923fc057afbfa942e90b77511",
        "carrier": "46000",
        "connectiontype": 2,
        "devicetype": 1
    }
}


        #"adid": "d625c3e923fc057afbfa942e90b77511",

bridge_schema = {
    'type': 'object',
    'properties': {
        'api': {'type': 'string'},
        'time': {'type': 'string'},
        'token': {'type': 'string'},
        'reqid': {'type': 'string'},
        'imp': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'native': {'$ref': '#/definitions/native'},
                    'banner': {'$ref': '#/definitions/banner'}
                },
                'required': ['id'],
                'minProperties': 2
            }
        },
        'app': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'ver': {'type': 'string'},
                'bundle': {'type': 'string'},
                'name': {'type': 'string'},
                'cat': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            },
            'required': ['id', 'ver', 'bundle', 'name', 'cat']
        },
        'device': {
            'type': 'object',
            'properties': {
                'ua': {'type': 'string'},
                'ip': {'type': 'string'},
                'geo': {'$ref': '#/definitions/geo'},
                'sw': {'type': 'integer'},
                'sh': {'type': 'integer'},
                'sd': {'type': 'integer'},
                'make': {'type': 'string'},
                'brand': {'type': 'string'},
                'model': {'type': 'string'},
                'os': {'type': 'integer', 'enum': [0, 1, 2, 3]},
                'osv': {'type': 'string'},
                'did': {'type': 'string'},
                'mac': {'type': 'string'},
                'adid': {'type': 'string'},
                'carrier': {'type': 'string'},
                'connectiontype': {'type': 'integer', 'enum': [0, 1, 2, 3, 4]},
                'devicetype': {'type': 'integer', 'enum': [0, 1, 2, 3]}
            },
            'anyOf': [
                { 'required': ['ip', 'sw', 'sh', 'model', 'os', 'osv', 'did', 'adid', 'carrier', 'connectiontype', 'devicetype'] },
                { 'required': ['ip', 'sw', 'sh', 'model', 'os', 'osv', 'adid', 'carrier', 'connectiontype', 'devicetype'] }
            ]
        },
        'env': {
            'type': 'object',
            'properties': {
                'applist': {
                    'type': 'array',
                    'items': {
                        'bundle': {'type': 'string'}
                    },
                    'required': ['bundle']
                }
            }
        }
    },
    'required': ['api', 'time', 'token', 'reqid', 'imp', 'app', 'device'],
    'definitions': {
        'banner': {
            'type': 'object',
            'properties': {
                'w': {'type': 'integer'},
                'h': {'type': 'integer'},
                'id': {'type': 'string'}
            },
            'required': ['w', 'h', 'id']
        },
        'session': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'context': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                },
                'isunique': {'type': 'integer', 'enum': [0, 1]},
                'seq': {'type': 'integer'}
            },
            'required': ['id', 'seq']
        },
        'image': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'imgtyp': {'type': 'integer', 'mininum': 1, 'maxinum': 10},
                'w': {'type': 'integer'},
                'h': {'type': 'integer'}
            },
            'required': ['id', 'imgtyp', 'w', 'h']
        },
        'word': {
            'type': 'object', 
            'properties': {
                'id': {'type': 'string'},
                'wtyp': {'type': 'integer', 'mininum': 1, 'maxinum': 7},
                'max': {'type': 'integer'}
            },
            'required': ['id', 'wtyp', 'max']
        },
        'adslot': {
            'type': 'object',
            'properties': {
                'image': {
                    'type': 'array',
                    'items': {
                        '$ref': '#/definitions/image'
                    }
                },
                'word': {
                    'type': 'array',
                    'items': {
                        '$ref': '#/definitions/word'
                    }
                }
            },
            'required': ['image', 'word']
        },
        'native': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'adtype': {'type': 'integer'},
                'session': {'$ref': '#/definitions/session'},
                'adslot': {'$ref': '#/definitions/adslot'}
            },
            'required': ['id', 'adtype', 'adslot']
        },
        'geo': {
            'type': 'object',
            'properties': {
                'lat': {'type': 'number'},
                'lon': {'type': 'number'},
                'country': {'type': 'string'},
                'type': {'type': 'integer', 'enum': [1, 2, 3]}
            },
            'required': ['lat', 'lon']
        }
    }
}


class Test(object):
    def test(self):
        try:
            validator = Draft4Validator(bridge_schema)
            msg = ''
            def get_path(err_path):
                path = ""
                for dot in err_path:
                    path += "[%s]" % dot
                return path
            for error in validator.iter_errors(bridge_demo_banner_req):
                msg += "%s: %s\n" % (get_path(error.path), error.message)
            print msg
        except ex:
            print "there is a validation error"
        
if __name__ == '__main__':
    t = Test()
    t.test()
