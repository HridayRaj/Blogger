from flask import Flask, render_template , request , session , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
import json
with open('config.json' , 'r') as c:
    params=json.load(c)['params']
local_server=True
app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']


db = SQLAlchemy(app)

class Contact(db.Model):
    '''
     Slno. , Name , Email , phone , Date

    '''
    Slno   = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(120), nullable=False)


class blogdata(db.Model):

    ''' Sno , Title , slug , Content , Date , img'''
    Sno=db.Column(db.Integer , primary_key=True)
    Title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    Content = db.Column(db.String(220), nullable=False)
    Date = db.Column(db.String(12), nullable=False)
    img=db.Column(db.String(11), nullable=False)


''' home page'''
@app.route("/")
def home():
    posts=blogdata.query.filter_by().all()
    return render_template("index.html" ,params=params, posts=posts)


''' dashboard'''
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
@app.route("/dashboard" ,  methods=['GET' , 'POST'])
def dashboard():

    if( 'user' in session and session['user']==params['uname'] ):
        return render_template('dashboard.html' , params=params)


    if(request.method =='POST'):
        username=request.form.get('uname')
        userpass=request.form.get('upass')

        if(username == params['uname'] and userpass==params['upass']):
            session['user']=username
            posts=blogdata.query.all()
            return render_template('dashboard.html', params=params , posts=posts)

    else:
        return render_template('login.html' ,   params=params)



''' inside dashboard'''
''' session close'''
@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html' , params=params)

''' about'''

@app.route("/about")
def hriday():
    return render_template('about.html',params=params)

''' contact form  '''
@app.route("/contact" , methods =['GET' , 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to database '''
        name=request.form.get('name')
        email_id=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('msg')

        entry=Contact(Name=name , Email=email_id , phone=phone , msg=message , Date=datetime.now())

        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html",params=params)


@app.route("/post/<string:post_slug>" , methods=['GET'])
def post_route(post_slug):
    post=blogdata.query.filter_by(slug=post_slug).first()
    return render_template("post.html",params=params , post=post)



''' adding blog content'''

@app.route('/edit/<string:sno>' , methods=['GET', 'POST'])
def edit(sno):
    if ('user' in session and session['user'] == params['uname']):
        if(request.method=='POST'):
            title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            ''' Sno , Title , slug , Content , Date , img'''
            entry=blogdata(Sno=sno, Title=title , slug=slug , Content=content , Date=datetime.now() , img='img/home.jpg')

            if(sno=='0'):
                db.session.add(entry)
                db.session.commit()
            else:
                edit_post=blogdata.query.filter_by(Sno=sno).first()
                edit_post.Title=title
                edit_post.slug=slug
                edit_post.Content=content
                edit_post.date=datetime.now()
                db.session.commit()

                return redirect('edit/'+sno)

        post=blogdata.query.filter_by(Sno=sno).first()
        return render_template('edit.html' , params=params , post=post)



''' delete the post'''
@app.route('/delete/<string:sno>')
def delete(sno):
    if('user' in session and session['user']==params['uname']):
        post = blogdata.query.filter_by(Sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        redirect('/dashboard')


app.run(debug=True)

