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
def get_useres():
  return jsonify(db.GetUsers())
  #pass

#get /restaurants
@app.route('/restaurants')
def get_restaurants():
  return "smadar:32.442244:34.915156"
  #pass


#post /userupdate data: {name :}
@app.route('/user/<string:userid>/update' , methods=['POST'])
def update_user(userid):
  request_data = request.get_json()
  db.updateUserPreferences(userid, preferences=request_data)
  return "200 ok"


if __name__ == '__main__':
    app.run(port=5000)
