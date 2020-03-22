from model.parameter import adb_wrapper
from model.task_anotations import handle_module_event
from sh import shell


@handle_module_event
def vibrate_on_connect(task_info=None, result=None, adb=None):
    """connect_device"""
    shell('adb shell \'su -c \"echo 500 > /sys/class/timed_output/vibrator/enable\"\'')

