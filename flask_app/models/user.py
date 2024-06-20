from flask_app.config.mysqlconnection import db,connectToMySQL
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import app
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d).+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    @classmethod
    def save(cls , data):
        encrypted_password = bcrypt.generate_password_hash(data['password'])
        data = dict(data)
        data['password'] = encrypted_password
        query = """
                INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
                """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL(db).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return []
    @classmethod
    def edit(cls, data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM users
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, data)
    @staticmethod
    def validate_register_form(data):
        is_valid= True
        email = User.get_by_email(data)
        
        if len(data["first_name"]) < 2:
            is_valid = False
            flash("First name must be at least 2 characters",'error1')
        elif not data["first_name"].isalpha():
            is_valid = False
            flash("First name must contain only letters", 'error2')
        
        if len(data["last_name"]) < 2:
            is_valid = False
            flash("last name must be at least 2 characters",'error3')
        elif not data["last_name"].isalpha():
            is_valid = False
            flash("Last name must contain only letters", 'error4')

        if email:
            is_valid = False
            flash("A user with this email already exists",'error5')
        if not data["email"]:
            is_valid = False
            flash("You must put a email",'error6')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("invalid Email",'error7')

        if len(data['password']) < 8:
            is_valid = False
            flash("Passwords must be at least 8 characters",'error8')
        elif not PASSWORD_REGEX.match(data['password']):
            is_valid = False
            flash("Password must contain at least one number and one uppercase letter", 'error13')
        elif data['password'] != data['confirm_password']:
            is_valid = False
            flash("Passwords must match.",'error9')
        return is_valid
    @staticmethod
    def validate_login(data):
        
        input_data ={
                "email" : data["email_login"],
                "password" : data["password_login"]
        }
        is_valid = True
        user_in_db = User.get_by_email(input_data)

        if not EMAIL_REGEX.match(input_data['email']):
            is_valid = False
            flash("Invalid email",'error10')
        elif not user_in_db:
            is_valid = False
            flash("No user with this email exists",'error11')
        elif not bcrypt.check_password_hash(user_in_db.password , data['password_login']):
            is_valid = False
            flash("Incorrect Password",'error12')
        
        return is_valid