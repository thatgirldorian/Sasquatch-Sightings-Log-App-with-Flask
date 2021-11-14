from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.sighting import Sighting

@app.route('/new/sighting')
def new_sighting():
    return render_template('new_sighting.html')

@app.route('/report',methods=['POST'])
def create_sighting():
    if Sighting.validate_report(request.form):
        Sighting.save(request.form)
        return redirect('/')
    data ={ 
        "location": request.form['location'],
        "what_happened": request.form['what_happened'],
        "date_of_sighting": request.form['date_of_sighting'],
        "no_of_sas": request.form['no_of_sas']
    }
    id = Sighting.save(data)
    session['sighting_id'] = id

    return redirect('/dashboard')

@app.route('/dashboard')
def updated_dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "location": request.form['location'],
        "what_happened": request.form['what_happened'],
        "date_of_sighting": request.form['date_of_sighting'],
        "no_of_sas": request.form['no_of_sas']
    }
    return render_template("dashboard.html", sighting=Sighting.get_by_id(data))
