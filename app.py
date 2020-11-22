import time
import logging
import datetime
import threading
from constants import *
from flask import Flask
from jinja2 import Template
from flask import make_response
from flask import send_from_directory
from mockDataGenerator import generate_mock_data
from services.discoveryService import DiscoveryService
from services.notificationService import NotificationService
from services.deviceRegistryService import DeviceRegistryService


if os.environ.get("LOG_MODE") == "prod":
    # logging in prod mode
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(
        format=u'%(threadName)s\t%(filename)s\t[LINE:%(lineno)d]# %(levelname)-8s\t [%(asctime)s]  %(message)s',
        level="INFO",
        handlers=[logging.FileHandler(os.path.join(LOG_DIR, "log.txt"), 'w', 'utf-8')])
else:
    # logging in dev mode
    logging.basicConfig(
        format=u'%(threadName)s\t%(filename)s\t[LINE:%(lineno)d]# %(levelname)-8s\t [%(asctime)s]  %(message)s',
        level="DEBUG")

log = logging.getLogger(__name__)

if os.environ.get("DEMO_MODE", "disable") == "enable":
    generate_mock_data()

notificationService = NotificationService.get_instance()
discoveryService = DiscoveryService.get_instance()
deviceRegistryService = DeviceRegistryService.get_instance()


def pretty_datetime(data):
    try:
        return datetime.datetime.fromtimestamp(data).strftime("%d.%m.%Y %H:%M:%S")
    except Exception as e:
        log.error("Cannot format for datetime: %s" % str(e))
    return "-"


def do_discovery():
    while True:
        try:
            discoveryService.discover_devices()
        except Exception as e:
            notificationService.notify("ERROR DISCOVERY! " + str(e))
        time.sleep(DISCOVERY_PERIOD_SEC)


threading.Thread(target=do_discovery, args=(), daemon=True).start()


app = Flask(__name__, static_url_path='/static', static_folder=os.path.join(WEB_DIR, "static"))


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def root():
    data_dto = dict(devices=deviceRegistryService.get_all_devices())
    for dev in data_dto.get("devices"):
        dev["last_discovery"] = pretty_datetime(dev.get("last_discovery"))
        dev["last_online"] = pretty_datetime(dev.get("last_online"))
    with open(os.path.join(WEB_DIR, "index.html")) as f:
        return make_response(Template(f.read()).render(**data_dto))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
