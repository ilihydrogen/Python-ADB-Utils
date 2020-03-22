import sys
from time import sleep

from adb import ADB
from model.configuration_model import Config
from model.task_anotations import *
from model.task_model import TaskInfo, Author

GITHUB_REPO_URL = "https://github.com/ilihydrogen/Python-ADB-Utils"

created_by = "iiihydrogen"
version = "1.0"


def reconnect(adb, cfg):
    address = cfg.wireless.wireless_address
    disconnect_client(adb, address)
    sleep(1)
    return connect_client(adb, address)


def connect_client(adb, address):
    return adb.connect_remote(host=address, port=5555)[0]


def disconnect_client(adb, address):
    print("Successfully disconnected from %s" % address if len(
        adb.disconnect_remote(host=address, port=5555)) == 0 else 'something was wrong')


@entry
def run_app(adb: ADB, cfg: Config):
    devices = adb.get_devices()[1]

    if len(devices) > 1:
        for device in devices:
            disconnect_client(adb, device)

    response = connect_client(adb, cfg.wireless.wireless_address)

    if response.startswith('unable'):
        return (response)
    elif "already" in response:

        if "-f" in sys.argv:
            response = reconnect(adb, cfg)
            return (response)
        else:
            if '-s' not in sys.argv: return ("Reconnect using -f if needed")

    elif response.startswith('connected to'):
        return ("Connection restored")
    else:
        return ("Unknown error: " + response)

@module_summary
def summary():
    info = TaskInfo("Device connection utility", Author(nickname=created_by), version, GITHUB_REPO_URL)
    return info
