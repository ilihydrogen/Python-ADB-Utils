import os
from os import path

from utils.utils import v


def del_all_in_directory(dirpath):
    v('deleting %s ...')
    for file in os.listdir(dirpath):
        os.remove(file)
        v('%s%sremoved!' % (file, ' ' if path.exists(file) else ' not '))
