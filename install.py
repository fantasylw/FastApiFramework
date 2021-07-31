
print("---初始化项目---")


print("1. 创建user模型")
user_model_script = '''
from mongoengine import Document
from mongoengine import StringField, BooleanField,DateTimeField


class ModelUser(Document):

    meta = {"collection": "user"}

    name = StringField(required=True,unique=True)
    username = StringField(required=True,unique=True) # 登陆账号
    password =  StringField(required=True) # 登陆密码
    lastlogin = DateTimeField() # 最后登陆时间
    avatar = StringField()  # 用户头像
    updated_time = DateTimeField() # 最后更新时间
    created_time = DateTimeField() # 创建时间 其实也可以从ID获取
    status = BooleanField(default=True,) # False 为软删除
    description  = StringField()
'''

with open('database/model_user.py','w', encoding='utf-8') as f:
    f.write(user_model_script)

exec('''
from mongoengine import connect
connect('case',host = '127.0.0.1:5000') # 连接数据库
from hashlib import md5
from database.model_user import ModelUser
user_admin_data = {
    "name": "管理员",
    "username": "admin",
    "password": md5("admin".encode('utf8')).hexdigest()
}
try:
    print('创建账号：admin,密码为：admin')
    ModelUser(**user_admin_data).save()
except:
    print('admin已存在')
''')

print("2. 创建project模型")
project_model_script = '''
from mongoengine import Document
from .model_user import ModelUser
from mongoengine import StringField,BooleanField,DateTimeField,ReferenceField


class ModelProject(Document):

    meta = {"collection": "project"}

    name = StringField(required=True,unique=True)

    owner = ReferenceField(ModelUser, required=True) # 项目管理员

    updated_time = DateTimeField() # 最后更新时间
    created_time = DateTimeField() # 创建时间 其实也可以从ID获取
    status = BooleanField(default=True,) # False 为软删除
    description  = StringField()

'''

with open('database/model_project.py','w',encoding='utf-8') as f:
    f.write(project_model_script)

print("---初始化完毕---")