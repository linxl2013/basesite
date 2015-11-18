# coding=utf-8

import re


class GetForm:

    elements = []
    data = {}
    error = []
    request = None

    def __init__(self, request):
        self.request = request

    def get(self, name, required=False, validType=None, minLen=None, maxLen=None, text="该输入框", errStr=None, default=None):
        value = self.request.GET.get(name, default)
        self.appendData(name, value, required, validType,
                        minLen, maxLen, text, errStr)

    def post(self, name, required=False, validType=None, minLen=None, maxLen=None, text="该输入框", errStr=None, default=None):
        value = self.request.POST.get(name, default)
        self.appendData(name, value, required, validType,
                        minLen, maxLen, text, errStr)

    def appendData(self, name, value, required, validType, minLen, maxLen, text, errStr):
        if required == True and errStr == None:
            errStr = "%s为必填项" % text
        element = {"name": name, "value": value, "required": required,
                   "validType": validType, "minLen": minLen, "maxLen": maxLen, "errStr": errStr}
        self.elements.append(element)

    def check(self):
        # print self.elements
        for element in self.elements:
            if element["required"] == True and (element["value"] == "" or element["value"] == None):
                msg = element["errStr"]
                self.error.append({"name": element["name"], "msg": msg})
                continue

            if element["validType"] != None:
                (ret, msg) = getattr(self, "valid_%s" %
                                     element["validType"])(element["value"])
                if ret == False:
                    self.error.append({"name": element["name"], "msg": msg})
                    continue

            if element["minLen"] > 0 and element["maxLen"] > 0 and (element["minLen"] > len(element["value"]) or element["maxLen"] < len(element["value"])):
                msg = "%s长度必须在%s~%s之间" % (element["text"], element[
                                          "minLen"], element["maxLen"])
                self.error.append({"name": element["name"], "msg": msg})
                continue

            elif element["minLen"] > 0 and element["maxLen"] == None and element["minLen"] > len(element["value"]):
                msg = "%s长度必须大于%s个字" % (element["text"], element["minLen"])
                self.error.append({"name": element["name"], "msg": msg})
                continue

            elif element["minLen"] == None and element["maxLen"] > 0 and element["maxLen"] < len(element["value"]):
                msg = "%s长度必须小于%s个字" % (element["text"], element["maxLen"])
                self.error.append({"name": element["name"], "msg": msg})
                continue

            self.data[element["name"]] = element["value"]

        if len(self.error) > 0:
            return (1, self.error)
        else:
            return (0, self.data)

    def valid_mobile(self, value):
        return (True, None)

    def valid_email(self, value):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", value) != None:
            return (True, None)
        else:
            return (False, "电子邮件地址格式错误")

    def valid_zipcode(self, value):
        return (True, None)

    def valid_url(self, value):
        return (True, None)

    def valid_number(self, value):
        return (True, None)
