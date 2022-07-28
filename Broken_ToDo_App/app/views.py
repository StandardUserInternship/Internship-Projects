from flask import jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'id: {self.id}'

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'status':self.status}



@app.route('/')
def index():
    return render_template('home.html')


@app.route('/addToDo', methods=['POST', 'GET'])
def addToDo():
    title = request.get_json()['title']
    status = 'In Progress'
    # ToDo :) Create a new row in the database for the new todo
    db.session.add(todo)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/getToDo', methods=['GET'])
def getToDo():
    todos = [s.serialize() for s in ToDo().query.all()]    
    return jsonify({'todo': todos})


@app.route('/toDoActions', methods=['POST'])
def toDoActions():
    action = request.get_json()['action']
    todo_id = request.get_json()['id']
    if action == 'DEL':
        ToDo.query.filter_by(id=todo_id).delete()
        db.session.commit()
        return jsonify({'status': 'success'})
    elif action == 'FIN':
        todo = ToDo.query.filter_by(id=todo_id).first()
        todo.status = 'Finished'
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})