from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    headers = request.headers
    return "Headers are" + str(headers) 

@app.route('/notes/all')
def notes_all():

    # Return all the notes_all
    return 'notes'

@app.route('/notes/new', methods=['POST'])
def notes_new():
    #Create a new note
    note = request.form.get('note')
    return str(note)

@app.route('/notes/delete')
def notes_delete():
    #Delete a note
    return "delete"

if __name__ == "__main__":
    app.run()
