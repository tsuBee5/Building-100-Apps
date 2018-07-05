from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# create app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'

db = SQLAlchemy(app)


# define database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


# routers
@app.route('/')
def index():
    todos_incomplete = Todo.query.filter_by(complete=False).all()
    todos_complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html',
                           todos_incomplete=todos_incomplete,
                           todos_complete=todos_complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todo-item'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
	## for debub
	#app.run(debug=True)
