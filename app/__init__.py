from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from app.db import db
from app.models import User
import os

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///test.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "dev-secret")
    app.config['JWT_SECRET_KEY'] = "secret-key" # CHANGE

    app.json.compact = False

    db.init_app(app)         
    jwt.init_app(app)    


    with app.app_context():
        print("====                 Creating DB")
        db.create_all()


    # @app.route("/")
    # def hello_world():
    #     return "<p>Hello, World!</p>"

    @app.route('/')
    def home():
        return render_template('templates/login.html')
    
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            return jsonify({"msg": "Missing username or password"}), 400

        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"msg": "User already exists"}), 409

        user = User(username=data["username"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()

        if not user or not user.check_password(data["password"]):
            return jsonify({"msg": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    

    return app
