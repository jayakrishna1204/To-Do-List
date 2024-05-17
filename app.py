# To-Do-List-Python-Flask-and-MySQL

from flask import Flask, request, render_template
from datetime import date
import pymysql
from werkzeug.utils import quote


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Krishna@1509#'
app.config['MYSQL_DB'] = 'to_do_list'

def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def gettasklist():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT task FROM tasks')
        task_rows = cursor.fetchall()
    conn.close()
    tasklist = [task['task'] for task in task_rows] if task_rows else []
    return tasklist

def createnewtasklist():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS tasks')
        cursor.execute('CREATE TABLE tasks(id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))')
    conn.commit()
    conn.close()

def updatetasklist(tasklist):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE tasks')
        for task in tasklist:
            cursor.execute('INSERT INTO tasks(task) VALUES (%s)', (task,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    datetoday2 = date.today().strftime("%d-%B-%Y")
    return render_template('home.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))

@app.route('/clear')
def clear_list():
    createnewtasklist()
    datetoday2 = date.today().strftime("%d-%B-%Y")
    return render_template('home.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))

@app.route('/addtask', methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
    conn.commit()
    conn.close()
    datetoday2 = date.today().strftime("%d-%B-%Y")
    return render_template('home.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))

@app.route('/deltask', methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = gettasklist()
    message = ''
    if task_index < 0 or task_index >= len(tasklist):
        message = 'Invalid Index'
    else:
        removed_task = tasklist.pop(task_index)
        updatetasklist(tasklist)
        message = 'Task removed successfully'
    datetoday2 = date.today().strftime("%d-%B-%Y")
    return render_template('home.html', datetoday2=datetoday2, tasklist=tasklist, l=len(tasklist), mess=message)

if __name__ == '__main__':
    app.run(debug=True)
