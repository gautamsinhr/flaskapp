

from flask import Flask, render_template,request,redirect,session,g
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from flask_mail import Mail, Message


# from flask_login import login_required, current_user

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/todolist'
mail = Mail(app)
db = SQLAlchemy(app)


class register(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10),unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    

class tododata(db.Model):
    sno=db.Column(db.Integer ,primary_key = True)
    tital = db.Column(db.String(100))
    date = db.Column(db.String(20))


# 



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rajputgautamsinh123@gmail.com'
app.config['MAIL_PASSWORD'] = '' 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True




@app.route('/home',methods=['GET','POST'])
def home():
    if not session.get("name"):
        return redirect("/login")
    else:    
        if request.method=="POST":
            tital = request.form.get('tital')

            con = tododata(tital=tital,date=datetime.now())

            db.session.add(con)
            db.session.commit()
            mail.send_message('New mail ' , tital,
                                sender = 'rajputgautamsinh123@gmail.com',
                                recipients=['makwanagautam199@gmail.com'],
                                body = "this is coustem msg"
                                )
         
        con = tododata.query.all()
        u = register.query.all()
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



@app.route('/',methods=['POST','GET'])
def registerdata():
    if (request.method=="POST"):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        con = register(username=username,email=email,password=password)
        db.session.add(con)
        db.session.commit()


    return render_template('reg.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add',methods=['GET','POST'])
def addval():
    if request.method=="POST":
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

                


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('name', None)
   
    return redirect('/')        
   
    





    




app.run(debug=True)







