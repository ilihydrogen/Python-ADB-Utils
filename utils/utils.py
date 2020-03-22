import argparse

from model import parameter

CONF = 'config.conf'

parser = argparse.ArgumentParser(description='Util for ADB', allow_abbrev=True)
parser.add_argument('-c', '--config',
                    action="store", type=str, required=False,
                    help="Custom configuration file", default="config.conf")

parser.add_argument("-v", "--verbose", action="store_true",
                    required=False, help="Make output more shitty"
                    )

parser.add_argument("-f", action="store_true",
                    required=False, help="Force flag", dest='mforce'
                    )

parser.add_argument("-s", action="store_true",
                    required=False, help="Be silent", dest='msilent'
                    )

# parser.prefix_chars += 't'
# parser.add_('t' 'tasks', action='store', required=True,
#                     help='select tasks to execute', default='info', dest='tasks')

parser.add_argument('-t', '--tasks',
                    action="store", type=str, required=False,
                    help="Execute tasks(s)", dest="task")

args = parser.parse_args()

_verbose = args.verbose
CONF = args.config
task_name = args.task
parameter.args = args


def v(msg):
    if _verbose: print(msg)


def dict_from_class(*cls):
    def extract_dict(cls):
        return dict((key, value) for (key, value) in cls.__dict__.items() if "__" not in key)

    if len(cls) == 1:
        return extract_dict(cls[0])
    else:
        result = dict()
        for dictionary in cls:
            result.update(extract_dict(dictionary))
        return result
