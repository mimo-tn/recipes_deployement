from flask_app.config.mysqlconnection import db,connectToMySQL
from flask import flash
from flask_app import app


class Comment:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.recipe_id= data["recipe_id"]
        self.note = data["note"]
        self.users = None
    @classmethod
    def add_comment(cls , data):
        query = "INSERT INTO recipes_comment ( recipes_id, users_id, note) VALUES (%(recipe_id)s, %(user_id)s, %(note)s);"
        return connectToMySQL(db).query_db(query , data)

    # Method to remove a like from a review
    @classmethod
    def remove_user_like(cls , data):
        query = "DELETE FROM recipes_comment WHERE user_id = %(user_id)s AND review_id = %(review_id)s;"
        return connectToMySQL(db).query_db(query , data)