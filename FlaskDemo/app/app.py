
import redis
from flask import Flask

app = Flask(__name__)
redisClient = redis.Redis(host='redis_abc', port=6379)

@app.route('/')
def hello():
    redisClient.set("name","Suman Dhakal")

    return 'Hello World! hahahah {}'.format(redisClient.get("name"))

