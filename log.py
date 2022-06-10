# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 6:45
import logging
import logging.config
import sys
from copy import copy

import click

import settings

TRACE_LOG_LEVEL = 5


class ColourizedFormatter(logging.Formatter):
    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(str(level_name), fg="blue"),
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"),
        logging.CRITICAL: lambda level_name: click.style(str(level_name), fg="bright_red"),

    }

    def __init__(self, fmt=None, datefmt=None, style="%", use_colors=None):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_message(self, level_no, message):
        def default(message):
            return str(message)

        func = self.level_name_colors.get(level_no, default)
        return func(message)

    def should_use_colors(self):
        return True

    def formatMessage(self, record):
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        seperator = " " * (8 - len(recordcopy.levelname))
        if self.use_colors:
            recordcopy.__dict__["message"] = self.color_message(record.levelno, recordcopy.getMessage())
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        return super().formatMessage(recordcopy)


DEFAULT_LOG_FMT = "[%(asctime)s %(levelname)-5.5s %(module)s:%(lineno)d] %(message)s"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "fmt": DEFAULT_LOG_FMT,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(asctime)s %(client_addr)s - \"%(request_line)s\" %(status_code)s",  # noqa: E501
        },
        "color": {
            "()": "log.ColourizedFormatter",
            "fmt": DEFAULT_LOG_FMT,
            "use_colors": True,
        }
    },
    "handlers": {
        "access_log": {
            "formatter": "access",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": settings.APP_ACCESS_LOG_PATH,
            "maxBytes": 10 * 1024 * 1024,  # 10 MiB
            "backupCount": 10,
        },
        "app_log": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": settings.APP_LOG_PATH,
            "maxBytes": 10 * 1024 * 1024,  # 10 MiB
            "backupCount": 10,
        },
        "request_log": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": settings.APP_REQUEST_LOG_PATH,
            "maxBytes": 10 * 1024 * 1024,  # 10 MiB
            "backupCount": 10,
        },
        "console_log": {
            "formatter": "color",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["app_log"],
            "level": "INFO",
        },
        "uvicorn.error": {
            "handlers": ["app_log"],
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["access_log"],
            "level": "INFO",
            "propagate": False
        },
        "request": {
            "handlers": ["request_log"],
            "level": "INFO",
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["app_log", "console_log"]
        },
    },
}

# logger for internal use
uvicorn_log = logging.getLogger("uvicorn")

app_log = logging.getLogger()
action_log = logging.getLogger("action")
request_log = logging.getLogger("request")


def log_init(log_to_stderr: str, log_level: str = "debug"):
    LOGGING_CONFIG["loggers"]["root"]["level"] = log_level.upper()
    if log_to_stderr.lower() not in ("true", "1", "yes"):
        root_handlers = LOGGING_CONFIG["loggers"]["root"]["handlers"]
        if "console_log" in root_handlers:
            root_handlers.remove("console_log")  # noqa
    logging.config.dictConfig(LOGGING_CONFIG)
