print(" ██╗   ██╗██████╗  ██████╗")
print(" ██║   ██║██╔══██╗██╔════╝")
print(" ██║   ██║██████╔╝██║     ")
print(" ██║   ██║██╔══██╗██║     ")
print(" ╚██████╔╝██████╔╝╚██████╗")
print("  ╚═════╝ ╚═════╝  ╚═════╝")

# load the logging configuration
import logging
from logging.config import fileConfig
fileConfig('config/logging.ini')

# make default logfile
from datetime import datetime
root = logging.getLogger()
fh = logging.FileHandler(datetime.now().strftime('logs/%Y-%m-%d.log'))
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
root.addHandler(fh)

# load the config file
from configparser import ConfigParser
_config = ConfigParser(interpolation=None)
_config.read('config/config.ini')
_ENV = _config['default']['env']

# create SMApply instance
from util.api.smapply import SMApplyInstance
_smapply = None
def get_smapply_instance():
    global _smapply
    if not _smapply:
        _smapply = SMApplyInstance()
    return _smapply
