from bson.objectid import ObjectId
from fastapi import APIRouter
from datetime import datetime
from utils.errors import ErrorLog
from utils.schemas import ModelLQLQueryBody
from utils.response import ResponseCode
from utils import tools

router = APIRouter()


def get_model_object(name):
    try:
        from_name = 'model_' + name.lower().split('model')[1]
        exec_code = f'from database.{from_name} import {name}'
        exec(exec_code)
        return eval(name)
    except Exception as e:
        raise ErrorLog(e,'获取模型对象异常')

def exec_query(keys, report, data):
    if type(keys) in [dict, list]:  # TODO dict还没进行测试
        if '*' in keys:
            return tools.get_dict_for_model(report)
        for key in keys:
            
            if type(key) is str:
                if '=>' in key:
                    key_list = key.split('=>')
                    data_key = key_list[1]
                    report_key = key_list[0]
                else:
                    report_key = data_key = key
                try:
                    item_value = report[report_key]
                except:
                    item_value = '已删除'
                class_name = item_value.__class__.__name__
                if 'Model' in class_name:
                    if type(keys) is list:
                        data[data_key] = item_value.id
                    else:
                        data[data_key] = exec_query(
                            keys[key], item_value, {})
                else:
                    data[data_key] = item_value
            elif type(key) is dict:
                for item in key:
                    if '=>' in item:
                        key_list = item.split('=>')
                        data_key = key_list[1]
                        report_key = key_list[0]
                    else:
                        report_key = data_key = item
                    try:
                        if report[report_key]:
                            data[data_key] = exec_query(key[item], report[report_key], {})
                        else:
                            data[data_key] = None
                    except Exception as e:
                        print(str(e))
                        data[data_key] = '已删除'
    else:
        data = report[keys]
    return data

def get_model_query(query):
    model_query = {}
    if 'id' in query:
        query['_id'] = ObjectId(query.pop('id'))
    for key in query:
        value = query[key]
        if '@' in key:
            value = ObjectId(value) if value else value
            if value == '':
                continue
            key = key.replace('@','')
        if key[-1] == '%':
            # 模糊匹配
            model_query[key[:-1]] = {
                '$regex': value
            }
        elif key[-1] == '≠':
            model_query[key[:-1]] = {
                '$ne': value
            }
        elif key[-1] == '&':
            judgment_data = value
            for judgment in judgment_data:
                judgment_value = judgment_data[judgment]
                if judgment == '>':
                    judgment_key = '$gt'
                elif judgment == '>=':
                    judgment_key = '$gte'
                elif judgment == '<':
                    judgment_key = '$lt'
                elif judgment == '<=':
                    judgment_key = '$lte'
                elif judgment == '!=':
                    judgment_key = '$ne'
                elif judgment == 'format':
                    continue
                else:
                    raise f'不支持的判断方法:{judgment}'
                if 'format' in judgment_data:
                    # format 为 时间专用
                    judgment_value = datetime.strptime(
                        judgment_value, judgment_data['format'])
                model_query[key[:-1]] = {judgment_key: judgment_value}
        else:
            model_query[key] = value
    return model_query

def get_model_data(query):
    model_data = {}
    for key in query:
        value = query[key]
        if '@' in key:
            value = ObjectId(value) if value else value
            key = key.replace('@', '')
        model_data[key] = value
    return model_data

@router.post("/{model}/query")
def query(query_data: ModelLQLQueryBody, model: str):
    total = 0
    structure = query_data.structure
    try:
        ModelObject = get_model_object(model)
        model_query = get_model_query(query_data.query)
        if type(structure) is list:
            data = []
            skip = query_data.skip
            limit = query_data.limit
            # 查询列表
            if 'id' in model_query:
                model_query['_id'] = model_query.pop('id')
            query_iter = ModelObject.objects(
                __raw__=model_query).order_by(*query_data.order)
            total = query_iter.count()
            limit = limit if total > limit else total
            report_list = query_iter.skip(skip).limit(limit)
            for report in report_list:
                item = {}
                item = exec_query(structure, report, item)
                data.append(item)
        else:
            data = {}
            if '_id' not in model_query:
                return ResponseCode.code_500('查询单个详情时, query必须且只能包含id字段')
            else:
                one_model_query = {"id": model_query.pop('_id')}
            # 查询单个记录
            report = ModelObject.objects.get(**one_model_query)
            if report:
                data = exec_query(structure, report, data)
            else:
                data = {}
    except Exception as e:
       return ResponseCode.code_500(str(e))
    return ResponseCode.code_200(data, total=total)


@router.post("/{model}/save")
def save(data: dict, model: str):
    try:
        ModelObject = get_model_object(model)
        data = get_model_data(data)
        data_id = data.get('id')
        if data_id:
            meodel_obj = ModelObject.objects.get(id=data_id)
            meodel_obj.updated_time = datetime.now()
            meodel_obj.update(**data)
        else:
            meodel_obj = ModelObject(**data)
            meodel_obj.created_time = datetime.now()
            meodel_obj.save()
    except Exception as e:
        return ResponseCode.code_500(str(e))
    return ResponseCode.code_200(data=str(meodel_obj.id), message="保存成功!")


if __name__ == "__main__":
    # 通用查询框架
    # ModelCaseReport
    case1 = {
        "limit": 3,
        "skip": 1,
        "structure": [
            "name",
            {
                "case_id=>case": [
                    "id",
                    "name"
                ],
                "project=>projectId": "id",
                "project=>projectName": "name"
            }
        ],
        "query": {
            "name": "生产过程检验"
        }
    }
    # 查询单条时, 查询条件有且只有主键
    case2 = {
        "structure": {
            "name": 1,
            "case_id=>case": [
                "id",
                "name"
            ],
            "project=>projectId": "id",
            "project=>projectName": "name"
        },
        "query": {
            "id": "6084ca3eece339e6ad3f1a5e"
        }
    }
    # 单条, 返回全部信息
    case2_2 = {
        "limit": 3,
        "skip": 0,
        "structure": {
            "*": 1
        },
        "query": {
            "id": "60865e9f599ba74b48248365"
        }
    }
    # 加id查询
    case3 = {
        "limit": 3,
        "skip": 0,
        "structure": [
            "name",
            {
                "case_id=>case": [
                    "id",
                    "name"
                ],
                "project=>projectId": "id",
                "project=>projectName": "name"
            }
        ],
        "query": {
            "name%": "生产过程检验",
            "id": "6084ca3eece339e6ad3f1a5e"
        }
    }
    # 用 * 匹配所有字段
    case3 = {
        "limit": 3,
        "skip": 0,
        "structure": [
            "name",
            {
                "case_id=>case": [
                    "*"
                ],
                "project=>projectId": "id",
                "project=>projectName": "name"
            }
        ],
        "query": {
            "name%": "生产过程检验"
        }
    }
    # 时间范围查询
    case4 = {
        "limit": 3,
        "skip": 0,
        "structure": [
            "name",
            {
                "case_id=>case": [
                    "id"
                ],
                "project=>projectId": "id",
                "project=>projectName": "name"
            },
            "created_time"
        ],
        "query": {
            "name%": "生产过程检验",
            "created_time&": {
                ">": "2021-04-25 11:00",
                "<": "2021-04-25 11:39",
                "format": "%Y-%m-%d %H:%M"
            }
        }
    }
    # 符合范围查询
    case5 = {
        "limit": 3,
        "skip": 0,
        "structure": [
            "*"
        ],
        "query": {
            "created_time&": {
                ">": "2021-04-25 11:00",
                "<": "2021-04-27 11:39",
                "format": "%Y-%m-%d %H:%M"
            },
            "status&": {
                ">=": 0, "<": 2
            }
        }
    }
    '''
    相等
    % 正则
    & {} 范围 ">0,<=1000"
    @ 强制转换为 objectId
    => 更改名字
    ≠ 不等于
    '''
