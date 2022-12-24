from flask import request
from flask_restx import Resource, Namespace, fields
import os
import psycopg2 as pg2
from dotenv import load_dotenv

SELECT_TABLE_ACCOUNT = (
    "SELECT * FROM test;"
)

INSERT_ACCOUNT_DATA = ("""
    INSERT INTO test(username,password,email,create_on)
    VALUES 
    (%s,%s,%s,CURRENT_TIMESTAMP)
""")

DELETE_ACCOUNT_DATA = ("""
    DELETE FROM test 
    WHERE username = %s
    RETURNING username;
""")

Ele_server = Namespace('Ele_server')

account_field = Ele_server.model('Account_Input', { 
    'username': fields.String(description='User name or ID', required=True, example="jinseongbe"),
    'password': fields.String(description='password, just for study', required=True, example="0123456df!!"),
    'email': fields.String(description='Email address', required=True, example="jinsengbe@gmail.com")
})

account_delete_field = Ele_server.model('Account_Delete', { 
    'username': fields.String(description='username to delete', required=True, example="jinseongbe"),
})

account_all_field = Ele_server.model('Account_All', { 
"result": fields.String("[(1, 'Jose', 'password', 'jose@mail.com', datetime.datetime(2022, 12, 21, 18, 5, 12, 863584), datetime.datetime(2022, 12, 21, 18, 22, 15, 351067)), (2, 'Jose2', 'passwor2sdfd', 'jossfee@mail.com', datetime.datetime(2022, 12, 23, 12, 59, 12, 350507), None), (5, 'park', 'asjkdfhuiwef', 'asdkjfue@naver.com', datetime.datetime(2022, 12, 23, 13, 6, 36, 459872), None), (6, 'asdfhue', 'asjsfhukdfhuiwef', 'weiuhjsdfe@naver.com', datetime.datetime(2022, 12, 23, 13, 6, 58, 278858), None), (9, 'someone1', 'asdkjfhuw', 'asfdhhue@naver.com', datetime.datetime(2022, 12, 23, 16, 37, 27, 751588), None), (11, 'someone2', 'asdkjfhuw', 'asfdfedhhue@naver.com', datetime.datetime(2022, 12, 23, 16, 37, 36, 86160), None), (12, 'someone3', 'asdkjfhuw', 'sfedhhue@naver.com', datetime.datetime(2022, 12, 23, 16, 37, 42, 794429), None)]")
})

db_url = os.getenv("CLOUD_DB_URL")
db_password = os.getenv("CLOUD_DB_PASSWORD")
conn = pg2.connect(db_url, password=db_password)



@Ele_server.route('')
class Test(Resource):
    def get(self):
        """ele_server account 전체목록을 불러옵니다."""
        with conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_TABLE_ACCOUNT)
                data = cur.fetchall()
        return {'result': str(data)}
    def post(self):
        """ele_server account를 추가합니다"""
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']

        with conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_ACCOUNT_DATA,(username, password, email))
        return {"message" : "account added."}, 201

    def delete(self):
        """ele_server account 삭제합니다."""
        data = request.get_json()
        username = data['username']

        with conn:
            with conn.cursor() as cur:
                cur.execute(DELETE_ACCOUNT_DATA,(username,))
                deleted_username = cur.fetchall()
        return {"message": "delete account data username = {}, {}".format(username, deleted_username)}, 201

