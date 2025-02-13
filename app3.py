# # sqlite  it is RDBMS software
# #sqlalchemy   this is one toolkit ehich allows to perform crud operations without worrying about sql queries
# #ORM   Object Relational Mapping
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# app=Flask(_name_)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"   #to tell flask about location of database
# db = SQLAlchemy(app)  #connection between db and app
#  #SQLITE it is an rdbms software which will store your data 
# #tell schema to database  whether name is in which form eg name in string
# class Student(db.Model):
#     _tablename_="studentsList"   #this will define name of table 
#     roll_no=db.Column(db.Integer,primary_key=True) #primary_key will generate numbers automatically
#     name=db.Column(db.String(100))
#     email=db.Column(db.String(100))
#     address=db.Column(db.String(100))
#     def _init_(self,name,email,address):
#         self.name=name
#         self.email=email
#         self.address=address
#     def _repr_(self):
#         return f"Student name is {self.name} and Student email is {self.email} and Student address is {self.address}"    #printing data in terminal
# with app.app_context():  #we have opened the window of database here
#     db.create_all()   #this will form tables
#     student1=Student("Arshia","arshiamahajan@gmail.com","Dharamshala")
#     student2=Student("Aaru","aarushmahajan@gmail.com","Dharamshala")
#     # db.session.add(student1)   #to add data in table yh wala db ka session hai poorane wala nahi 
#     db.session.add_all([student1,student2])   #here we are adding students in the database

#     db.session.commit()



#authentication
# it is the process of verifying user identity 
#this will check whether user is authenticated to visit website or 
#inside authentication following steps are included
#1.Sign up
#2 login
#3password hashing
#4 session management 
#authentication is the process of granting access to the user for particular routes according to their role.
# from flask import Flask,render_template,request,url_for,redirect,flash
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash,check_password_hash
# app=Flask(_name_)
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
# @app.route("/")
# def home():
#     return render_template("base.html")
# db=SQLAlchemy(app)
# class User(db.Model):
#     _table_="users"
#     id =db.Column(db.Integer,primary_key=True)
#     username =db.Column(db.String(100))
#     email=db.Column(db.String(100))
#     password_hash = db.Column(db.String(200))
#     role=db.Column(db.String(100),default="user")
    

#     #for saving hash password #123
#     def save_hash_password(self,password):
#         self.password_hash=generate_password_hash(password)
#         #we are generating encrypted password here
#     def check_hash_password(self,password):
#         return check_password_hash(self.password_hash,password)
#     #this will return true or false according to user credential

# @app.route("/register")
# def register():
#     if request.method=="POST":
#         username=request.form.get("username")
#         email=request.form.get("email")
#         password=request.form.get("password")
#         role=request.form.get("role")
#         if User.query.filter_by(email=email).first():
#             flash("User Already exists")
#             return redirect(url_for("home"))
#         user_data=User(username=username,email=email,role=role)
#         user_data.save_hash_password(password)
#         db.session.add(user_data)
#         db.session.commit()
#         flash("User registered successfully")
#         return(redirect(url_for("login")))

#     return render_template("signup.html")
# @app.route("/login")
# def login():
#     return render_template("login.html")
# if(_name=="main_"):
#     app.run(debug=True)













#authentication
#1 signup
#2 login
#3 password hashing
#4 session management

#authorization
#authorization is the process of granting access to user 
#for particular routes according to their role
from flask import Flask,render_template,redirect,request,url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,logout_user,UserMixin,login_required
#flask-login---->session
#flask login library is used for better session management

from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SECRET_KEY"]="welcome"
db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)   #we are linking our app with flask-manager
login_manager.login_view=("login")    #if user is not logged in then he will direct to this page

@app.route("/")
def home():
    return render_template("base.html")
#usermixin will provide you additional methods like is_authenticated, is_active,get_id
#is_authenticated will return true if user is logged in 
#is_active will return true when user is in session
#get_id    will  return user_id
class User(db.Model,UserMixin):
    _tablename_="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password_hash=db.Column(db.String(100))
    role=db.Column(db.String(100),default="user")

    def save_hash_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_hash_password(self,password):
        return check_password_hash(self.password_hash,password)    


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        role=request.form.get("role")

        if User.query.filter_by(email=email).first():
            flash("User Already exists")
            return redirect(url_for("home"))

        user_data=User(username=username,email=email,role=role)
        user_data.save_hash_password(password)

        db.session.add(user_data)
        db.session.commit()
        flash("USer registered successfully")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        role=request.form.get("role")

        user_data=User.query.filter_by(email=email,role=role).first()
        #hashed password =original_database_hash_password
        if user_data and user_data.check_hash_password(password):
            login_user(user_data)   #storing user object in session
            flash("user login successfully")
            return redirect(url_for("dashboard"))



            


    return render_template("login.html")
#user loader function to fetch current user data from database 
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(user_id)   #this will fetch user id from the session and retrieve current object from the data base

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")

with app.app_context():
    db.create_all()


if __name__=="__main__":
    app.run(debug=True)



