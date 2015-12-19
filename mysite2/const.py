# coding:utf-8


class _const:

    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const (%s)" % name
        self.__dict__[name] = value

const = _const()


const.DeployStatus = {
    "unsolved": "未解决",
    "solved": "已解决",
    "closed": "关闭"
}
