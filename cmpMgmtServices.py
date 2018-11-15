from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

#uncomment to run on coaf dev connect rds on coaf dev
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flagship:123123@hammerdevdb-coaf.ccr6zchg1pp7.us-east-1.rds.amazonaws.com:5432/flagship'
engine = create_engine('postgresql://flagship:123123@hammerdevdb-coaf.ccr6zchg1pp7.us-east-1.rds.amazonaws.com:5432/flagship')

from views import *

if __name__ == '__main__':
       app.secret_key = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
       app.run( debug=True)
