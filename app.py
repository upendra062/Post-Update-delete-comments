
from datetime import datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
# database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Rocky.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Rocky(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("post")
        title = request.form['title']
        desc = request.form['desc']
        todo = Rocky(title = title, desc= desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Rocky.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Rocky.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')  

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Rocky.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Rocky.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/show")
def products():
    allTodo = Rocky.query.all()
    print(allTodo)
    return 'this is products page'
 

if __name__ == "__main__":
    app.run(debug=True, port=8000) 