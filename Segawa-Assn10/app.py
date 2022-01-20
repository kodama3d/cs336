#   Name: Dustin Segawa
#   Assignment: CS336 Assignment #10
#   Created: 8/18/2020
#   Description: Flask Python

from flask import Flask, redirect, render_template, request, session
from functools import wraps
import sqlite3
import jinja2
import datetime
import random

app = Flask(__name__)
app.secret_key = 'password123'

# attempts to open connection to database
# IN: opened file variable
# OUT: connection to database
# CALLS: sqlite3 connection method
def db_connect(file):
    try:  # tries to open connection to db file
        db_connection = sqlite3.connect(file)
        db_connection.row_factory = sqlite3.Row
        print('db connected')
        return db_connection
    except Exception as err:
        exit(err)

# attempts to assign cursor to the database connection
# IN: opened database connection
# OUT: cursor to database
# CALLS: cursor method
def assign_cursor(db_connection):
    try:  # tries to assign cursor to db
        c = db_connection.cursor()
        print('cursor assigned')
        return c
    except Exception as err:
        exit(err)

# check if session is logged in
# IN: function to run
# OUT: passed function
# CALLS: none
def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return 'You are NOT logged in as an administrator and do not have access to this page'
    return wrapper


@app.route('/')
@app.route('/index')
def index():
    session['current_url'] = request.path       # assigned to session to remember last page during login
    return render_template('index.html', description="Index Page")

# processes login attempts
# IN: get/post from form
# OUT: none
# CALLS: db_connect, assign_cursor, sql commands
@app.route('/login', methods=['GET', 'POST'])
def do_login() -> str:
    if request.method == 'POST':
        un = request.form['username']   # assign username and password from form to sql query
        pw = request.form['password']   # jinja2.escape(request.form['password']) breaks this
        sql_query = 'SELECT firstname, lastname FROM users WHERE username = "' + un + '" AND password = "' + pw + '";'

        with db_connect("database_code/conference.sqlite") as db:   # connect to db and execute query
            curs = assign_cursor(db)
            curs.execute(sql_query)
            admin_sql = curs.fetchall()

        if admin_sql == []:                             # test for empty match
            print('username and password not found')
            return redirect(session['current_url'])     # redirect back to original page

        print('Welcome ' + admin_sql[0][0])
        session['logged_in'] = True             # log in as admin
        session['fname'] = admin_sql[0][0]
        session['lname'] = admin_sql[0][1]
        return redirect('/admin')               # redirect to admin page

# logs out session
# IN: none
# OUT: none
# CALLS: session
@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'

# checks status of session
# IN: none
# OUT: none
# CALLS: session
@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are currently logged in.'
    return 'You are NOT logged in'


@app.route('/activities')
def activities():
    session['current_url'] = request.path
    return render_template('activities.html', description="Activities Page")

# checks if session is logged in before loading admin page
# IN: none
# OUT: none
# CALLS: session
@app.route('/admin')
@check_logged_in
def admin():
    session['current_url'] = request.path
    welcome = 'Welcome back ' + session['fname'] + ' ' + session['lname']
    return render_template('admin.html', description="Administration Page", welcome=welcome)

@app.route('/awards', methods=['GET', 'POST'])
def process_vote():
    session['current_url'] = request.path
    if request.method == 'POST':
        vote = 'You have voted for: ' + request.form['award_poll']
        return render_template('poll.html', vote=vote, description="Awards Page")
    else:
        return render_template('poll.html', description="Awards and Poll Page")

@app.route('/keynote')
def keynote():
    session['current_url'] = request.path
    return render_template('keynote.html', description="Keynote Page")

# processes user selected query for registrant lists
# IN: get/post from form
# OUT: none
# CALLS: db_connect, assign_cursor, sql commands
@app.route('/lists', methods=['GET', 'POST'])
def lists():
    session['current_url'] = request.path
    if request.method == 'POST':
        selected = request.form['reg_lists']
        if selected == 'list_all':
            sql_title = 'All Conference Registrants'
            sql_query = 'SELECT title, first_name, last_name FROM registration;'
        else:                                                                          # enter query for each column
            sql_query = 'SELECT title, first_name, last_name FROM registration ' \
                        'WHERE meals = "' + selected + \
                        '" OR session_1 = "' + selected + \
                        '" OR session_2 = "' + selected + \
                        '" OR session_3 = "' + selected + '" ORDER BY last_name;'
            if selected[0:8] == 'Workshop':                         # set title for each type of query
                sql_title = 'All Registrants taking ' + selected
            elif selected == 'mealpack':
                sql_title = 'All Registrants signed up for Full Meal Package '
            elif selected == 'dinnerday2':
                sql_title = 'All Registrants signed up for Second Dinner Only'

        with db_connect("database_code/conference.sqlite") as db:
            curs = assign_cursor(db)
            curs.execute(sql_query)
            reg_sql = curs.fetchall()
        # for k in reg_sql:
        #     print(tuple(k))
        return render_template('lists.html', description="Registrants List Page", reg_sql=reg_sql, sql_title=sql_title)
    else:
        print('1')
        return render_template('lists.html', description="Registrants List Page")

@app.route('/meals')
def meals():
    session['current_url'] = request.path
    return render_template('meals.html', description="Meals Page")

@app.route('/nametags8')
def nametags8():
    return render_template('nametags8.html')


@app.route('/nametags10')
def nametags10():
    return render_template('nametags10.html')

# processes registration form
# IN: get/post from form
# OUT: none
# CALLS: db_connect, assign_cursor, sql commands
@app.route('/registration', methods=['GET', 'POST'])
def process_registration():
    session['current_url'] = request.path
    if request.method == 'POST':
        id_num = jinja2.escape(request.form['confIDnum'])
        form_arr = [datetime.date.today(),
                    jinja2.escape(request.form['titleList']),               # jinja2.escape to protect the database
                    jinja2.escape(request.form['fname']), jinja2.escape(request.form['lname']),
                    jinja2.escape(request.form['street1']), jinja2.escape(request.form['street2']),
                    jinja2.escape(request.form['city']), jinja2.escape(request.form['stateList']),
                    jinja2.escape(request.form['zip']),
                    jinja2.escape(request.form['telephone']), jinja2.escape(request.form['email']),
                    jinja2.escape(request.form['company_web']), jinja2.escape(request.form['company_pos']),
                    jinja2.escape(request.form['company_name']),
                    jinja2.escape(request.form['meals']),
                    jinja2.escape(request.form['fname']),                   # pulled billing name
                    jinja2.escape(request.form['lname']),
                    'AA',                                                   # billing card type
                    random.randint(1000000000000000, 9999999999999999),     # random card number
                    random.randint(1000, 9999),                             # random CSV
                    random.randint(2021, 2026),                             # random exp year
                    random.randint(1, 12),                                  # random exp month
                    jinja2.escape(request.form['session1']), jinja2.escape(request.form['session2']),
                    jinja2.escape(request.form['session3'])]
        registration_template = '''INSERT INTO registration (
                                reg_date,title,first_name,last_name,add1,add2,city,st,zip,telephone,email,website,
                                co_position,co,meals,bill_first_name,bill_last_name,card_type,card_number,card_csv,
                                exp_year,exp_month,session_1,session_2,session_3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        with db_connect("database_code/conference.sqlite") as db:
            curs = assign_cursor(db)
            curs.execute(registration_template, form_arr)
        db.commit()  # force update database
        return render_template('thankyou.html', description="Thank You Page", form_arr=form_arr, id_num=id_num)
    else:
        return render_template('registration.html', description="Registration Page")

@app.route('/workshopschedule')
def workshopschedule():
    session['current_url'] = request.path
    return render_template('workshopschedule.html', description="Workshop Schedule Page")

@app.route('/error_b')
def error_b():
    error_msg = 'Session 1 - Reflectors has been selected, so no Session 2 workshops are available.'
    fix_msg = 'If you would like to attend a Session 2 workshop, please select a different Session 1 workshop.'
    return render_template('error.html', error_msg=error_msg, fix_msg=fix_msg, description="Error Page")

@app.route('/error_b3')
def error_b3():
    error_msg = 'Session 1 - Reflectors has been selected, so no Session 2 workshops are available, which must be taken' \
                ' with Session 3 - Processing'
    fix_msg = 'If you would like to attend Session 3 - Processing, please select a different Session 1 workshop.'
    return render_template('error.html', error_msg=error_msg, fix_msg=fix_msg, description="Error Page")

@app.route('/error_f')
def error_f():
    error_msg = 'Session 2 - Interference has been selected, so Session 3 - Processing must be taken.'
    fix_msg = 'If you would like to attend another Session 3 workshop, please select a different Session 2 workshop.'
    return render_template('error.html', error_msg=error_msg, fix_msg=fix_msg, description="Error Page")

@app.route('/error_h')
def error_h():
    error_msg = 'Session 3 - Processing has been selected, so Session 2 - Interference must be taken.'
    fix_msg = 'If you would like to attend another Session 2 workshop, please select a different Session 3 workshop.'
    return render_template('error.html', error_msg=error_msg, fix_msg=fix_msg, description="Error Page")

if __name__ == '__main__':
    app.run(debug=True)
