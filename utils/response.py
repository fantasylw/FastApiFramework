from  bson.objectid import ObjectId
from datetime import datetime,date
import json


class MongoDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, (datetime,date)):
            return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        else:
            return super(MongoDataEncoder, self).default(obj)


def to_response(data):
    if type(data) in [dict, list]:
        rsp_data = json.dumps(data, cls=MongoDataEncoder)
        rsp_data = json.loads(rsp_data)
    elif data.__class__.__name__ == "ObjectId":
        rsp_data = {"id": str(data)}
    else:
        rsp_data = data
    return rsp_data


def render_response(data, code=200, message="请求成功", success=True, total=None):
    if type(data) in [dict,list]:
        rsp_data = json.dumps(data, cls=MongoDataEncoder)
        rsp_data = json.loads(rsp_data)
    elif data.__class__.__name__ == "ObjectId":
        rsp_data = {"id": str(data)}
    else:
        rsp_data = data
    if total is not None:
        return_data = {"data": rsp_data, "message": message,
                   "total": total, "code": code, "success": success}
    else:
        return_data = {"data": rsp_data, "message": message, "code": code, "success": success}
    return return_data


class ResponseCode:

    staticmethod
    def code_200(data, message="请求成功", total=None,):
        return render_response(data, message=message, total=total)
    
    staticmethod
    def code_500(data, message="服务执行异常"):
        return render_response(data, message=message, code=500, success=False)

