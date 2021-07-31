# 统一的异常类
class ErrorLog(Exception):

    def __init__(self, error, title='error') -> None:
        self.error = error
        self.title = title
        import traceback
        import sys
        self.paths = sys.argv
        _type, _value, _tb = sys.exc_info()
        if _tb:
            _, _lineno, _, line_content = traceback.extract_tb(_tb, 1)[0]
            self.type = _type.__name__
            self.line_number = _lineno
            self.line_content = line_content
            if _value.args:
                self.description = str(_value)
            else:
                self.description = _type.__name__
        else:
            self.type = None
            self.line_number = None
            self.line_content = ''
            self.description = str(self.error)
    
    def get_report(self):
        return {
            'title': self.title,
            "type": self.type,
            "line_number": self.line_number,
            "line_content": self.line_content,
            "message": self.description
        }

# 后续的太细了, 好啰嗦, 重构后不要了
# 不支持的表达式类型
class ExpressionTypeError(Exception):
    name = "表达式类型异常"

    def __init__(self, message):
        self.message = message

# 非json响应


class ReponseBodyTypeError(Exception):
    name = "响应类型异常"

    def __init__(self, message):
        self.message = message


class SettingError(Exception):
    name = "设置值异常"

    def __init__(self, message):
        self.message = message


class ExtractsError(Exception):
    name = "取值异常"

    def __init__(self, message):
        self.message = message


class AssertionsError(Exception):
    name = "断言异常"

    def __init__(self, message):
        self.message = message


class PreCodeError(Exception):
    name = "前置代码异常"

    def __init__(self, message):
        self.message = message


class PostCodeError(Exception):
    name = "后置代码异常"

    def __init__(self, message):
        self.message = message


class CiteRunError(Exception):
    name = "引用用例执行异常"

    def __init__(self, message):
        self.message = message


class SQLConnectError(Exception):
    name = "数据库连接异常"

    def __init__(self, message):
        self.message = message


class SQLCursorError(Exception):
    name = "数据库执行异常"

    def __init__(self, message):
        self.message = message


class TestCaseDebugError(Exception):
    name = "用例调试执行异常"

    def __init__(self, message):
        self.message = message


class SettingsError(Exception):
    name = "参数化设置异常"

    def __init__(self, message):
        self.message = message

