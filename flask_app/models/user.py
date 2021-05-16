from logging import StrFormatStyle
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re 
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.hack_attempts = data['hack_attempts']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('wall_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) \
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('wall_schema').query_db(query,data)


    @staticmethod
    def register_validation(user):

        is_valid = True

        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        else:
            if not str(user['first_name']).isalpha():
                flash('First name can NOT contain numbers')
                is_valid = False

        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        else:
            if not str(user['last_name']).isalpha():
                flash('Last name can NOT contain numbers')

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address')
            is_valid = False
        else:
            if User.get_user_by_email({'email': user['email']}) :
                flash('Email address already taken')
                is_valid = False

        if len(user['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False

        #Check for at least 1 digit
        if not re.search(r'\d', user['password']):
            flash('Password must contain at least 1 number')
            is_valid = False
        
        if not re.match(r'\w*[A-Z]\w*', user['password']):
            flash('Password must contain at least 1 capitol letter')
            is_valid = False

        if user['password'] != request.form['confirm_password']:
            flash('Passwords do not match')
            is_valid = False

        return is_valid


    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('wall_schema').query_db(query,data)
        return cls(results[0])


    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('wall_schema').query_db(query,data)


    @classmethod
    def get_all_not_self(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s ORDER BY first_name"
        return connectToMySQL('wall_schema').query_db(query,data)


    @classmethod
    def update_attemps(cls,data):
        query = "UPDATE users SET hack_attempts = 1 WHERE id = %(id)s"
        return connectToMySQL('wall_schema').query_db(query,data)

    @staticmethod
    def login_validation(user,password):
        if not user:
            flash("Invalid login")
            return False
        if not bcrypt.check_password_hash(user.password, password):
            flash("Invalid login")
            return False

        return True