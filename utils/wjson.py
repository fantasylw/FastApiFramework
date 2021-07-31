from jsonpath import jsonpath
import json5 as json # 比json库多了处理注释的功能

__author__ = "luo wei"
__version__ = '0.3'
'''
v0.1
基本功能开发完成
v0.2
修复转化json文本的BUG
v0.3
支持json文本带注释
'''


def totable(data, root="$"):
    table = {}
    if type(data) in [dict, Json]:
        if data == {}:
            if root == "$":
                table = data
            else:
                table[root] = data
        else:
            for key in data.keys():
                node = root + "." + key
                table.update(totable(data[key], node))
    elif type(data) is list:
        for i, item in enumerate(data):
            child_node = root + "[%s]" % i
            table.update(totable(item, child_node))
    else:
        if root == "$":
            table = data
        else:
            table[root] = data
    return table


class JsonBase:

    def tostr(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True, quote_keys=True, indent=4, trailing_commas=False)

    def jsonpath(self, expr, *args):
        try:
            value = jsonpath(self, expr, *args)
        except Exception as e:
            value = str(e)
        return value

    def setvalue(self, expr, value):
        paths = jsonpath(self, expr, result_type='IPATH')
        tmp = ""
        if paths is False:
            raise Exception("异常:请检查当前{}语法！".format(expr))
        else:
            for path in paths:
                tmp = "self"
                for item in path:
                    if item.isdigit():
                        tmp += "[{}]".format(item)
                    else:
                        tmp += "['{}']".format(item)
                new_value = value
                if type(new_value) is str:
                    new_value = "'{}'".format(new_value)
                elif type(new_value) is bool:
                    new_value = str(new_value)
                exec_text = tmp + "={}".format(new_value)
                exec(exec_text)
        return paths

    def totable(self):
        return totable(self)


class Json:
    def __new__(cls, args):
        
        if type(args) is list:

            class Data(list, JsonBase):
                def __init__(self, *args):
                    super().__init__(*args)
        elif type(args) is dict:

            class Data(dict, JsonBase):
                def __init__(self, *args):
                    super().__init__(*args)
        else:
            args = dict(args)

            class Data(dict, JsonBase):
                def __init__(self, *args):
                    super().__init__(*args)

        return Data(args)

    @classmethod
    def str2Josn(cls, text: str):
        if text:
            #text = text.replace("'", '"')
            try:
                try:
                    data = json.loads(text)
                except:
                    data = False
                if not data:
                    try:
                        data = eval(text)
                    except:
                        data = False
                data = Json(data)
            except:
                data = False

            return data
        else:
            return {}
    
    @classmethod
    def str2Dict(cls, text: str):
        try:
            data = json.loads(text)
        except:
            data = False
        if not data:
            try:
                data = eval(text)
            except:
                data = False

        return data

    @classmethod
    def dict2str(cls, data):
        try:
            if type(data) is list:
                return json.dumps(data, ensure_ascii=False, sort_keys=True, quote_keys=True, indent=4, trailing_commas=False)
            else:
                for key in data:
                    if type(data[key]) not in [int,dict,list,bool,float,str]:
                        data[key] = str(data[key])
                return json.dumps(data, ensure_ascii=False, sort_keys=True, quote_keys=True, indent=4, trailing_commas=False)
        except Exception as e:
            print(e)
            return str(data)
    
    @classmethod
    def set_value(cls,data,expr, value):
        json_data = Json(data)
        json_data.setvalue(expr, value)
        new_data = dict(json_data)
        return new_data
