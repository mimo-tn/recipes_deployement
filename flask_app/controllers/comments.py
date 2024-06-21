from flask_app import app
from flask import render_template, redirect, session, request, url_for
from flask_app.models.comment import Comment

@app.route('/creat_note', methods = ['POST'])
def process_input():
    if 'first_name' in session:
        data = {
                "recipe_id" : request.form['recipe_id'],
                "user_id" : request.form['user_id'],
                "note" : request.form['note']
                }
        print(f"salalalalalala{data}")
        Comment.add_comment(data)
        return redirect('/all_recipes')
    else :
        return redirect('/')
