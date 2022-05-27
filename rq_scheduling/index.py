from flask import Flask, request
import redis
from rq import Queue
import time
from helper_functions import background_task
from datetime import timedelta
from rq_scheduler import Scheduler

app = Flask(__name__)
r = redis.Redis()
q = Queue(connection=r)
#scheduler = Scheduler(queue=q)

@app.route('/')
def hello_world():
	return "Hello world"

@app.route('/task')
def add_task():
	if request.args.get("n"):
		job = q.enqueue(background_task,request.args.get("n"))
		q_len = len(q)
		return f"Task{job.id} added to queue at {job.enqueued_at} {q_len} tasks in the queue"
	else:
		return "No value for n"
		
@app.route('/task_schedule')
def schedule_task():
	if request.args.get("n"):
		print(request.args.get("n"))
		job = q.enqueue_in(timedelta(seconds=int(request.args.get("n"))),background_task,request.args.get("n"))
		#job = scheduler.enqueue_in(timedelta(seconds=10),background_task,request.args.get("n"))
		q_len = len(q)
		return f"Task{job.id} added to queue at {job.enqueued_in} {q_len} tasks in the queue"
	else:
		return "No value for n"
		
		


if __name__ == "__main__":
	app.run()
