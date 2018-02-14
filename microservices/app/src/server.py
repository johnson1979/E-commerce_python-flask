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


    return render_template("home.html",uname=None,token=None,pdata=pdata,hasura_id=0)


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

        hasura_id=data['hasura_id']
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
                        "hasura_id": hasura_id,
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
        data=json.loads(resp.content.decode("UTF-8"))
        

        return render_template("home.html",uname=uname,token=token,pdata=pdata,hasura_id=hasura_id)

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
        hasura_id=data['hasura_id']
        if token:
            return render_template("home.html",uname=uname,token=token,pdata=pdata,hasura_id=hasura_id)
        return "Invalid credentials"
    return render_template("login.html")

@app.route('/userinfo/<int:hasura_id>')
def userinfo(hasura_id):
    # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "customer",
            "columns": [
                "name",
                "email",
                "phone"
            ],
            "where": {
                "hasura_id": {
                    "$eq": hasura_id
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    return (resp.content)


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

@app.route("/addtocart/<int:hasura_id>/<int:prod_id>")
def addtocart(hasura_id,prod_id):
    # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "cart",
            "columns": [
                "prod_id"
            ],
            "where": {
                "hasura_id": {
                    "$eq": hasura_id
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    pdata=json.loads(resp.content.decode("UTF-8"))
    plist=[]
    status=False
    for p in pdata:
        plist.append(p['prod_id'])


    for i in plist:
        if prod_id is i:
            status=True


    if(status is False):
        # This is the url to which the query is made
        url = "https://data.bloodlessly89.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "cart",
                "objects": [
                    {
                        "prod_id": prod_id,
                        "hasura_id": hasura_id
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
        return "item added to cart"
    else:
        return "sorry!item already added to cart"



@app.route("/cartitems/<int:hasura_id>")
def cartitems(hasura_id):
    # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "cart",
            "columns": [
                "prod_id"
            ],
            "where": {
                "hasura_id": {
                    "$eq": hasura_id
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data=json.loads(resp.content.decode("UTF-8"))
    l=[]
    pid=None
    for id in data:
        pid=id['prod_id']
        l.append(pid)

    # This is the url to which the query is made
    url = "https://data.bloodlessly89.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "product",
            "columns": [
                "name",
                "price",
                "discount",
                "owner"
            ],
            "where": {
                "id": {
                    "$in": l


                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data=json.loads(resp.content.decode("UTF-8"))
    total_price=0
    for p in data:
        total_price+=int(p['price'])


    return render_template("cart.html",data=data,total_price=total_price)

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        name=request.form['search_text']
        search_text=name.strip()
       # This is the url to which the query is made
        url = "https://data.bloodlessly89.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "select",
            "args": {
                "table": "product",
                "columns": [
                    "name"
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        prod_name=json.loads(resp.content.decode('UTF-8'))
        search_prod_items=[]

        for name in prod_name:
            item_name=name['name']
            status=item_name.strip().find(search_text)
            if search_text is "":
                return redirect('/home')
            else:
                if not status is -1 :
                    search_prod_items.append(item_name)

        url = "https://data.bloodlessly89.hasura-app.io/v1/query"
        requestPayload = {
        "type": "select",
        "args": {
            "table": "product",
            "columns": [
                "name",
                "price",
                "discount",
                "owner"
            ],
            "where": {
                "name": {
                    "$in": search_prod_items


                }
            }
        }
    }

    # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data=json.loads(resp.content.decode("UTF-8"))
        return resp.content

    return redirect('/home')


