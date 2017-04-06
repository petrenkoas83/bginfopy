import subprocess
import sys
from os.path import expanduser

import configparser


def str2bool(string):
    # type: (str) -> bool
    return string.lower() in ("yes", "true", "y", "1")


# http://stackoverflow.com/questions/5980042/how-to-implement-the-verbose-or-v-option-into-a-script
def verboseprint(message):
    if VERBOSE:
        print message
    else:
        pass


# Default values
APP_NAME = 'bginfopy'
# TODO: https://docs.python.org/2/library/logging.html
VERBOSE = True
USER_CONF_DIR = expanduser("~") + '/.' + APP_NAME
USER_CONF_FILE = APP_NAME + '.ini'


# User configuration
# Try to create user conf dir
try:
    output = subprocess.check_output(["mkdir", "--verbose", "--parents", USER_CONF_DIR], stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as error:
    sys.exit("Error: '{0}': '{1}': '{2}'".format(error.returncode, error.output, error.message))
else:
    verboseprint(
        "Directory {0} successfully created or already exist: {1}: {2}".format(USER_CONF_DIR, output,
                                                                               subprocess.STDOUT))
# Try to read user config
# TODO: use by default main config file /etc/bginfopy. Use user config file only if allowed at main config.
config = configparser.ConfigParser()
verboseprint("User config file: {0}".format(USER_CONF_DIR + "/" + USER_CONF_FILE))
config.read(USER_CONF_DIR + "/" + USER_CONF_FILE)
verboseprint("User config contains sections: {0}".format(config.sections()))

### SECTION MAIN ###
if 'MAIN' not in config:
    config.add_section('MAIN')
config_main = config["MAIN"]
config['MAIN']['suffix']                   = config_main.get('suffix', fallback = '_{0}'.format(APP_NAME))
config['MAIN']['original_wallpaper_image'] = config_main.get('original_wallpaper_image', fallback = '')
config['MAIN']['use_wallpaper_image']      = config_main.get('use_wallpaper_image', fallback = 'False')

### SECTION BACKGROUND ###
if 'BACKGROUND' not in config:
    config.add_section('BACKGROUND')
config_background = config["BACKGROUND"]
config['BACKGROUND']['color'] = config_background.get('color', fallback = 'teal')

### SECTION TEXT ###
if 'TEXT' not in config.sections():
    config.add_section('TEXT')
config_text = config["TEXT"]
config['TEXT']['gravity'] = config_text.get('gravity', fallback = 'NorthEast')
config['TEXT']['title']   = config_text.get('title', fallback = 'Please provide this info to tech support')

### SECTION SHOW ###
if 'SHOW' not in config.sections():
    config.add_section('SHOW')
config_show = config["SHOW"]
config['SHOW']['hostname']     = config_show.get('hostname', fallback = 'True')
verboseprint("config['SHOW']['hostname'] = {0}".format(config['SHOW']['hostname']))
config['SHOW']['dns_suffix']   = config_show.get('dns_suffix', fallback = 'True') # TODO
config['SHOW']['interfaces']   = config_show.get('interfaces', fallback = '*') # TODO
config['SHOW']['interface_ip'] = config_show.get('interface_ip', fallback = 'True')
