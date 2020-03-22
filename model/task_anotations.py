from typing import TypeVar, Callable
from media import *
from model.parameter import handle_module_event_sub_pool, register
from model.task_model import TaskInfo

Task = TypeVar("Task", bound=Callable)
A = TypeVar('A', str, bytes)

def entry(func: Task) -> Task:
    register(func.__module__, func, type='entry')
    return func

def module_summary(func: Task) -> Task:
    cat = func()
    register(func.__module__, cat, type='summary')
    return func

def handle_module_event(fun: Task) -> Task:
    handle_module_event_sub_pool.append(fun)
    return fun


"""

    category = None
    author = None
    version = None
    repository = None

"""


def call_subscribers(__name__, result, adb, task_info: TaskInfo):
    for sub in handle_module_event_sub_pool:
        for text_fragment in sub.__doc__.split(","):

            if text_fragment in __name__:
                print("Calling %s " % sub(result=result, task_info=task_info, adb=adb))
