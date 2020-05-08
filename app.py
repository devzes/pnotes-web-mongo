from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import json
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI']=os.getenv('MONGO_URI')
mongo=PyMongo(app)


'''
List of class, functions and routes

class JSONEncoder - To convert the Json having ObjectId to simple String


/
index() - index Page

/api/notes/all
notes_all() - API to get all the notes in the database

/api/notes/new
notes_new() - API To add a new note in the database

/api/notes/delete
notes_delete() - API To delete a note in the database

'''

'''--------------- Classes ---------------'''
# Class to convert ObjectId to simple String 
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)        

'''---------------- Functions -------------'''
# Funciton to insert a new note
def insertNote(heading, description):
    insert_value = mongo.db.notes.insert_one({ "heading": heading, "description": description })
    return str(insert_value.inserted_id)

def deleteNote(id):
    mongo.db.notes.delete_one({ "_id": id })  #check if it is deleting or not

'''--------------- Routes -----------------'''

''' Main Page to be added soon '''
@app.route('/')
def index():
    headers = request.headers
    return "Headers are" + str(headers) 

'''--------------- API Routes --------------'''
''' 
API to get all the notes 
Example:
Request: 
GET (No parameters needed)

Response:
{ notes: [ {'_id': '5eb55594da6e679996f27b66', 'heading': 'hello', 'description': 'Note description' }  ]}
list in notes,
String in _id, heading, description
'''
@app.route('/api/notes/all')    # This can give errors, add a try catch also
def notes_all():
    # Return all the notes_all
    online_notes = mongo.db.notes.find({})
    data = { 'notes': list(online_notes) }
    #print(data)
    return JSONEncoder().encode(data)  #This converts the ObjectId to simple Iid


'''
API to add a new note
Example:
Request:
POST Body in form or json type
Parameters: heading String, description String

Response:
data = { success: 1, msg="Error message or success message" or inserted_id: "id" }
'''
@app.route('/api/notes/new', methods=['POST'])
def notes_new():
    #Create a new note
    try:
        if(request.is_json):
            #print("Yes a json")
            data = request.get_json()
            heading = data['heading']
            description = data['description']
        else:
            #print("Will think it as a form urlencoded")
            heading = request.form['heading']
            description = request.form['description']

        inserted_id = insertNote(heading, description)
        return ({ "success":1, "inserted_id": inserted_id })
    except Exception as e:
        return ({'success':0, "msg": str(e)})


''' //Need to think of how this needs to be done
API to delete a note
Request: (POST) In form url encoded or Json body
Just send the note id and { 'id': 'Note id'}

Response:
data = { success: 1, msg="Error message or success message" }
'''
@app.route('/api/notes/delete', methods=['POST'])
def notes_delete():
    #Delete a note
    try:
        if(request.is_json):
            #print("Yes a json")
            data = request.get_json()
            id = data['id']
        else:
            #print("Will think it as a form urlencoded")
            id = request.form['id']

        deleteNote(id)
        return ({ "success":1, "msg": "successfully deleted!" })
    except Exception as e:
        return ({'success':0, "msg": str(e)})

if __name__ == "__main__":
    app.run()
