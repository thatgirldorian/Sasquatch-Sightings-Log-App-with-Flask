from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from pprint import pprint



class Sighting:
    db = "login_schema"

    def __init__(self,db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.what_happened = db_data['what_happened']
        self.date_of_sighting = db_data['date_of_sighting']
        self.no_of_sas = db_data['no_of_sas']
        self.users_id = db_data['users_id']
        self.reporter = db_data['reporter']


    #This method saves new data inserted into the db
    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location, what_happened, date_of_sighting, no_of_sas, users_id) VALUES (%(location)s,%(what_happened)s,%(date_of_sighting)s,%(no_of_sas)s,%(users_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    #This method gets all the available sightings
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_sightings = []
        for row in results:

            all_sightings.append( cls(row) )
        return all_sightings
    
    #This method selects one sighting row
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    #This method updates the sightings data
    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, what_happened=%(what_happened)s, date_of_sighting=%(date_of_sighting)s, no_of_sas=%(no_of_sas)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    #This method deletes the sightings data (per row)
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    #This method validates our data
    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting['location']) < 3:
            is_valid = False
            flash("Location must be at least 3 characters","sighting")
        if len(sighting['what_happened']) < 3:
            is_valid = False
            flash("What Happened must be at least 3 characters","sighting")
        if (sighting['date_of_sighting']) == "":
            is_valid = False
            flash("Please enter a valid date","sighting")
        if len(sighting['no_of_sas']) < 1:
            is_valid = False
            flash("Number of sasquatch must be at least 1","sighting")
        return is_valid