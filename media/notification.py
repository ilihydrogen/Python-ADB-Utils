import os
from typing import Callable, TypeVar

from adb import ADB
from model.parameter import adb_wrapper
from model.task_anotations import handle_module_event
from model.task_model import TaskInfo
from sh import shell

Task = TypeVar("Task", bound=Callable)


@handle_module_event
def notify_send(task_info=None, result=None, adb=None):
    """connect_device"""
    shell('notify-send -t 5 "%s" "%s - Battery charge: %s"' % (task_info.category, result, adb.get_battery_level()))
