from flask import Flask, render_template,jsonify,request,abort,Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mydatabase'
db = SQLAlchemy(app)
CORS(app)

class movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column('movie_id', db.Integer,primary_key=True)
    title = db.Column('movie_title', db.Unicode)
    genre = db.Column('movie_genre', db.Unicode)
    def  __init__(self, id, title, genre):
        self.id = id
        self.title = title
        self.genre = genre

@app.route('/mov',methods=["POST"])
def add_movie():

    title = request.get_json(force=True)["title"]
    id = request.get_json(force=True)["id"]
    gen  =request.get_json(force=True)["genre"]
    #new_ex = movies(id,title)
    #print(gen)
    db.session.add(movie(id,title,gen))
    db.session.commit()
    return "success"

@app.route('/ge',methods=['GET'])
#@cross_origin()
def get_movie():

    ex=movie.query.all()
    lis = ""
    for e in ex:
        lis=lis+str(e.title)+"#"
    lis = lis + "%"
    for e in ex:
        lis=lis+str(e.id)+"$" 
    #print(lis)
    return(lis)

@app.route('/re',methods=['GET'])
#@cross_origin()
def recommend():
    result = db.engine.execute("SELECT movie_genre FROM movie GROUP BY movie_genre ORDER BY COUNT(*) DESC LIMIT 1;")
    for rowproxy in result:
        for column,value in rowproxy.items():
            res=value
    return str(res)
