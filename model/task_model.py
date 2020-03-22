import importlib

from model.parameter import variables, get_item


# tasks_directory, adb_wrapper, user_cfg


class Processable:
    object_type = None
    object_value = None

    def __init__(self, type, value) -> None:
        super().__init__()

        self.object_type = type
        self.object_value = value


class Author:
    nickname = None
    email = None

    def __init__(self, nickname=None, email=None) -> None:
        super().__init__()
        self.email = email
        self.nickname = nickname


class TaskInfo:
    category = None
    author = None
    version = None
    repository = None

    def __init__(self, cat, au, ver, repo) -> None:
        super().__init__()

        self.category = cat
        self.author = au
        self.version = ver
        self.repository = repo


class TaskHelper:
    __task_filename__ = None
    __task_module__ = None

    task_filename = None
    task_info = None

    def __init__(self, task_filename, mask='tasks') -> None:
        super().__init__()

        __task_filename__ = self.__get_info__(task_filename)
        self.__task_module__ = importlib.import_module(__task_filename__)
        self.task_info = self.get_info()
        self.start = get_item(self.__task_module__.__name__)

        # self.start = self.task_info.start_func_name

    def __get_info__(self, task_filename):
        mask = variables.tasks_directory
        self.task_filename = task_filename

        self.__task_filename__ = __task_filename__ = "%s/%s" % (
            mask if not mask.endswith('/') else mask[:-1], task_filename)
        return __task_filename__.replace("/", ".")

    def reload(self):
        reload = importlib.reload(self.__task_filename__)
        self.__task_module__ = reload
        return reload

    def get_info(self):
        return get_item(self.__task_module__.__name__, type='summary')
