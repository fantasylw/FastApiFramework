from fastapi import APIRouter
from fastapi import Header
from fastapi import Request
from fastapi import Depends
from hashlib import md5
from typing import Any, Union,Optional
from datetime import datetime, timedelta
from jose import jwt
from database.model_user import ModelUser
from setting.config import SECRET_KEY
from utils.message import  USER_LOGIN_ERROR, USER_INFO_ERROR, USER_INFO_EXPIRED
from utils.response import ResponseCode
from utils.schemas import ModelLoginBody

router = APIRouter()
ALGORITHM = "HS256"

# 加密密钥 这个很重要千万不能泄露了 
# 设置过期时间 现在时间 + 有效时间 1天 如果要给流水线的接口 可以额外写一个无限制的.

def get_expire():
    expire = datetime.utcnow() + timedelta(days=1) # exp 是固定写法必须得传
    return  expire


def check_jwt_token(token: Optional[str] = Header(None)) -> Union[str, Any]:
    try:
        payload = jwt.decode( token, SECRET_KEY, algorithms=[ALGORITHM] )
        return payload
    except Exception as e:
        if e.__class__ is jwt.JWTError:
            return USER_INFO_ERROR
        else:
            return USER_INFO_EXPIRED


@router.post("/login")
def login(body:ModelLoginBody):
    username = body.username
    password = md5(body.password.encode('utf8')).hexdigest()
    try:
        user = ModelUser.objects.get(username=username,password=password)
    except:
        return USER_LOGIN_ERROR
    login_encode = {"exp": get_expire(), "id": str(user.id), "username": user.username} # 生成token 
    encoded_jwt = jwt.encode(login_encode, SECRET_KEY, algorithm=ALGORITHM)
    data = {
        "token": encoded_jwt,
        "owner": str(user.id)
    }
    return ResponseCode.code_200(data)

@router.get("/info", summary="获取用户信息")
def get_user_info(request: Request, token_data: Union[str, Any] = Depends(check_jwt_token)) -> Any:
    """ 获取用户信息 :param token_data: :return: """
    # print(token_data) # 这个状态能响应说明token验证通过
    client_host = request.client.host
    if "username" not in token_data:
        return token_data
    else:
        user_id = token_data['id']
        user =  ModelUser.objects.get(id = user_id)
        data= {
                "roles": [
                    "admin" # TODO 角色跟权限以后再补充
                ],
                "description": user.description,
                "avatar": user.avatar,
                "name": user.name,
                "owner": user_id,
                "username": user.username,
                "client_host": client_host
            }
        return ResponseCode.code_200(data=data)


@router.post("/add")
def login(body:ModelLoginBody):
    user_admin_data = {
        "name": body.name,
        "username": body.username,
        "password": md5(body.password.encode('utf8')).hexdigest()
    }
    try:
        ModelUser(**user_admin_data).save()
    except:
        return USER_LOGIN_ERROR
    return ResponseCode.code_200('创建成功！')
