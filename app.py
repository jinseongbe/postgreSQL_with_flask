from flask import Flask, request
from flask_restx import Api, Resource

from todo import Todo
from account import Test_account

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="jinseongbe's API Study Server",
    description="for study, API Server!",
    terms_url="/",
    contact="jinseongbe@gmail.com",
    license="MIT"
)
api.add_namespace(Test_account, '/account')
api.add_namespace(Todo, '/todos')






# flask_restx(name space)를 쓰지 않았을때 사용했던 방법
# @api.route('/hello/<string:name>')
# class HelloWorld(Resource):
#     def get(self, name):
#         return {'hello': 'world {}'.format(name)}
# @app.get("/api/account")
# def get_account_all():
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute(SELECT_TABLE_ACCOUNT)
#             data = cur.fetchall()
#     return str(data)
# @app.post("/api/account/add")
# def add_account():
#     data = request.get_json()
#     name = data['name']
#     password = data['password']
#     email = data['email']
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute(INSERT_ACCOUNT_DATA,(name, password, email))
#     return {"message" : "account added."}, 201
  