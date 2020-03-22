#!/usr/bin/python3

import traceback
from os import path

import model.parameter
from adb import ADB
from model import parameter, task_anotations
from model.task_model import TaskHelper
from utils.const import SAMPLE_CONFIG
from utils.utils import v, task_name
from utils.configuration import config_init, create_default, read_config
from model.configuration_model import Config
from media import notification, vibration


def adb_init():
    adb = ADB()

    adb.set_adb_path(parameter.variables.executable_path)

    adb.DEFAULT_TCP_PORT = parameter.variables.default_tcp_port
    adb.DEFAULT_TCP_HOST = parameter.variables.wireless_address

    if not adb.get_version():
        raise ConnectionError("Unable to communicate with adb daemon!")

    return adb


def reask(param, func):
    if input(param + " ").lower().startswith("y"):

        try:
            result = func()
            print(result)
            return False, result
        except Exception as e:
            exit(e)

    return True, None


def static_update(x):
    parameter.wireless_address = x.wireless.wireless_address
    parameter.command_to_execute = x.display.command_to_execute
    parameter.restart_on_error = x.adb.restart_on_error
    parameter.executable_path = x.adb.executable_path
    parameter.default_tcp_port = x.adb.default_tcp_port

    parameter.adb_wrapper.set_adb_path(x.adb.executable_path)
    parameter.adb_wrapper.DEFAULT_TCP_PORT = x.adb.default_tcp_port

    pass


def try_start_task(adb, x):
    h = TaskHelper(task_name)
    try:
        task_anotations.call_subscribers(h.__task_module__.__name__, h.start(adb, x), adb, h.task_info)
    except Exception as e:
        exit("Fallen. %s" % e)


def init_start(adb, cfg):
    # TODO Finish and test init
    pass


def main():
    try:
        adb = adb_init()
        parameter.adb_wrapper = adb
    except Exception as e:
        message = "%s: %s\nTry again? [y/N]" % (type(e).__name__, str(e.__traceback__))
        condition, adb = reask(message, adb_init)
        if condition:
            exit()

    x = None

    parameter.def_cfg = read_config(conf=SAMPLE_CONFIG)
    init = config_init()
    try:
        x = Config(init)
    except Exception as e:
        trace = 'Error on line %s (%s)' % (type(e).__name__, traceback.print_tb(e.__traceback__))
        message = trace + "\nWould you like to recreate configuration file? [y/N]"
        if reask(message, create_default):
            exit()
        else:
            x = Config(config_init())

    if not x or not adb:
        exit()

    static_update(x)
    init_start(adb, x)
    try_start_task(adb, x)


def connect_adb(wireless_address, adb=ADB()):
    v("Trying to connect to %s " % wireless_address)
    remote = adb.connect_remote(wireless_address)
    return remote[0] if remote and len(remote) > 0 else -1


def shell_adb(cmd, adb=ADB()):
    v("execute shell command: %s" % cmd)
    remote = adb.shell_command(cmd)
    return remote[0] if remote and len(remote) > 0 else -1


if __name__ == '__main__':
    main()
