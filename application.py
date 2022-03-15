from time import localtime, strftime
from flask import Flask, redirect, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from wtf_forms import *
from models import *


#app configuration

app = Flask(__name__)
app.secret_key = 'change later'

#database configuration

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://wbgnnveatjnsde:894f6ce4f88140825841cbeb5de35e19626da8ebf68aaf0cb3ded6d4b5e23d14@ec2-54-195-246-55.eu-west-1.compute.amazonaws.com:5432/d9a54c0fpo75bo'

db = SQLAlchemy(app)

#intialize flask-socketio
socketio = SocketIO(app)

# rooms for chat
ROOMS = ["lounge", "basketball", "music", "parties"]

# flask login configuration 
login = LoginManager (app)
login.init_app (app)

@login.user_loader
def load_user(id):
    
   return User.query.get(int(id))

@app.route( "/", methods=['GET' , 'POST'])
def index(): 

    rego_form = RegistrationForm()
    if rego_form.validate_on_submit():
        username = rego_form.username.data
        password = rego_form.password.data

        #adding user to the database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template ("index.html", form= rego_form)

@app.route("/login", methods=['Get', 'POST'])
def login():

    login_form = loginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    
    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
def chat():
  #  if not current_user.is_authenticated:
   #     return "Log in, before chatting"

    return render_template('chat.html', username=current_user.username, rooms=ROOMS )

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    return " Logged out, see you soon :)"

@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])

@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data ['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data ['username'] + " has left the " + data['room'] + " room."}, room=data['room'])




if __name__ == '__main__':
    socketio.run(app, debug=True)  