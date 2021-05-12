from flask import Flask, session, request, redirect, url_for, jsonify

app = Flask(__name__)
# Psuedo secret key
app.secret_key = 'aV3rYs3crE+key'

# Psuedo database / tables
dict_user = {}
dict_task = {}

@app.route('/')
def success():
    return 'Welcome, %s!' % session['username']

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if username in dict_user:
        return jsonify('Username already exists'), 403
    else:
        dict_user[username] = password
        dict_task[username] = []
        return jsonify('Account registered'), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if verify_credentials(username, password):
        session['username'] = username
        return redirect(url_for('success')) # TODO: Return access token

    return jsonify('Incorrect username / password'), 403

@app.route('/task', methods=['GET', 'POST', 'PUT', 'DELETE'])
def task():   
    if session.get('username') == None:
        return jsonify('Not logged in'), 401

    username = session['username']

    # List all tasks of current user
    if request.method == 'GET':        
        if username in dict_task:
            return jsonify(dict_task[username])
        return jsonify('User not found'), 404

    # Add task
    if request.method == 'POST':
        task_name = request.form['task_name']
        if task_name not in dict_task[username]:
            dict_task[username].append(task_name)
            return jsonify('Task added'), 201
        return jsonify('Task already exists. Task name must be unique'), 403

    # Update task
    if request.method == 'PUT':        
        task_name_prev = request.form['task_name_prev']
        task_name_new = request.form['task_name_new']  
        if task_name_new in dict_task[username]:
            return jsonify('New task already exists. Task name must be unique'), 403
        if task_name_prev in dict_task[username]:
            index = dict_task[username].index(task_name_prev)
            dict_task[username][index] = task_name_new
            return jsonify('Task updated')
        return jsonify('Task does not exist'), 404

    # Delete task
    if request.method == 'DELETE':
        task_name = request.form['task_name']
        if task_name in dict_task[username]:
            dict_task[username].remove(task_name)
            return jsonify('Task deleted')
        return jsonify('Task does not exist'), 404

@app.route('/task/move', methods=['PUT'])
def move_task():
    if session.get('username') == None:
        return jsonify('Not logged in'), 401

    username = session['username']
    task_name = request.form['task_name']
    index = int(request.form['index'])

    if task_name in dict_task[username]:
        if index < len(dict_task[username]):
            dict_task[username].remove(task_name)
            dict_task[username].insert(index, task_name)
            return jsonify('Task moved')
        return jsonify('Index should be less than list size'), 403
    return jsonify('Task does not exist'), 404

def verify_credentials(username, password):
    if username in dict_user and password == dict_user[username]:
        return True
    return False