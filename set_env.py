#!/usr/bin/env python
"""Django's command-line utility for settings up environment file."""
import base64
import os
import secrets
from pathlib import Path
from typing import Literal, Union

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_PATH = Path(__file__).resolve().parent


ENVIRONMENT_PARAMETERS = [
    "DEBUG",
    "ALLOWED_HOSTS",
    "SECRET_KEY",
    "SIGNING_KEY",
    "DB_ENGINE",
    "DB_NAME",
    "DB_HOST",
    "DB_USER",
    "DB_PASS",
    "MEMCACHED_HOST",
    "MEMCACHED_PORT",
    "REDIS_HOST",
    "REDIS_PORT",
    "RABBITMQ_HOST",
    "RABBITMQ_PORT",
    "RABBITMQ_USER",
    "RABBITMQ_PASSWORD",
    "RABBITMQ_VHOST",
    "BROKER_NAME",
    "CORS_ALLOWED_ORIGINS",
    "FRONTEND_URL",
    "PROCFILE",
]

ENVS = Literal["development", "production"]


def create_environment_file(env: ENVS = None):
    if env is None:
        env = "development"

    SECRET_KEY = base64.b64encode(secrets.token_bytes(32)).decode("utf-8")
    SIGNING_KEY = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")

    defaults = {
        "DEBUG": 1 if env != "production" else 0,
        "SECRET_KEY": SECRET_KEY,
        "SIGNING_KEY": SIGNING_KEY,
        "PROCFILE": "Procfile",
        "BROKER_NAME": "rabbitmq",  # or redis
        "RABBITMQ_HOST": "localhost" if env != "production" else "",
        "RABBITMQ_PORT": 5672,
        "RABBITMQ_USER": "guest" if env != "production" else "",
        "RABBITMQ_PASSWORD": "guest" if env != "production" else "",
        "RABBITMQ_VHOST": "/" if env != "production" else "",
        "MEMCACHED_HOST": "localhost" if env != "production" else "",
        "MEMCACHED_PORT": 11211,
        "REDIS_PORT": 6379,
        "REDIS_HOST": "localhost" if env != "production" else "",
        # for react:
        "ALLOWED_HOSTS": "*" if env != "production" else "",
        "CORS_ALLOWED_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000"
        if env != "production"
        else "",
    }

    env_params = {key: defaults.get(key, "") for key in ENVIRONMENT_PARAMETERS}

    with open(f".env.{env}", "w") as output:
        for key, value in env_params.items():
            output.write(f"{key}={value}\n")


def build_path(*chunks):
    str_chunks = [str(chunk) for chunk in chunks]
    return os.path.join(*str_chunks)


def create_symlink(src_dir: Union[Path, str], env: ENVS = None):
    if env is None:
        env = "development"

    src = build_path(src_dir, f".env.{env}")
    dst = build_path(src_dir, ".env")

    if os.path.exists(dst):
        os.unlink(dst)

    os.symlink(
        src=src,
        dst=dst,
    )


if __name__ == "__main__":
    import sys

    try:
        env = sys.argv[1]
    except IndexError:
        env = None

    try:
        src_dir = sys.argv[2]
    except IndexError:
        src_dir = BASE_PATH

    create_environment_file(env=env)
    create_symlink(env=env, src_dir=src_dir)
