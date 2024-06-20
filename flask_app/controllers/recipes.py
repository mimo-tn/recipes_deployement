from flask_app import app
from flask import render_template, redirect, session, request, url_for
from flask_app.models.recipe import Recipe
from flask_app.models.recipe import User
@app.route('/all_recipes')
def read_recipes():
    recipes = Recipe.get_all()
    return render_template("recipes.html",recipes = recipes)
@app.route('/recipes/<int:id>')
def read_one_recipe(id):
    if 'first_name' in session:
        if id :
            data = {"id" : id}
            recipe = Recipe.get_by_id(data)
            return render_template("show_recipe.html", recipe = recipe)
    else:
        return redirect('/')
@app.route('/edit/recipes/<int:id>')
def edit_one_recipe(id):
    if 'first_name' in session:
        if id :
            data = {"id" : id}
            recipe = Recipe.get_by_id(data)
            return render_template("edit_recipe.html", recipe = recipe)
    else:
        return redirect('/')

@app.route('/recipes/new')
def new_recipes_form():
    if 'first_name' in session:
        return render_template("create_recipe.html")
    else:
        return redirect('/')
@app.route('/create/recipes/new', methods = ['POST'])   
def create_recipes():
            if 'first_name' in session:
                session["form"] = "form3"
                if Recipe.validate_recipes(request.form):
                    first_data = {"email" : session['email']}
                    user = User.get_by_email(first_data)
                    second_data = {
                                    "user_id" : user.id,
                                    "name" : request.form['name'],
                                    "description" : request.form['description'],
                                    "instructions" : request.form['instructions'],
                                    "date_cooked_made" : request.form['date_cooked_made'],
                                    "duration" : request.form['duration']
                                }
                    Recipe.save(second_data)
                    return redirect('/all_recipes')
                return redirect('/recipes/new')
            else :
                return redirect('/')
@app.route('/update/recipes', methods = ['POST'])   
def update_recipes():
            if 'first_name' in session:
                session["form"] = "form4"
                if Recipe.validate_recipes(request.form):
                    data = {
                                    "id" : request.form['id'],
                                    "user_id" : request.form['user_id'],
                                    "name" : request.form['name'],
                                    "description" : request.form['description'],
                                    "instructions" : request.form['instructions'],
                                    "date_cooked_made" : request.form['date_cooked_made'],
                                    "duration" : request.form['duration']
                                }
                    Recipe.update(data)
                    return redirect('/all_recipes')
                recipe = Recipe.get_by_id(request.form)
                return render_template("edit_recipe.html", recipe = recipe)
            else :
                return redirect('/')
@app.route('/delete/<int:id>')   
def delete_post(id):
        if 'first_name' in session:
            data ={
                "id" : id
            }
            Recipe.delete(data)
            return redirect('/all_recipes')
        else :
            return redirect('/') 