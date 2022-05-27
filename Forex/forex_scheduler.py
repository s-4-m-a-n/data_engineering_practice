import redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import timedelta, datetime
import time
import redis_loader
from configparser import ConfigParser

# configs ----------------------
CONFIG_FILE = "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)
ENV  = config['ENV']['env']


# main -----------------------
def run():
    redis_cli = redis.Redis(host = config[ENV]['Host'],
                            port = config[ENV]['Port'])

    scheduler = Scheduler(connection = redis_cli)
    




if __name__ == "__main__":
    run()

