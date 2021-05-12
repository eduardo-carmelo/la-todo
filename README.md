# la-todo

Notes:
1. Database is implemented as dictionary
2. Secret key is hard-coded
3. User access token not implemented

Instructions:
1. Install Python
2. Install requirements.txt
3. Set FLASK_APP to todo.py
    a. (Windows) set FLASK_APP = "todo.py" 
    b. (Linux) export FLASK_APP = "todo.py"
    c. (Powershell) $env:FLASK_APP = "todo.py"
4. Execute "flask run"

End points:
1. /register

POST
Parameters:
username
password

2. /login

POST
Parameters:
username
password

3. /task

GET
Return:
Lists all tasks of current user

POST
Parameters:
task_name - Task to add

PUT
Parameters:
task_name_prev - Task to update
task_name_new - Updated task name

DELETE
Parameters:
task_name - Task to delete

4. /task/move

PUT
Parameters:
task_name - Task to move
index - New position to move to