# it will load the data fetched through an API to the redix server
import redis
import forex_fetcher
from configparser import ConfigParser

# config ---
config = ConfigParser()
config.read('config.ini')
ENV = config['ENV']['env']


def start():
    # connecting to the redis server
    redis_client = redis.Redis(host=config[ENV]['Host'],
                               port=config[ENV]['Port'])

    # fetching data from API
    response = forex_fetcher.get()
    if response:  # success
        # store each key pair in the redix server
        for key, value in response.items():
            redis_client.set(key, value)

        print("redis database has been updated sucessfully")
    else:
        print("error fetching data from the API")


if __name__ == "__main__":
    start()
