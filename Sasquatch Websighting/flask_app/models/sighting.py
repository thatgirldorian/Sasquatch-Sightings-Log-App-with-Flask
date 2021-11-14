from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Sighting:
    db = "login_schema"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_of_sighting = data['date_of_sighting']
        self.no_of_sas = data['no_of_sas']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location,what_happened,date_of_sighting,no_of_sas) VALUES(%(location)s,%(what_happened)s,%(date_of_sighting)s,%(no_of_sas)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db).query_db(query)
        sightings = []
        for row in results:
            sightings.append( cls(row))
        return sightings

    # @classmethod
    # def get_by_email(cls,data):
    #     query = "SELECT * FROM sightings WHERE email = %(email)s;"
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     if len(results) < 1:
    #         return False
    #     return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_report(sighting):
        is_valid = True
        if len(sighting['location']) < 2:
            flash("Location must be at least 2 characters","report")
            is_valid= False
        if len(sighting['what_happened']) < 3:
            flash("What happened must be at least 2 characters","report")
            is_valid= False
        if len(sighting['date_of_sighting']) < 2:
            flash("Date must have a value","report")
            is_valid= False
        if len(sighting['no_of_sas']) < 1:
            flash("Number of sasquatch must be at least 1","report")
        return is_valid