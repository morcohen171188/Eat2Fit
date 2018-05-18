from flask import Flask,jsonify,request
import subprocess
import sys
import dbHandler


app = Flask(__name__)

db = dbHandler.dbHandler()

@app.route('/')
def home():
    pass

#post /user data: {name :}
@app.route('/user' , methods=['POST'])
def create_user():
  request_data = request.get_json()
  return db.SaveNewUserPreferences(user_data=request_data)

#get /restaurant/<name> data: {name :}
@app.route('/restaurant/<string:data>')
def get_recommended_dishes(data):
    r = subprocess.Popen([sys.executable,'rateCalculation.py',data], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    datar = r.communicate()
    return datar

#get /users
@app.route('/users')
def get_stores():
  return jsonify(db.GetUsers())
  #pass

#post /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
  request_data = request.get_json()


if __name__ == '__main__':
    app.run(port=5000)
