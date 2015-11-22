# coding=utf-8

import re


class GetForm:

    elements = None
    data = None
    error = None
    request = None

    def __init__(self, request):
        self.elements = []
        self.data = {}
        self.error = []
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
                   "validType": validType, "minLen": minLen, "maxLen": maxLen, "text": text, "errStr": errStr}
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
                                     element["validType"])(element["value"], text=element["text"])
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

    def valid_mobile(self, value, *args, **kwargs):
        if re.match("^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$", value) != None:
            return (True, None)
        else:
            return (False, "手机号码格式错误")

    def valid_email(self, value, *args, **kwargs):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", value) != None:
            return (True, None)
        else:
            return (False, "电子邮件地址格式错误")

    def valid_zipcode(self, value, *args, **kwargs):
        if re.match("^[1-9]\d{5}$", value) != None:
            return (True, None)
        else:
            return (False, "邮编号码格式错误")

    def valid_url(self, value, *args, **kwargs):
        if re.match("^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$", value) != None:
            return (True, None)
        else:
            return (False, "网址格式错误")

    def valid_number(self, value, *args, **kwargs):
        if re.match("\d+", value) != None:
            return (True, None)
        else:
            return (False, "%s必须为数字" % kwargs["text"])
