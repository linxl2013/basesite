# coding:utf-8
import hashlib
import json
import time
from decimal import Decimal
from datetime import date, datetime


def md5(s):
    return hashlib.md5(str(s)).hexdigest()


def sha1(s):
    return hashlib.sha1(str(s)).hexdigest()


class Json:

    @staticmethod
    def decode(s, default=[]):
        s = Filters.trim(str(s))
        if '' == s:
            return default
        try:
            return escape.json_decode(s)
        except Exception, e:
            return default

    @staticmethod
    def encode(obj):
        return json.dumps(obj, cls=TypeEncoder).replace("</", "<\\/")


class TypeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)
