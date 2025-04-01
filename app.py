from flask import Flask

from get_token import get_access_token
from get_company import get_companies_access

from pushitem import push_item_info
from dotenv import load_dotenv

import cx_Oracle 
import os
#2

app = Flask(__name__)

load_dotenv()
access_token = get_access_token() 
company_id=get_companies_access(access_token)
push_item_info(access_token,company_id)


@app.route('/')
def item():
   return push_item_info(access_token,company_id)





if __name__ == '__main__':
    app.run(debug=True)


#@app.route('/company')
