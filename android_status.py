#!/usr/bin/python3

import configparser
import os
import sys
import pyadb
from sys import path
from utils import v, CONF, arg

DEFAULT_AUTO_CONNECT = False
DEFAULT_WIRELESS_ADDRESS = "192.168.1.1"

DEFAULT_EXEC_ON_CONNECT = False
DEFAULT_CMD = '#'


class Config:
    class Wireless:
        auto_connect = DEFAULT_AUTO_CONNECT
        wireless_address = DEFAULT_WIRELESS_ADDRESS

        def __init__(self, auto_connect, wireless_address) -> None:
            super().__init__()
            self.auto_connect = auto_connect
            self.wireless_address = wireless_address

    class Display:
        execute_on_connect = DEFAULT_EXEC_ON_CONNECT
        command_to_execute = DEFAULT_CMD

        def __init__(self, execute_on_connect, command_to_execute) -> None:
            self.execute_on_connect = execute_on_connect
            self.command_to_execute = command_to_execute

    wireless_section = None
    display_section = None

    def __init__(self, wireless_section, display_section) -> None:
        super().__init__()
        self.wireless_section = wireless_section
        self.display_section = display_section


def config_init():
    def read_config():
        v("[%s] Reading configuration file" % CONF)

        config = configparser.ConfigParser()
        config.read(CONF, encoding="UTF-8")

        return Config(
            Config.Wireless(config['wireless']['auto_connect'], config['wireless']['wireless_address']),
            Config.Display(config['display']['execute_on_connect'], config['display']['command_to_execute'])
        )

    def create_default():
        v("[%s] Creating default configuration file" % CONF)

        config = configparser.ConfigParser()

        config['wireless']['auto_connect'] = 'no'
        config['wireless']['wireless_address'] = '192.168.1.1'

        config['display']['execute_on_connect'] = 'no'
        config['display']['command_to_execute'] = '#'

        with open(CONF, "w") as x: config.write(x)

    if not path.exists(CONF):
        create_default()

    return read_config()


def connect_adb(wireless_address):
    return pyadb.ADB().connect_remote(wireless_address)


def shell_adb(cmd):
    return pyadb.ADB().shell_command(cmd)


def main():
    app_cfg = config_init()
    if app_cfg.Wireless.auto_connect: connect_adb(app_cfg.Wireless.wireless_address)
    if app_cfg.Display.execute_on_connect: print(shell_adb(app_cfg.Display.command_to_execute))


if __name__ == '__main__':
    main()
