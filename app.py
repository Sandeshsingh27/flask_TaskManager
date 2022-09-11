from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///taskManager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
        # return '<Todo %r>' % self.sno  //different ways of printing the task list

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        try:
            db.session.add(todo)
            db.session.commit()
        except:
            return 'There was an issue adding your task'
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form.get('desc')
        status = request.form.get('status')
        # print(status)
        todo = Todo.query.filter_by(sno=sno).first()
        # todo = Todo.query.get_or_404(sno)
        todo.title = title
        todo.desc = desc
        if status == "true":
            todo.status= True
        else:
            todo.status= False
        try:
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        except:
            return 'There was an issue updating your task'
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    # todo = Todo.query.get_or_404(sno)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an issue deleting your task'

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, port=8000)