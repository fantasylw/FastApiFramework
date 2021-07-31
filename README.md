# 介绍

这是一个基于fastapi+mongdo开发的Http后端快速开发框架，基本功能已包含了登录、数据库模型、工具类、日志类、路由等功能，可以搭建vue快速开发框架做到开箱即用。

# 初始化

1. 安装好python3环境，建议版本为3.9+

2. 安装mongo数据库，推荐用dokcer安装。

   > docker run -it -p 5000:27017  mongo:latest
   >
   > 若需要持久化数据，请使用-v参数，将容器的 /data 目录挂载到本机目录

3. 执行pip install -r requirements.txt 安装依赖库，若执行很慢请修改为清华源。

   > pip install pip -U
   >
   > pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

3. 执行python install.py 初始化数据库
4. 执行python main.py 访问站点
5. 访问 http://127.0.0.1:8888/docs 

# 学习资料

1. [FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/)
2. [mongoengine](http://docs.mongoengine.org/)

