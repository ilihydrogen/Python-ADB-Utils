import sys
import argparse

CONF = 'config.conf'

parser = argparse.ArgumentParser(description='Util for ADB')
parser.add_argument('config', action="store", type=str)

args = parser.parse_args()
arg = lambda key, default: args[key] if key in args else None

_verbose = '-v' in sys.argv
CONF = arg("config", CONF)


def v(msg):
    if _verbose: print(msg)
