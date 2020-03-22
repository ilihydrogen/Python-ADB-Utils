from adb import ADB
from model.task_anotations import *
from model.task_model import TaskInfo, Author

GITHUB_REPO_URL = "https://github.com/ilihydrogen/Python-ADB-Utils"

created_by = "iiihydrogen"
version = "1.0"
adbx = ADB()

@entry
def run_app(adb, cfg):
    adbx = adb
    pass

@module_summary
def summary():
    return TaskInfo("test", Author(nickname=created_by), version, GITHUB_REPO_URL)
