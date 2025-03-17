from flask import Blueprint, jsonify, request
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db, User
from src.constants.http_status_codes import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

auth=Blueprint('auth', __name__, url_prefix='/api/v1.0/auth')

@auth.post("/register")
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # input validations
    if " " in username:
        return jsonify({"error": "username should not contain space"})
    if len(username) < 3:
        return jsonify({"error": "username is too short"})
    if not username.isalnum():
        return jsonify({"error": "username should not contain numbers or special characters"})
    
    if not validators.email(email):
        return jsonify({"error": "email is invalid"})
    
    if len(password) < 6:
        return jsonify({"error:" "password is too short. Atleast 6 characters long"})
    
    # check if the username and email already exist
    if User.query.filter_by(username=username).first():
        return jsonify({"error": 'username already exist'}), HTTP_409_CONFLICT
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": 'email already exist'}), HTTP_409_CONFLICT
    
    # generate a password hash 
    password_hashed = generate_password_hash(password)

    # save the contents in the users table in the database
    user=User(username=username, email=email, password=password_hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'user registered successfully',
        'user':{
            'username': username,
            'email': email
        }
    }), HTTP_201_CREATED

# user login route
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # get the user from the db by email
    user=User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "wrong email or password"}), HTTP_400_BAD_REQUEST
    
    password_check=check_password_hash(user.password, password)

    if password_check:
    # create jwt tokens
        access=create_access_token(identity=str(user.id))
        refresh=create_refresh_token(identity=str(user.id))

        return jsonify({
            'message': "login successfully",
            'user':{
                'email': user.email,
                'access': access,
                'refresh': refresh,
                'id': user.id

            }
        }), HTTP_200_OK
    return jsonify({"message": "wrong password"}), HTTP_400_BAD_REQUEST
    

# get user profile
@auth.get('/profile')
@jwt_required()
def user_profile():
    user_id=get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()

    return jsonify({
        'profile':{
            'username': user.username,
            'email': user.email,

        }
    }), HTTP_200_OK

# create user refresh token
@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_token():
    user_id=get_jwt_identity()
    access=create_access_token(identity=str(user_id))

    return jsonify({
        'access': access
    }), HTTP_200_OK

# update user profile
@auth.put("/update_profile")
@jwt_required()
def update_profile():
    current_user_id=get_jwt_identity()

    profile=User.query.filter_by(id=current_user_id).first()
    
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # input validations
    if " " in username:
        return jsonify({"error": "username should not contain space"})
    if len(username) < 3:
        return jsonify({"error": "username is too short"})
    if not username.isalnum():
        return jsonify({"error": "username should not contain numbers or special characters"})
    
    if not validators.email(email):
        return jsonify({"error": "email is invalid"})
    
    if len(password) < 6:
        return jsonify({"error:" "password is too short. Atleast 6 characters long"})
    
    # check if the username and email already exist
    if User.query.filter_by(username=username).first():
        return jsonify({"error": 'username already exist'}), HTTP_409_CONFLICT
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": 'email already exist'}), HTTP_409_CONFLICT
    
    # generate a password hash 
    password_hashed = generate_password_hash(password)

    # save the contents in the users table in the database
    profile.username = username
    profile.email = email
    profile.password = password_hashed
    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully',
        'user':{
            'username': profile.username,
            'email': profile.email
        }
    }), HTTP_201_CREATED
