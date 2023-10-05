import sqlalchemy
import flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from project_orm import User
from flask import Flask,session,flash,redirect,render_template,url_for
from utils import *
from flask.globals import request
from main import camera
from ParkingSpacePicker import editor

app=Flask(__name__)
app.secret_key="The basics of life with python"

def get_db():
    engine = create_engine('sqlite:///database.sqlite')
    Session = scoped_session(sessionmaker(bind=engine))
    return Session()
  

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        if email and validate_email(email):
            if password and len(password)>=6:
                try:
                    sess = get_db()
                    user = sess.query(User).filter_by(email=email).first()

                    if user and user.password == password:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        session['name'] = user.name
                        del sess
                        flash('login successfull','success')
                        return redirect('/home')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
    return render_template('index.html',title='login')
    
@app.route("/signup",methods=["GET","POST"]) 
def signup():
    if request.method=="POST":
        name=request.form.get("name") 
        email=request.form.get("email")
        password=request.form.get("password")
        cpassword=request.form.get("cpassword") 
        print(name, email, password, cpassword)        
        if name and len(name) >= 3:
            if email and validate_email(email):
                if password and len(password)>=6:
                    if cpassword and cpassword == password:
                        try:
                            sess = get_db()
                            print(sess)
                            newuser = User(name=name,email=email,password=password)
                            print(newuser)
                            sess.add(newuser)
                            sess.commit()
                            del sess
                            flash('registration successful','success')
                            return redirect('/')
                        except Exception as e:
                            print(e)
                            flash('email account already exists','danger')
                    else:
                        flash('confirm password does not match','danger')
                else:
                    flash('password must be of 6 or more characters','danger')
            else:
                flash('invalid email','danger')
        else:
            flash('invalid name, must be 3 or more characters','danger')
    return render_template('signup.html',title='register')

@app.route("/home",methods=["GET","POST"])
def home():
    return render_template("home.html",title="home")
    
@app.route("/contact",methods=["GET","POST"])
def contact():
    return render_template("contact.html",title="forgot password")

@app.route("/about")
def about():
    return render_template("about.html",title="About us")
    
@app.route("/logout")
def logout():
    if session.get('isauth'):
        session.clear()
        flash('you have been logged out','warning')
    return redirect("/home")

@app.route('/launch/camera')
def launch_camera():
    camera()
    return redirect('/home')

@app.route('/launch/editor')
def launch_editor():
    editor()
    return redirect('/home')

if __name__=="__main__":
    app.run(debug=True)