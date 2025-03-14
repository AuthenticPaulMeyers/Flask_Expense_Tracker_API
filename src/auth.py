from flask import Blueprint, jsonify

auth=Blueprint('auth', __name__, url_prefix='/api/v1.0/auth')


@auth.post("/register")
def register():
    return jsonify({'name': "your name"})