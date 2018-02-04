from src import app
from flask import Flask,render_template,request,redirect
import requests
import json



@app.route("/")
@app.route("/home")
def home():
        # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "product",
            "columns": [
                "*"
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    pdata=json.loads(resp.content.decode("UTF-8"))
    return render_template("home.html",token=None,uname=None,pdata=pdata)


@app.route("/signup",methods=['GET','POST'])
def signup():
            # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "product",
            "columns": [
                "*"
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    pdata=json.loads(resp.content.decode("UTF-8"))



    if request.method=="POST":
        uname=request.form["uname"]
        email=request.form["email"]
        phone=request.form["phone"]
        password=request.form["password"]

        # This is the url to which the query is made
        url = "https://auth.bloodlessly89.hasura-app.io/v1/signup"

        # This is the json payload for the query
        requestPayload = {
            "provider": "username",
            "data": {
                "username": uname,
                "password": password
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data=json.loads(resp.content.decode("UTF-8"))
        id=data['hasura_id']
        token=data['auth_token']
        # This is the url to which the query is made
        url = "https://data.bloodlessly89.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "customer",
                "objects": [
                    {
                        "hasura_id": id,
                        "name": uname,
                        "email": email,
                        "phone": phone
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)


        return render_template("home.html",uname=uname,token=token,pdata=pdata)

    return render_template("signup.html")




@app.route("/login" ,methods=["GET","POST"])
def login():
            # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "product",
            "columns": [
                "*"
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    pdata=json.loads(resp.content.decode("UTF-8"))

    if request.method=="POST":
        uname=request.form["uname"]
        password=request.form["password"]
        # This is the url to which the query is made
        url = "https://auth.bloodlessly89.hasura-app.io/v1/login"

        # This is the json payload for the query
        requestPayload = {
            "provider": "username",
            "data": {
                "username": uname,
                "password": password
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        data=json.loads(resp.content.decode("UTF-8"))

        token=data['auth_token']
        return render_template("home.html",uname=uname,token=token,pdata=pdata)
    return render_template("login.html")

@app.route("/logout/<string:token>")
def logout(token):
        # This is the url to which the query is made
    url = "https://auth.bloodlessly89.hasura-app.io/v1/user/logout"

    # This is the json payload for the query
    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, headers=headers)


    return redirect("/home")

@app.route("/addtocart")
def addtocart():
    return "added to cart ~/"


if __name__=="__main__":
    app.run(debug=True)


