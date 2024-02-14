from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import mysql.connector, os
from dotenv import load_dotenv
from datetime import timedelta

app = Flask(__name__)
load_dotenv(dotenv_path="secret/secret.env")
DATABASE = os.getenv("DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

load_dotenv(dotenv_path="config/config.env")
jwt = JWTManager(app)
bycrypt = Bcrypt(app)

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": DB_USERNAME,
    "password": DB_PASSWORD,
    "database": DATABASE
}

@app.route("/", methods=["POST", "GET"])
def index():
    return "auth running"

@app.route("/auth", methods=["POST"])
def auth():
    if request.method == "POST":
        username = request.form.get("username")
        user_password = request.form.get("password")

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data and bycrypt.check_password_hash(user_data[4], user_password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 201
    
        return "Invalid Credentials", 404
    
@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        db=mysql.connector.connect(**db_config)
        cursor = db.cursor()

        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        user_password = request.form.get("password")

        try:
            cursor.execute(
                    "INSERT INTO users (username, name, email, user_password) VALUES(%s,%s,%s,%s)",
                    (username, name, email, user_password)
                )
            db.commit()
            cursor.close()
            return "signup successful", 200
        except:
            return "Invalid Signup", 404
        
@app.route("/verify", methods=["POST", "GET"])
@jwt_required()
def verify():
    if request.method == "POST":
        current_user = get_jwt_identity()
        return jsonify({"message": "Token is valid", "user": current_user}), 200
    else:
        return jsonify({"message": "Welcome to the verification endpoint"}), 200
    
if __name__ == "__main__":
    app.run(debug=True, port=8000, host=os.getenv("APP_HOST"))

