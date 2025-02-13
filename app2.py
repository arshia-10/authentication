from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"   #to tell flask about location of database
# app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False     optional telling sqlalchemy tool to do not store db activities because it will consume some space
db = SQLAlchemy(app)
class Student(db.Model):
    __tablename__="studentsList"   #this will define name of table 
    roll_no=db.Column(db.Integer,primary_key=True) #primary_key will generate numbers automatically
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    address=db.Column(db.String(100))
    marks=db.Column(db.Integer)
    def __init__(self,name,email,address,marks):
        self.name=name
        self.email=email
        self.address=address
        self.marks=marks
    def __repr__(self):
        return f"Student: {self.roll_no},{self.name},{self.email},{self.address},{self.marks}"
@app.route("/")
def home():
    return render_template("home.html",users=Student.query.all())

@app.route("/formSubmit",methods=["GET","POST"])
def submitFunction():
    if request.method=="POST":
        name=request.form.get("user-name")
        email=request.form.get("user-email")
        address=request.form.get("user-address")
        marks=request.form.get("user-marks")
        user=Student(name,email,address,marks)
        # {name="Arshia",email="arshiamahajan@gmail.com",address="Dharamshala"}
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
@app.route("/delete/<int:roll_number>")
def deleteFunction(roll_number):
    user=db.session.get(Student,roll_number)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return "No user found "
@app.route("/update/<int:roll_number>",methods=["GET","POST"])
def updateFunction(roll_number):
    user=db.session.get(Student,roll_number)
    if request.method=="POST":
        user.name=request.form.get("user-name")
        user.email=request.form.get("user-email")
        user.address=request.form.get("user-address")
        user.marks=request.form.get("user-marks")
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("updateForm.html",data=user)

#CRUD 
#__repr__  it will be automatically called itself when u call the class
with app.app_context():
    db.create_all()
    # data=Student.query.all()#this will return all the data present in database (Read operation )
    # for Student in data:
    #     print(Student.roll_no,Student.name,Student.email,Student.address)
    # print(data)   second way to access the data
    #filters 
    #
    # Student3=Student.query.get(2)  #if the number data is not present it will give none as in place of 2 ill write 12 it will give error
    # print(Student3)
    data_marks=Student.query.filter_by(marks=0).all()
    data_address=Student.query.filter_by(address="dharamshala").all()
    data_address1=Student.query.filter_by(address="dharamshala").first() #give the first address
    #filter and filterby
    # print(data_address1)
    # marks_0=Student.query.filter(Student.marks>0).all()
    # print(marks_0)
    # filter_by_more_conditions=Student.query.filter(Student.marks>7,Student.address=="dharamshala").all()
    # print(filter_by_more_conditions)


    #update
    # update_user=db.session.get(Student,3)
    # update_user.name="Shauraya Vohra"
    # update_user.email="shaurayooo@gmail.com"
    # db.session.add(update_user)
    # db.session.commit()
    # print(Student.query.all)



    #delete 
    delete_user=db.session.get(Student,4)
    if delete_user:
        db.session.delete(delete_user)
        db.session.commit()
    print(Student.query.all())
if __name__=="__main__":
    app.run(debug=True)

