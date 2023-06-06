import os

from dotenv import load_dotenv

load_dotenv()

HOST_IP = os.environ.get("APP_HOST", "0.0.0.0")
HOST_PORT = os.environ.get("APP_PORT", "8000")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = os.environ.get("DEBUG", "True")

LOGGER_SETTINGS = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "statistics": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}

connection = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    os.environ.get("DB_USERNAME"),
    os.environ.get("DB_PASSWORD"),
    os.environ.get("DB_HOST"),
    os.environ.get("DB_PORT"),
    os.environ.get("DB_DATABASE"),
)

psycopg2_connection = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
    os.environ.get("DB_USERNAME"),
    os.environ.get("DB_PASSWORD"),
    os.environ.get("DB_HOST"),
    os.environ.get("DB_PORT"),
    os.environ.get("DB_DATABASE"),
)

INSTANCES_SOCIAL_ENDPOINT = os.environ.get("INSTANCES_SOCIAL_ENDPOINT")
INSTANCES_SOCIAL_SECRET = os.environ.get("INSTANCES_SOCIAL_SECRET")

INSTANCES_SOCIAL_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + INSTANCES_SOCIAL_SECRET
}

MASTODON_INSTANCE_ENDPOINT = os.environ.get("MASTODON_INSTANCE_ENDPOINT")
MASTODON_INSTANCE_ACCESS_TOKEN = os.environ.get("MASTODON_INSTANCE_ACCESS_TOKEN")

# retrieve alive, open to register and with min number of active users mastodon instances
MASTODON_UPDATE_INSTANCE_ENDPOINT = INSTANCES_SOCIAL_ENDPOINT + "/instances/list?include_closed=false&count=0&min_active_users=500&include_down=false"

# retrieve the list of current trends
MASTODON_SOCIAL_TRENDS_ENDPOINT = MASTODON_INSTANCE_ENDPOINT + "/api/v1/trends/tags?limit=20"

# application secret key
APP_SECRET = os.environ.get("APP_SECRET")

# fast mode
SANIC_FAST = os.environ.get("SANIC_FAST", "True") == "True"
