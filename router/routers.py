from router.user import login
from router.lql import lql

data = [
    (lql.router, '/lql', ['统一查询器']),
    (login.router,'/user',['用户'])
]
