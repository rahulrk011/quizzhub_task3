from app import app,db
from flask import Flask,render_template,flash,redirect,url_for,request,session,jsonify
from werkzeug.urls import url_parse
from app.forms import LoginForm,RegistrationForm,EditProfileForm,EmptyForm,PostForm,quizForm,quiz_info_Form
from app.models import User,Quiz,Quiz_ques
from flask_login import current_user,login_user,logout_user,login_required
from datetime import datetime
import json

quiz_data={}

@app.route("/")
@app.route("/welcome",methods=['GET','POST'])
def landing():
    return render_template('landing.html',title='welcome')



@app.route("/home",methods=['GET','POST'])
@login_required
def home():
    return render_template('home.html', title='home')


@app.route('/submit_quiz', methods=['GET','POST'])
@login_required
def submit_quiz():
    if request.method=='POST':
        data = request.json
        score = data.get('score')
        quiz_name = data.get('quiz_name')
        print(score,quiz_name)
        quiz_data['score']=score
        quiz_data['quiz_name']=quiz_name
        return jsonify({'message': 'Quiz data received successfully!'})
    else:
        return jsonify(quiz_data)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page= request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('landing')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form= RegistrationForm()
    if form.validate_on_submit():
        user= User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! \n Please sign in to continue')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user,form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/follow/<username>',methods=['POST'])
@login_required
def follow(username):
    form=EmptyForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found'.format(username))
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are now following {}'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('home'))
    
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('home'))
    
@app.route('/quizinfo', methods=['GET', 'POST'])
@login_required
def quizinfo():
    form = quiz_info_Form()

    if form.validate_on_submit():
        quiz = Quiz(name=form.name.data, number=form.noq.data,author=current_user)
        db.session.add(quiz)
        db.session.commit()

        session['quiz_id'] = quiz.id
        session['quiz_name'] = quiz.name
        session['quiz_number'] = quiz.number

        return redirect(url_for('questions'))

    return render_template('quizinfo.html', title='info', form=form)


@app.route('/questions/', methods=['GET', 'POST'])
@login_required
def questions():
    form = quizForm()

    quiz_id = session.get('quiz_id')
    quiz_name = session.get('quiz_name')
    quiz_number = session.get('quiz_number')

    if quiz_id is None or quiz_name is None or quiz_number is None:
        return redirect(url_for('quizinfo'))

    if form.validate_on_submit():
        question_number=form.question_number.data
        question=form.question.data
        option1= form.op1.data
        option2= form.op2.data
        option3= form.op3.data
        option4= form.op4.data
        correct_option = form.crctop.data


        quiz_ques = Quiz_ques(
                
                question=question,
                op1=option1,
                op2=option2,
                op3=option3,
                op4=option4,
                correct_option=correct_option,
                quiz_id=quiz_id
            )
        
        db.session.add(quiz_ques)
        db.session.commit()
        print(question_number)
        next_question_number=int(question_number)+1
        print(next_question_number)
        if next_question_number<= quiz_number:
            form.question.data = ''
            form.op1.data = ''
            form.op2.data = ''
            form.op3.data = ''
            form.op4.data = ''
            form.crctop.data = ''
            return redirect(url_for('questions'))
        else:      
            return redirect(url_for('landing'))
    return render_template('questions.html', title="questions", form=form)


@app.route('/quiz/<quizname>')
@login_required
def quiz(quizname):
    quiz=Quiz.query.filter_by(name=quizname).first_or_404()
    questions= quiz.questions.order_by(Quiz_ques.id)
    form = EmptyForm()
    return render_template('quiz.html', questions=questions,quiz=quiz,form=form)


@app.route('/search_users', methods=['GET'])
@login_required
def search_users():
    username = request.args.get('username')

    # Perform the search query on the server-side and retrieve matching users
    matching_users = User.query.filter(User.username.like(f'%{username}%')).all()

    # Convert the list of user objects into a list of dictionaries
    users_list = [{'username': user.username, 'id': user.id} for user in matching_users]

    # Return the matching users as a JSON response
    return jsonify({'users': users_list})

    
