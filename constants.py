import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
WEB_DIR = os.path.join(RESOURCES_DIR, "web")
LOG_DIR = os.path.join(BASE_DIR, "log")

OFFLINE_STATE = "offline"
ONLINE_STATE = "online"

DISCOVERY_PERIOD_SEC = int(os.environ.get("DISCOVERY_PERIOD_SEC", default=30))
