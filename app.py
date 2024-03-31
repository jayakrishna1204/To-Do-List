# To-Do-List-Python-Flask-and-MySQL

import os
from flask import Flask,request,render_template
from datetime import date
from flask_mysqldb import MySQL

# Defining To-Do List Flask App
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = '*****'
app.config['MYSQL_PASSWORD'] = '*****'
app.config['MYSQL_DB'] = 'to_do_list'

mysql = MySQL(app)

# Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


# def gettasklist():
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT * FROM tasks')
#     tasklist = cur.fetchall()
#     cur.close()
#     tasklist = []
#     if task_rows:
#         tasklist = [task[0] for task in task_rows]
#     return tasklist

def gettasklist():
    cur = mysql.connection.cursor()
    cur.execute('SELECT task FROM tasks')
    task_rows = cur.fetchall()
    cur.close()

    tasklist = [task[0] for task in task_rows] if task_rows else []  
    # Convert fetched data into a list or return an empty list

    return tasklist


def createnewtasklist():
    cur = mysql.connection.cursor()
    cur.execute('DROP TABLE IF EXISTS tasks')
    cur.execute('CREATE TABLE tasks(id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))')
    mysql.connection.commit()
    cur.close()

def updatetasklist(tasklist):
    cur = mysql.connection.cursor()
    cur.execute('TRUNCATE TABLE tasks')
    for task in tasklist:
        cur.execute('INSERT INTO tasks(task) VALUES (%s)', (task,))
    mysql.connection.commit()
    cur.close()

# Other functions remain the same but update the operations according to the database


################## ROUTING FUNCTIONS #########################

# Our main page
@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


# Function to clear the to-do list
@app.route('/clear')
def clear_list():
    createnewtasklist()
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


# Function to add a task to the to-do list
@app.route('/addtask', methods=['POST'])
def add_task():
    task = request.form.get('newtask')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    mysql.connection.commit()
    cur.close()

    return render_template('home.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))

# Function to remove a task from the to-do list
@app.route('/deltask', methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = gettasklist()
    message = ''  # Initialize an empty message
    if task_index < 0 or task_index >= len(tasklist):
        message = 'Invalid Index'
    else:
        removed_task = tasklist.pop(task_index)
        updatetasklist(tasklist)
        message = 'Task removed successfully'
    
    return render_template('home.html', datetoday2=datetoday2, tasklist=tasklist, l=len(tasklist), mess=message)


# Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
