import configparser
from os.path import isfile

import model.parameter
from model import parameter
from utils.utils import v, CONF, dict_from_class
from model.configuration_model import Config
from utils.const import SAMPLE_CONFIG


def read_config(conf=CONF):
    v("[%s] Reading configuration file" % conf)

    config = configparser.ConfigParser()
    config.read(conf, encoding="UTF-8")

    return config


def create_default(conf=CONF):
    v("[%s] Creating default configuration file" % conf)

    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section('global')

    root_dict = dict()

    for x in (dict_from_class(Config)):
        class_ = Config.__dict__[x]
        if issubclass(class_.__class__, Config.__base_section__.__class__):
            from_class = dict_from_class(Config.__dict__['__base_section__'], class_)

            v("Adding section %s with %s fields" % (x, len(from_class)))
            config.add_section(x)

            config[x] = from_class
        else:
            root_dict.update(dict({x: Config.__dict__[x]}))

    config['global'] = root_dict

    config.add_section("INFO")
    version = parameter.adb_wrapper.get_version()
    state = parameter.adb_wrapper.get_state()[0]
    connection_state = ("device date: %s" % parameter.adb_wrapper.shell_command("date")[0]) if parameter.adb_wrapper.get_state()[0] == 'device' else "# Disconnected"

    text = '#\n#\n#\n# util for tweaking adb functionality\n#\n#\n#\n' \
           '# adb version: %s\n' \
           '# adb state: %s\n' \
           '# adb %s\n' \
           % (
                str(version),
                str(state),
                str(connection_state)
            )

    text += "#\n"
    text += "#\n"
    text += "#\n"

    config.set("INFO", "")
    config.set("INFO", text)

    with open(conf, "w") as x:
        config.write(x)


def config_init(conf=CONF):
    create_default(conf=SAMPLE_CONFIG)

    if not isfile(conf):
        create_default(conf=conf)

    return read_config(conf=conf)
