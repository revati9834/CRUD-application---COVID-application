

#      MongoDb crud Application

# For flask implementation  
from flask import Flask, render_template,request,redirect,url_for 
# For ObjectId to work
from bson  import ObjectId   
from pymongo import MongoClient  
import os  
  
app = Flask(__name__)  
title = "Vaccine Availability "  
heading = "Store Vaccination slots information"  
  


#host uri
client = MongoClient("mongodb://127.0.0.1:27017")  
#Select the database  
db2 = client.mymongodb    
#Select the collection name                          
users = db2.user 

def redirect_url():  
    #redirect
    return request.args.get('next') or request.referrer or url_for('index')  

@app.route("/list")  
def lists ():  
    #List all users
    users_list = users.find()  
    status_list="active"  
    status_info=" "
    return render_template('list.html',users=users_list,t=title,h=heading)

@app.route("/")
def index():
    #Display user addition form
    status_info="active"
    status_list=" "
    return render_template('index.html')

@app.route("/action", methods=['POST'])  
def action ():  
    #Adding a user 
    VaccineCenterName=request.values.get("VaccineCenterName")  
    VaccineName=request.values.get("VaccineName")  
    Availability=request.values.get("Availability")
    Age=request.values.get("Age") 
    Website=request.values.get("Website")
    users.insert({ "VaccineCenterName":VaccineCenterName, 
                   "VaccineName":VaccineName, 
                   "Availability": Availability, 
                   "Age":Age,
                   "Website":Website
                   })  
    return redirect("/list")  

@app.route("/remove")  
def remove ():  
    #Deleting a user with various references  
    key=request.values.get("_id")  
    users.remove({"_id":ObjectId(key)})  
    return redirect("/list")  

@app.route("/update")  
def update ():  
    id=request.values.get("_id")  
    user=users.find({"_id":ObjectId(id)})  
    return render_template('update.html',users=user,h=heading,t=title)

@app.route("/home")  
def home ():    
    return render_template('home.html',h=heading,t=title)


@app.route("/action3", methods=['POST'])  
def action3 ():  
    #Updating a user with various references  
    VaccineCenterName=request.values.get("VaccineCenterName")  
    VaccineName=request.values.get("VaccineName")  
    Availability=request.values.get("Availability")
    Age=request.values.get("Age") 
    Website=request.values.get("Website")
    id=request.values.get("_id")  
    users.update({"_id":ObjectId(id)},
         {'$set':{ "VaccineCenterName":VaccineCenterName, 
                   "VaccineName":VaccineName, 
                   "Availability": Availability, 
                   "Age":Age,
                   "Website":Website}})  
    return redirect("/list")    

@app.route("/search", methods=['GET'])  
def search():  
    #Searching a user with various references  
    key=request.values.get("key")  
    refer=request.values.get("refer")  
    users_list = users.find({refer:key})  
    return render_template('searchlist.html',users=users_list,t=title,h=heading)


if __name__ == "__main__":  
  
    app.run(host='127.0.0.1',port=5002,debug=True)  
