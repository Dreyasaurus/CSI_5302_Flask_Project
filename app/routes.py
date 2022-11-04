from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, People, UserPeople
from datetime import datetime




@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        subquery = db.session.query(UserPeople.playerid).filter_by(userid= current_user.id).subquery()
        query = db.session.query(People).filter(People.playerId.in_(subquery))
        results = db.session.execute(query)
        likedP = results.fetchall()
        posts = [r[0] for r in likedP]
        print(posts)
        
    return render_template("index.html", title='Home Page', posts=posts,rule =  "base.css")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.all()
    print(user)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form,rule =  request.url_rule)
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form,rule =  request.url_rule)
   
   
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
    
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts,rule =  request.url_rule)
    
    
        
        
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form,rule =  request.url_rule)
    
    
@app.route('/player/<playerId>', methods=['GET', 'POST','DELETE'])
@login_required
def playerId(playerId):
    if request.method == 'POST':
        sql = 'INSERT INTO user_people(userId,playerid) VALUES('+str(current_user.id)+',\''+playerId+'\');'
        db.session.execute(sql)
        db.session.commit()
        return '{\"message\":\"success\"}'
        
        
    if request.method == 'DELETE':
        r= UserPeople.query.filter_by(userid = current_user.id, playerid = playerId).first()
        print(r)
        db.session.delete(r)
        r= UserPeople.query.filter_by(userid = current_user.id, playerid = playerId).first()
        print(r)
        db.session.commit()
        return '{\"message\":\"success\"}'
        
    lResult = db.session.execute('SELECT count(1) FROM user_people where userid = \''+str(current_user.id) + '\' and playerid= \''+ playerId+'\'')
    liked = lResult.fetchone()
    player = People.query.get(playerId)
    carrerSummary=[]
    results = db.session.execute("Call carrer_summary ('"+playerId+"')")
    for row in results:
        carrerSummary =row
    return render_template('player.html', player=player,carrer_summary=carrerSummary,rule = "player.css", liked = liked[0])