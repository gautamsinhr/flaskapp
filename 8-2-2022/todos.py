# from werkzeug.utils import secure_filename
# https://uniwebsidad.com/libros/explore-flask/chapter-12/forgot-your-password 


from flask import Flask, render_template,request,redirect,session,current_app,flash,url_for
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from random import randint
import os
import secrets
from flask_wtf import FlaskForm
from markupsafe import string 
from wtforms import  PasswordField,EmailField,Form
from wtforms.validators import DataRequired, Length, Email 

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/todolist'
db = SQLAlchemy(app)


class register(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10),unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    hashCode = db.Column(db.String(120))
    

class tododata(db.Model):
    sno=db.Column(db.Integer ,primary_key = True)
    tital = db.Column(db.String(100))
    date = db.Column(db.String(20))
    usr = db.Column(db.String(20))
    file = db.Column(db.String(100))






app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rajputgautamsinh123@gmail.com'
app.config['MAIL_PASSWORD'] = 'nlwiwqnpfyignylf' 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

otp=randint(000000,999999) 

mail = Mail(app)


def saveimg(photo):
    hash_photo = secrets.token_urlsafe(10)
    _,file_ecxtetion = os.path.splitext(photo.filename)
    photo_name = hash_photo+file_ecxtetion
    file_path = os.path.join(current_app.root_path,'static/',photo_name)
    photo.save(file_path)
    return photo_name



@app.route('/',methods=['POST','GET'])
def registerdata():
    if (request.method=="POST"):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user= register.query.filter_by(username=username).first()

        if user:
            flash('User Alredy Exists Enter Onther One')
        else:    
            con = register(username=username,email=email,password=password)
            db.session.add(con)
            db.session.commit()
            

            msg=Message(subject='OTP',sender='rajputgautamsinh123@gmail.com',recipients=['makwanagautam199@gmail.com'])
            msg.body=str(otp)
            mail.send(msg)
    
            return render_template('verify.html')
    return render_template('reg.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add',methods=['GET','POST'])
def addval():
    if request.method=="POST":
        # session.pop('name', None) 
        username = request.form.get('username')
        password = request.form.get('password')

        user = register.query.filter_by(username=username,password=password).first()
 
        if user is not None:
            db.session.add(user)
            db.session.commit()
            session["name"] = username
            return redirect('/home')
        else:
            return redirect('/')

                

@app.route('/home',methods=['GET','POST'])

def home():
    if not session.get("name"):
        return redirect("/login")
    else:    
        if request.method=="POST":
          
            
            tital = request.form.get('tital')
            img = saveimg(request.files.get('photo'))
            # usr = register.query.filter_by(username=session["name"]).first()
            usr = (session['name'])
            # print(u,'-------------------------------------------------------------iejjeeeeeeeeeeeeeeeeeeeeeeeee')

            # data = request.form.get('username')

            # file = request.files['file']
            # file.save(os.path.join(current_app.root_path,'/static',secure_filename(file.filename)))
            
            # file.save(secure_filename(file.filename))
            # id = register.query.get("username")
            # user = register.query.filter_by(username=session['name']).first()

            con = tododata(tital=tital,file=img,usr=usr,date=datetime.now())

            db.session.add(con)
            db.session.commit()
         
            msg = Message(
                'Hello',
                sender ='rajputgautamsinh123@gmail.com',
                recipients = ['makwanagautam199@gmail.com']
               )
            msg.body = 'Hello , Todo Add From : ' +usr +",  And Tital Is : " +tital  
            # msg.body=str(otp)
            # msg.attach ("File Name", "Type", read files)
            with app.open_resource("static/pop.png") as fp:
                msg.attach("pop.png", "image/png", fp.read())
            mail.send(msg)
            return redirect('/home')
        
        u = register.query.filter_by(username=session["name"]).first()
        con = tododata.query.filter_by(usr=session["name"])
        print(con,'dsdsdnsndjsdnn')
       
        return render_template('home.html',con=con,u=u)
    


@app.route('/delete/<int:id>')
def deletedata(id):
    deldata = tododata.query.filter_by(sno=id).first()
    db.session.delete(deldata)
    db.session.commit()
    return redirect('/home')



@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=="POST":
        tital = request.form['tital']
        updata = tododata.query.filter_by(sno=id).first()
        updata.tital= tital
        db.session.add(updata)
        db.session.commit()
        return redirect('/home')

    data = tododata.query.filter_by(sno=id).first() ## existing value show in update page 
    return render_template('update.html',data=data)



"""  varify otp validate or not check """

# @app.route('/verify',methods=['GET',"POST"])
# def verify():
  
#     msg=message(subject='OTP',sender='rajputgautamsinh123@gmail.com',recipients=['makwanagautam199@gmail.com'])
#     msg.body=str(otp)
#     mail.send(msg)
#     return render_template('verify.html')

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        # flash("otp is right")
        return redirect('/login')
    return "Please Try Again"




@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('name', None)
   
    return redirect('/')        
   



import random
@app.route('/forgot',methods=["POST","GET"])
def index():
    if request.method=="POST":
        username = request.form['username']
        check = register.query.filter_by(username=username).first()

        if check:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'rajputgautamsinh123@gmail.com', recipients = ['makwanagautam199@gmail.com'])
            msg.body = '''Hello,\nWe've received a request to reset your password. If you want to reset your password,
             click the link below and enter your new password\n http://localhost:5000/''' + check.hashCode
            mail.send(msg)
            return '''
                <form action="/forgot" method="post">
                    <small>enter the uername of the account you forgot your password</small> <br>
                    <input type="text" name="username" id="mail" placeholder="username"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return '''
            <form action="/forgot" method="post">
                <small>enter the username of the account you forgot your password</small> <br>
                <input type="text" name="username" id="mail" placeholder="username"> <br>
                <input type="submit" value="Submit">
            </form>
        '''
  
@app.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = register.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('index'))
            else:
                
                return '''
                    <form method="post">
                        <small>enter your new password</small> <br>
                        <input type="password" name="passw" id="passw" placeholder="password"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                        <input type="submit" value="Submit">
                    </form>
                '''
        else:
            return '''
                <form method="post">
                    <small>enter your new password</small> <br>
                    <input type="password" name="passw" id="passw" placeholder="password"> <br>
                    <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return render_template('/')



app.run(debug=True, port=8000)







