from flask import request
from flask_restx import Resource, Api, Namespace
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

@Test_account.route('')
class Account(Resource):
    def get(self):
        with conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_TABLE_ACCOUNT)
                data = cur.fetchall()
        return {'result': str(data)}
    
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']

        with conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_ACCOUNT_DATA,(username, password, email))
        return {"message" : "account added."}, 201

    def delete(self):
        data = request.get_json()
        username = data['username']

        with conn:
            with conn.cursor() as cur:
                cur.execute(DELETE_ACCOUNT_DATA,(username,))
        return {"message": "delete account data username = {}".format(username)}, 201

