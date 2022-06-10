# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/8 下午 5:49
import os
import platform

from starlette.config import Config

# 根目录
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
print(ROOT_PATH)

SYSTEM = platform.system().upper()
IS_FREEBSD = SYSTEM == "FREEBSD"
IS_LINUX = SYSTEM == "LINUX"
IS_WINDOWS = SYSTEM == "WINDOWS"
IS_DARWIN = SYSTEM == "DARWIN"

config = Config(
    env_file=os.path.join(ROOT_PATH, ".env"),
    environ=os.environ
)
#####################################################################################
#                                    全局配置 　　                                    ＃
#####################################################################################
SECRET_KEY = "__APP_SECRET_KEY__"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 60 minutes * 24 hours * 7 = 7 days
SERVER_HOST = config("SERVER_HOST", default="0.0.0.0")
SERVER_PORT = config("SERVER_PORT", cast=int, default=4443)
SERVER_WORKERS = config("SERVER_WORKERS", cast=int, default=1 if IS_WINDOWS or IS_DARWIN else 3)

PROJECT_NAME = "apschedule dashboard"
PROJECT_DESC = "apschedule dashboard api"
PROJECT_VERSION = "v0.1.0"
PROJECT_DEBUG = config("DEBUG", default=False)
PROJECT_DOCS_URL = "/docs"
PROJECT_REDOC_URL = "/redoc"
PROJECT_URL_PREFIX = "/api/v1"
# CORS
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=["*"])
# web静态文件路径
STATIC_RESOURCE_PATH = os.path.join(ROOT_PATH, "static")
SWAGGER_RESOURCE_PATH = os.path.join(ROOT_PATH, "swagger")
# ssl
SSL_KEYFILE = os.path.join(ROOT_PATH, "conf/ca/caprivate.key")
SSL_CERTFILE = os.path.join(ROOT_PATH, "conf/ca/cacert.crt")

#####################################################################################
#                                    平台配置 　　                                    ＃
#####################################################################################
if IS_WINDOWS or IS_DARWIN:
    # Just for developer
    PID_FILE = "../log/apschedule_dash.pid"
    APP_LOG_PATH = os.path.join(ROOT_PATH, "logs/apschedule_dash.log")
    APP_ACTION_LOG_PATH = os.path.join(ROOT_PATH, "logs/apschedule_dash_action.log")
    APP_REQUEST_LOG_PATH = os.path.join(ROOT_PATH, "logs/apschedule_dash_request.log")
    APP_RPC_LOG_PATH = os.path.join(ROOT_PATH, "logs/apschedule_dash_rpc.log")
    APP_ACCESS_LOG_PATH = os.path.join(ROOT_PATH, "logs/apschedule_dash_access.log")
    LOG_TO_STDERR = "true"
    LOG_LEVEL = "debug"
else:
    # config files
    PID_FILE = "/var/run/apschedule_dash.pid"
    APP_LOG_PATH = "/var/log/uxs/apschedule_dash.log"
    APP_ACTION_LOG_PATH = "/var/log/uxs/apschedule_dash_action.log"
    APP_REQUEST_LOG_PATH = "/var/log/uxs/apschedule_dash_request.log"
    APP_RPC_LOG_PATH = "/var/log/uxs/apschedule_dash_rpc.log"
    APP_ACCESS_LOG_PATH = os.path.join(ROOT_PATH, "/var/log/uxs/apschedule_dash_access.log")
    LOG_TO_STDERR = "true"
    LOG_LEVEL = "debug"
