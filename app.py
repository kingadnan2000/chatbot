from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

from chatbot import chatbot

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


#@app.route('/enternew')
#def new_record():
#   return render_template('new.html')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class database1(db.Model):
    id = db.Column('qns_id', db.Integer, primary_key = True)
    Question = db.Column(db.String(100))
    Answers = db.Column(db.String(1000))


    def __init__(self, Question:str, Answers:str):
        self.Question = Question
        self.Answers = Answers

@app.route('/show_all.html')
def show_all():
    return render_template('show_all.html', qnsans = database1.query.all())



@app.route('/new.html', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['Question'] or not request.form['Answers']:
         flash('Please enter all the fields', 'error')
      else:
         qnsans = database1(request.form['Question'], request.form['Answers'])
         # qnsans = database(question = request.form['Question'], answer = request.form['Answers'])
         db.session.add(qnsans)
         db.session.commit()
         flash('Record was successfully added')
         db.session.close()
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug =False)
