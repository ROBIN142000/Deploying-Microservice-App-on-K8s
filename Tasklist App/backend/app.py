from flask import Flask, request, jsonify, render_template, session, redirect
from flask_bcrypt import Bcrypt
import requests, os
from todo import csv_or_not, initialize_tasklist, add_task, edit, delete_task, clear_list
from dotenv import load_dotenv

app=Flask(__name__)
load_dotenv("secret/secret.env")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
bycrypt = Bcrypt(app)
load_dotenv("config/config.env")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login.html", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        user_password = request.form.get("password") 
        payload = {"username": username, "password": user_password}
        response = requests.post(f"{os.getenv('auth')}/auth", data=payload)

        if response.status_code == 201:
            session["access_token"] = response.json().get("access_token")
            session["username"] = username
            return redirect("/dashboard.html")
        else:
            return "INVALID CRENDENTIALS", 404
    else:
        return redirect ("/dashboard.html")

@app.route("/signup.html", methods=["POST", "GET"])
def signup_page():
    if request.method == "POST":
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        user_password = bycrypt.generate_password_hash(request.form["password"]).decode('utf-8')

        payload = {"username": username, "name": name, "email": email, "password": user_password}
        response = requests.post(f"{os.getenv('auth')}/signup", data=payload)
        if response.status_code == 200:
            return "Signup Succesful!"
        return "Invalid Signup", 404
    else:
        return render_template("signup.html")
    
@app.route("/dashboard.html", methods=["POST", "GET"])
def dashboard_page():
    if request.method == "POST":
        username = session["username"]
        data = request.get_json()
        action = data["action"]
        token = request.headers.get("Authorization")
        response = requests.post(f"{os.getenv('auth')}/verify", headers={"Authorization": token})
        if not response.status_code == 200:
            return redirect("/login.html")

        if action == "add-task":
            add_task([data["task"], data["time"]], username)
            return jsonify({"isDone": True})
        
        if action == "edit":
            edit(username, data["newTask"],  data["newTime"], data["edit_id"])
            return jsonify({"isDone": True})
        
        if action == "delete-task":
            delete_task(username, data["id"])
            return jsonify({"isDone": True})
        
        if action == "clear":
            clear_list(username)
            return jsonify({"isDone": True})
        
        if action == "logout":
            print("response is ", response.status_code)
            session["access_token"] = ""
            return jsonify({"isDone": True})
    else:
        response = requests.post(f"{os.getenv('auth')}/verify", headers={"Authorization": f"Bearer {session.get('access_token')}"})
        if response.status_code == 200:
            username = session["username"]
            csv_or_not(username)
            taskslist = initialize_tasklist(username)
            taskslist.pop(0)
            return render_template("dashboard.html", tasks=taskslist, username=username, token=session["access_token"])
        
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host=os.getenv("APP_HOST"))