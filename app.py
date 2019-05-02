from flask import Flask, render_template, request
import os
import sqlite3
import threading
import time
import uuid

def worker():
    while True:
        time.sleep(12)
        with sqlite3.connect('database.db') as conn:
            for row in conn.execute('SELECT * FROM tasks WHERE resource IS NULL'):
                conn.execute(f'UPDATE tasks SET resource = "Hello user:{row[1]} your task: {row[0]} has been completed" WHERE id=?', [row[0]])

t1 = threading.Thread(target=worker)
t1.start()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/long-task/<task_id>', methods=['get'])
def read_long_task(task_id):
    result = None
    with sqlite3.connect('database.db') as conn:
        result = conn.execute('SELECT resource FROM tasks WHERE id=?', [task_id]).fetchone()
    if result[0]:
        return result[0], 200
    else:
        return task_id, 202

@app.route('/long-task', methods=['POST'])
def create_long_task():
    task_id = str(uuid.uuid4())
    status = 202
    try:
        conn = sqlite3.connect('database.db')
        with conn:
            sql_string = f'INSERT INTO tasks VALUES ("{task_id}", "{str(request.headers["User-Id"])}", NULL)'
            conn.execute(sql_string)
    except sqlite3.DatabaseError as error:
        status = 500
    finally:
        conn.close()
    
    if(status == 202):
        return task_id, status
    else:
        return "There has been an error", status

if __name__ == "__main__":

    try: 
        try:
            conn = sqlite3.connect('database.db')
            with conn:
                conn.execute('CREATE TABLE tasks (id CHAR(36) PRIMARY KEY, user CHAR(36) NOT NULL, resource TEXT)')
        finally:
            conn.close()

        app.run()
    finally:
        if os.path.isfile('database.db'):
            os.remove('database.db')