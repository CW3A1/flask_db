from flask import Flask, jsonify, redirect, url_for
import uuid, database, environment

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

# TASK ENDPOINTS
@app.route('/api/task/list')
def listTask():
    return jsonify(database.listTask())

@app.route('/api/task/add')
def addTask():
    task_id = str(uuid.uuid4())[:8]
    return jsonify(database.addTask(task_id))

@app.route('/api/task/complete/<task_id>')
def completeTask(task_id):
    return jsonify(database.completeTask(task_id))

@app.route('/api/task/status/<task_id>')
def statusTask(task_id):
    return jsonify(database.statusTask(task_id))

# SCHEDULER ENDPOINTS
@app.route('/api/scheduler/list')
def listScheduler():
    return jsonify(database.listScheduler())

@app.route('/api/scheduler/free/<pc>')
def freeScheduler(pc):
    return jsonify(database.freeScheduler(pc))

@app.route('/api/scheduler/busy/<pc>')
def busyScheduler(pc):
    return jsonify(database.busyScheduler(pc))

@app.route('/api/scheduler/status/<pc>')
def statusScheduler(pc):
    return jsonify(database.statusScheduler(pc))

# @app.route('/api/pushurl/<id>/<status>')
# def pushJSONtoDB(id, status):
#     if request.args.get('secret')==environment.db_secret:
#         if id not in (None, "") and status not in (0, 1):
#             resp = requests.get(f"{environment.db_url}/api/column/id")
#             print(id, resp.json(), id not in resp.json())
#             if id not in resp.json():
#                 requests.post(f"{environment.db_url}/api/push", json={"id": int(id), "status": int(status)})
#                 return redirect(url_for('showAPI'))
#             return jsonify({"error": "id must be unique"})
#         return jsonify({"error": "invalid id or status provided"})
#     return jsonify({"error": "invalid secret provided"})