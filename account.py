from flask import request
from flask_restx import Resource, Namespace, fields
import os
import psycopg2 as pg2
from dotenv import load_dotenv

SELECT_TABLE_ACCOUNT = (
    "SELECT * FROM account;"
)

INSERT_ACCOUNT_DATA = ("""
    INSERT INTO account(username,password,email,create_on)
    VALUES 
    (%s,%s,%s,CURRENT_TIMESTAMP)
""")

DELETE_ACCOUNT_DATA = ("""
    DELETE FROM account 
    WHERE username = %s
""")

load_dotenv()
db = os.environ.get("DB")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
conn = pg2.connect(database=db, user=db_user, password=db_pass)

# 실제 서비스를 배포할때는 DB와 WAS를 분리해야 하기 때문에 아래 코드를 사용한다.
# db_url = os.getenv("DB_URL")
# conn = pg2.connect(db_url)


Test_account = Namespace('Test_account')

account_field = Test_account.model('Account_Input', { 
    'username': fields.String(description='User name or ID', required=True, example="jinseongbe"),
    'password': fields.String(description='password, just for study', required=True, example="0123456df!!"),
    'email': fields.String(description='Email address', required=True, example="jinsengbe@gmail.com")
})

account_delete_field = Test_account.model('Account_Delete', { 
    'username': fields.String(description='username to delete', required=True, example="jinseongbe"),
})

account_all_field = Test_account.model('Account_All', { 
"result": fields.String("[(1, 'Jose', 'password', 'jose@mail.com', datetime.datetime(2022, 12, 21, 18, 5, 12, 863584), datetime.datetime(2022, 12, 21, 18, 22, 15, 351067)), (2, 'Jose2', 'passwor2sdfd', 'jossfee@mail.com', datetime.datetime(2022, 12, 23, 12, 59, 12, 350507), None), (5, 'park', 'asjkdfhuiwef', 'asdkjfue@naver.com', datetime.datetime(2022, 12, 23, 13, 6, 36, 459872), None), (6, 'asdfhue', 'asjsfhukdfhuiwef', 'weiuhjsdfe@naver.com', datetime.datetime(2022, 12, 23, 13, 6, 58, 278858), None), (9, 'someone1', 'asdkjfhuw', 'asfdhhue@naver.com', datetime.datetime(2022, 12, 23, 16, 37, 27, 751588), None), (11, 'someone2', 'asdkjfhuw', 'asfdfedhhue@naver.com', datetime.datetime(2022, 12, 23, 16, 37, 36, 86160), None), (12, 'someone3', 'asdkjfhuw', 'sfedhhue@naver.com', datetime.datetime(2022, 12, 23, 16, 37, 42, 794429), None)]")
})


@Test_account.route('')
class Account(Resource):
    @Test_account.response(201, 'Success', account_all_field)
    def get(self):
        """account 전체목록을 불러옵니다."""
        with conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_TABLE_ACCOUNT)
                data = cur.fetchall()
        return {'result': str(data)}
    
    @Test_account.expect(account_field)
    @Test_account.response(201, 'Success')
    def post(self):
        """account를 추가합니다"""
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']

        with conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_ACCOUNT_DATA,(username, password, email))
        return {"message" : "account added."}, 201

    @Test_account.expect(account_delete_field)
    @Test_account.response(201, 'Success')
    def delete(self):
        """account 삭제합니다."""
        data = request.get_json()
        username = data['username']

        with conn:
            with conn.cursor() as cur:
                cur.execute(DELETE_ACCOUNT_DATA,(username,))
        return {"message": "delete account data username = {}".format(username)}, 201

