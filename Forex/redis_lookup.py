import redis
from configparser import ConfigParser

# config
config = ConfigParser()
config.read("config.ini")
ENV = config['ENV']['env']


def lookup_forex(From="USD", To="NPR"):
    """Will retrieve the forex rate from the redis server and return it."""
    # connecting to the redis server
    redis_cli = redis.Redis(host=config[ENV]['Host'],
                            port=config[ENV]['Port'])
    if From == "USD":
        redis_key = From+To  # an instence of redis key "USDNRP"

        forex_rate = float(redis_cli.get(redis_key))
    elif To == "USD":
        redis_key = To+From
        forex_rate = 1 / float(redis_cli.get(redis_key))

    return forex_rate


if __name__ == "__main__":
    print(lookup_forex())
