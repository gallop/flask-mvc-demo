
class Const:
    HTTP_ERROR = 9999
    TOKEN_INVALID = 1001
    TOKEN_BAD_SIGNATURE = 1002
    TOKEN_EXPIRED = 1003

    # class ConstError(TypeError):
    #     pass
    #
    # class ConstCaseError(ConstError):
    #     pass
    #
    # def __setattr__(self, name, value):
    #     if self.__dict__.has_key(name):
    #         raise self.ConstError("Can't change const.%s" % name)
    #     if not name.isupper():
    #         raise self.ConstCaseError('Const name "%s" is not all uppercase' % name)
    #     self.__dict__[name] = value


