# from utils.anotations import GroupAdd
import os
import sys
from random import randint

from adb import ADB
from model.configuration_model import Config
from utils import io
from utils.utils import v

param_groups = dict()
groups = []

def_cfg = None
user_cfg = None
adb_wrapper = None

loc = dict()
handle_module_event_sub_pool = []


def register(module_name, func, type='entry'):
    if module_name not in loc.keys():
        loc[module_name] = {}

    loc[module_name].update({type: func})

def get_item(module_name, type='entry'):
    return loc[module_name][type]


class init:
    __initialization_modules__ = []

    on_pre_exec = lambda self, session: v('[%s] preInitialization' % session.init_id)
    on_post_exec = lambda self, session: v('[%s] postInitialization' % session.init_id)

    class InitSession:
        adb = None
        config = None
        code = None

        init_id = None

        pre = None
        post = None

    def commit(self):
        if self.pre(self) < 0: raise RuntimeError("[%s]: ".format(self.init_id).join("Pre init failed"))

        if self.code(self) < 0: raise RuntimeError("[%s]: ".format(self.init_id).join("initialization failed"))

        if self.post(self) < 0: raise RuntimeError("[%s]: ".format(self.init_id).join("Post init failed"))

    def with_init_id(self, session_id):
        self.init_id = session_id

    def add_to_list(self):
        init.__initialization_modules__.append(self)

    def __init__(self, code: staticmethod, adb=adb_wrapper, config=user_cfg) -> None:
        super().__init__()
        self.init_id = str(randint()).__hash__()
        self.adb = adb
        self.config = config
        self.code = code

        if not code:
            raise AttributeError("Init method object is invalid")

        self.pre = init.on_pre_exec
        self.post = init.on_post_exec

        self.add_to_list()


# noinspection PyRedeclaration,PyMethodMayBeStatic
class groups:

    def wipe_logs(self):
        """logs"""
        if os.path.isdir(variables.logs_directory):
            io.del_all_in_directory(variables.logs_directory)
        else:
            v('directory is not exists')

    def wipe_tmp(self):
        """directory"""
        if os.path.isdir(variables.tmp_directory):
            io.del_all_in_directory(variables.tmp_directory)
        else:
            v('directory is not exists')

    def observe_directories(self):
        """directory"""
        return [x for x in variables.__dict__ if "_directory" in x]

    def get_by_groups(self):
        """__"""
        result = {

        }

        exclude_by_docs = lambda x: x and not x.startswith("__")
        exclude_by_name = lambda x: not x.startswith("__")

        functions = [x for x in groups.__dict__ if exclude_by_docs(groups.__dict__[x].__doc__) and exclude_by_name(x)]

        for func in functions:
            result[groups.__dict__[func].__doc__] = []

        for func in functions:
            func = groups.__dict__[func]

            group = func.__doc__
            if group in result:
                result[group].append(func)

        return result


class variables:
    'argv'
    args = None

    'Get log files list'
    logs_files = None

    'Tasks version check'
    check_tasks_version = True

    'Address of device which need to be connected'
    wireless_address = -1

    'Automatic shell command on device connection'
    command_to_execute = -1

    'Restart adb if shell crash'
    restart_on_error = -1

    'Path to platform-tools with exe file'
    executable_path = '/usr/bin/adb'

    'Default adb tcp/ip port'
    default_tcp_port = -1

    'Tasks directory'
    tasks_directory = 'tasks/'

    'Resources directory'
    resources_directory = 'resources/'

    'Logs directory'
    logs_directory = 'logs/'

    'Temp directory'
    tmp_directory = 'tmp/'
