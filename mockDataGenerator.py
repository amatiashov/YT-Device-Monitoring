import os
import json
import random
import logging
import shutil
from constants import RESOURCES_DIR


log = logging.getLogger(__name__)

DEVICES_DIR = os.path.join(RESOURCES_DIR, "devices")
MOCK_DATA_COUNT = int(os.environ.get("MOCK_DATA_COUNT", 30))


def clean_data():
    log.debug("Cleaning devices dir...")
    try:
        shutil.rmtree(DEVICES_DIR)
    except Exception as e:
        log.warning(str(e))


def create_environment():
    if not os.path.exists(DEVICES_DIR):
        log.debug("Creating %s" % DEVICES_DIR)
        os.makedirs(DEVICES_DIR)


def get_random_names():
    log.debug("Generating device names...")
    titles = set()
    while len(titles) < MOCK_DATA_COUNT:
        titles.add("Mock Device " + str(int(MOCK_DATA_COUNT * 1000 * random.random())))
    return list(titles)


def get_random_private_ip():
    private_ip = [str(random.choice([172, 192, 10]))]
    for _ in range(3):
        private_ip.append(str(random.randint(1, 254)))
    return ".".join(private_ip)


def generate_mock_data():
    clean_data()
    create_environment()
    for word in get_random_names():
        monitoring_state = random.choice(["enable", "disable"])
        with open(os.path.join(DEVICES_DIR, word + ".json"), "w") as f:
            f.write(json.dumps(dict(ip=get_random_private_ip(), name=word, monitoring=monitoring_state), indent=4))
