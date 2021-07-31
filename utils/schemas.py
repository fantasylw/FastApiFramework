from pydantic import BaseModel,validator
from typing import List, Optional,Union

# 创建数据模型


class ModelLoginBody(BaseModel):
    name: Optional[str] = ""
    username:Union[int,str] =""
    password:str = ""

    @validator('username')
    def validator_empty(cls, value):
        if value =='':
            raise ValueError('必须有值')
        return str(value)
    
    @validator('password')
    def validator_password(cls, value):
        if value =='':
            return 'qq123123'
        return value


class ModelGetEditBody(BaseModel):

    id: str = ""
    name: str = ""
    username: str = ""
    password: str = ""

    @validator('id')
    def validatorId(cls, value):
        if value == '':
            raise ValueError('必须有值')
        return str(value)

class ModelGetRegisterBody(BaseModel):
    name: str = ""
    username: str = ""
    password: str = ""

    @validator('name', 'username', 'password')
    def validatorName(cls, value):
        if value == '':
            raise ValueError('必须有值')
        return str(value)

class ModelGetCookiesBody(BaseModel):
    url:str
    token:str

    @validator('url', 'token')
    def validator_empty(cls, value):
        if value =='':
            raise ValueError('必须有值')
        return value

class ModelLQLQueryBody(BaseModel):
    limit: Optional[int] = 20
    skip: Optional[int] = 0
    structure: Union[list, dict] = ["*"]
    query: dict = {}
    order: Optional[list] = []
