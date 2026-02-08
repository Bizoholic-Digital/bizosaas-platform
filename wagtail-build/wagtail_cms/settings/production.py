from .base import *
import dj_database_url

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

DATABASES["default"] = dj_database_url.config(
    conn_max_age=600,
    ssl_require=True,
)
