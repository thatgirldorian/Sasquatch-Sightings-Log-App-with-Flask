from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

#This route shows our page for creating a new sighting
@app.route('/new/sighting')
def new_sighting():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['users_id']
    }
    return render_template('new_sighting.html',user=User.get_by_id(data))

#This route posts the newly created sighting
@app.route('/create/sighting',methods=['POST'])
def create_sighting():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "no_of_sas": request.form["no_of_sas"],
        "users_id": session["users_id"]
    }
    Sighting.save(data)
    return redirect('/dashboard')


@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['users_id']
    }
    return render_template("edit.html", edit=Sighting.get_one(data),user=User.get_by_id(user_data))


@app.route('/update/sighting',methods=['POST'])
def update_sighting():
    if 'users_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "no_of_sas": (request.form["no_of_sas"]),
        "id": request.form['id']
    }
    Sighting.update(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show_sighting(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['users_id']
    }
    return render_template("show.html",sighting=Sighting.get_one(data),user=User.get_by_id(user_data))

@app.route('/delete/sighting/<int:id>')
def delete_sighting(id):
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Sighting.delete(data)
    return redirect('/dashboard')