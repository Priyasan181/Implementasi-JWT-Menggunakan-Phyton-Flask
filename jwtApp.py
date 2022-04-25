from flask import Flask
from flask import make_response
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_url_path='/static')

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "myjwtsecretkey"  
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
jwt = JWTManager(app)
account = {
    "username": "admin01",
    "password": "admin"
}

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != account["username"] or password != account["password"]:
        return jsonify({"message": "Bad username or password"}), 401

    access_token = create_access_token(identity=account)
    response = make_response(jsonify(access_token=access_token), 200)
    response.set_cookie('access_token_cookie', access_token)
    return response

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/", methods=["GET"])
def mainPage():
    return 200

if __name__ == "__main__":
    app.run(port=5000)
