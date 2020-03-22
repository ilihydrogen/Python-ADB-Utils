import adb
import model.parameter
from model import parameter
from utils.const import *
from utils.class_utils import get_all_class_fields, py_access


class Config(dict):
    section_print_separator = '\\n'

    class __base_section__(dict):
        print_it = True

    class wireless(__base_section__):
        auto_connect = DEFAULT_AUTO_CONNECT
        wireless_address = DEFAULT_WIRELESS_ADDRESS

    class media(__base_section__):
        vibrate_on = True

    class display(__base_section__):
        execute_on_connect = DEFAULT_EXEC_ON_CONNECT
        command_to_execute = DEFAULT_CMD

    class adb(__base_section__):
        executable_path = "/usr/bin/adb"
        restart_on_error = False
        default_tcp_port = 5555

    def __init__(self, app_cfg) -> None:
        super().__init__()

        self.__initialize_from_configuration__(parameter.def_cfg, self)
        self.__initialize_from_configuration__(app_cfg, self)

        parameter.user_cfg = self

    @staticmethod
    def __initialize_from_configuration__(app_cfg, c, ignore_sections=None):
        if ignore_sections is None:
            ignore_sections = IGNORE_CONFIG_SECTIONS

        for sec in app_cfg.sections():
            if sec in ignore_sections: continue

            c[sec] = Config.__dict__[sec]()
            setattr(c, sec, c[sec])

            for sec_item in app_cfg.items(sec):
                c[sec][sec_item[0]] = Config.pre_process_value(sec_item)
                setattr(c[sec], sec_item[0], Config.pre_process_value(sec_item))
        for sec_item in app_cfg.items("global"):
            setattr(c, sec_item[0], Config.pre_process_value(sec_item))

            c[sec_item[0]] = Config.pre_process_value(sec_item)

    @staticmethod
    def pre_process_value(sec_item):
        data = sec_item[1]

        try:
            x = {}
            data = py_access("%s" % sec_item[1], x)
        except:
            pass

        if type(data) == type(bool()):
            return data

        return sec_item[1]
