from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import os

load_dotenv()
app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
uri = os.getenv("URI")

client=MongoClient(uri, server_api=ServerApi('1'))
db=client["contact_manager"]
contact=db["contact"]

@app.route("/", methods=["POST","GET"])
def index():
    if request.method=="POST":
        name_in=request.form.get("name")
        number_in = request.form.get("number")

        if not name_in or len(name_in) < 3:
            flash("Name cannot have less than 3 characters.")
            return redirect("/")

        if not number_in.isdigit():
            flash("Phone number must contain only digits.")
            return redirect("/")

        contact.insert_one({"name": name_in, "number": number_in})
        flash("Contact saved successfully!")
        return redirect("/")

    elif request.method=="GET":
        contacts=list(contact.find())
        return render_template("index.html", contacts=contacts)

@app.route("/delete/<contact_id>")
def delete_contact(contact_id):
    if request.method == "GET":
        del_contact=contact.delete_one({"_id": ObjectId(contact_id)})
        return redirect("/")

if __name__=="__main__":
    app.run(debug=True)