from flask import Flask,jsonify,request
import subprocess
import sys
import rateCalculation2
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
    #r = subprocess.Popen([sys.executable,'rateCalculation.py',data], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    datar = rateCalculation2.main(data)#r.communicate()
    return jsonify(datar)

#get /users
@app.route('/users')
def get_useres():
  return jsonify(db.GetUsers())

#get /restaurants
@app.route('/restaurants')
def get_restaurants():
  return jsonify(db.GetRestaurants())

#post /userupdate data: {name :}
@app.route('/user/<string:userid>/update' , methods=['POST'])
def update_user(userid):
  request_data = request.get_json()
  db.updateUserPreferences(userid, preferences=request_data)
  return "200 ok"

#post /userupdatepreviously data: {name :}
@app.route('/user/<string:userid>/updatepreviously' , methods=['POST'])
def update_previously_liked(userid):
  request_data = request.get_json()
  db.UpdateUserPreviouslyLiked(userid, request_data)
  return "200 ok"

if __name__ == '__main__':
    app.run(port=5000)
