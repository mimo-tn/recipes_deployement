from flask_app.config.mysqlconnection import db,connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.comment import Comment

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked_made = data["date_cooked_made"]
        self.duration = data["duration"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users_who_comment = []
        self.comment = []
        self.owner = None
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO recipes (name, description, instructions, date_cooked_made, user_id , duration, created_at, updated_at)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked_made)s, %(user_id)s, %(duration)s, NOW(), NOW());
                """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM recipes
            LEFT JOIN users AS owners ON recipes.user_id = owners.id
            LEFT JOIN recipes_comment ON recipes.id =  recipes_comment.recipes_id
            LEFT JOIN users AS users_who_comment ON users_who_comment.id = recipes_comment.users_id
            ORDER BY recipes.id;
        """
        results = connectToMySQL(db).query_db(query)
        recipes = []

        for row in results:
            # Consider this row to be a new recipe
            new_recipe = True

            # Parse the data of the user that liked the recipe to a dictionary
            user_who_comment_data = {
                'id': row['users_who_comment.id'],
                'email': row['users_who_comment.email'],
                'first_name': row['users_who_comment.first_name'],
                'last_name': row['users_who_comment.last_name'],
                'password': row['users_who_comment.password'],
                'created_at': row['users_who_comment.created_at'],
                'updated_at': row['users_who_comment.updated_at'],
            }
            comment_data = {
                'id': row['recipes_comment.id'],
                'note': row['note'],
                'recipe_id': row['recipes_id'],
                'user_id': row['users_id'],
            }

            # Storing the number of recipes added the final list
            number_of_recipes = len(recipes)

            # We are checking if we are on the first iteration of the loop
            if number_of_recipes > 0:
                # Get the recipe of the previous iteration
                previous_recipe = recipes[number_of_recipes - 1]
                if previous_recipe.id == row['id']:
                    previous_recipe.users_who_comment.append(User(user_who_comment_data))
                    previous_recipe.comment.append(Comment(comment_data))
                    new_recipe = False

            if new_recipe:
                # Creating an instance of the recipe
                recipe = cls(row)

                # Dictionary to create the owner of this recipe
                owner_data = {
                    'id': row['owners.id'],
                    'email': row['email'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'password': row['password'],
                    'created_at': row['owners.created_at'],
                    'updated_at': row['owners.updated_at'],
                }
                recipe.owner = User(owner_data)
                if row['users_who_comment.id']:
                    recipe.users_who_comment.append(User(user_who_comment_data))
                    recipe.comment.append(Comment(comment_data))
                recipes.append(recipe)

        return recipes
    # @classmethod
    # def get_all(cls):
    #     query = """
    #             SELECT * FROM recipes
    #             LEFT JOIN users
    #             ON recipes.user_id = users.id
    #             ORDER BY recipes.created_at DESC;
    #             """
    #     results = connectToMySQL(db).query_db(query)
    #     if results:
    #         recipes = []
    #         for row in results:
    #             recipe = cls(row)
    #             user_data = {
    #                 "id" : row["users.id"],
    #                 "first_name" : row["first_name"],
    #                 "last_name" : row["last_name"],
    #                 "email" : row["email"],
    #                 "password" : None,
    #                 "created_at" : None,
    #                 "updated_at" : None
    #             }
    #             recipe.users = User(user_data)
    #             recipes.append(recipe)
    #         return recipes
    #     else: 
    #         return []
    @classmethod
    def get_by_user_id(cls, data):
        query = """
                SELECT * FROM recipes
                LEFT JOIN users
                ON recipes.user_id = users.id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query,data)
        if results:
            recipes = cls(results[0])
            user_data = {
                    "id" : results[0]["users.id"],
                    "first_name" : results[0]["first_name"],
                    "last_name" : results[0]["last_name"],
                    "email" : results[0]["email"],
                    "password" : None,
                    "created_at" : None,
                    "updated_at" : None
                }
            recipes.users = User(user_data)
            return recipes
        else: 
            return []
    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM recipes
                LEFT JOIN users
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query,data)
        if results:
            recipes = cls(results[0])
            user_data = {
                    "id" : results[0]["users.id"],
                    "first_name" : results[0]["first_name"],
                    "last_name" : results[0]["last_name"],
                    "email" : results[0]["email"],
                    "password" : None,
                    "created_at" : None,
                    "updated_at" : None
                }
            recipes.users = User(user_data)
            return recipes
        else: 
            return []
    @classmethod
    def update(cls , data):
        query = """
                UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked_made = %(date_cooked_made)s, duration = %(duration)s, updated_at = NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query , data)
    
    @classmethod
    def delete(cls , data):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query , data)
    @staticmethod
    def validate_recipes(data):
        is_valid= True
        if  not data["name"] and not data["description"] and not data["instructions"]:
            is_valid = False
            flash("All fields required",'error16')
        else:
            if len(data["name"]) < 3:
                is_valid = False
                flash("Name must be at least 3 characters",'error17')
            if len(data["description"]) < 3:
                is_valid = False
                flash("Description must be at least 3 characters",'error18')
            if len (data["instructions"]) < 3:
                is_valid = False
                flash("Instructions must be at least 3 characters",'error19')
        return is_valid

