import subprocess
import sys
from os.path import expanduser

import configparser


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
config = configparser.ConfigParser()
verboseprint("User config file: {0}".format(USER_CONF_DIR + "/" + USER_CONF_FILE))
config.read(USER_CONF_DIR + "/" + USER_CONF_FILE)
verboseprint("User config contains sections: {0}".format(config.sections()))

### SECTION MAIN ###
if 'MAIN' not in config:
    config.add_section('MAIN')
config_main = config["MAIN"]
MAIN_suffix                   = config_main.get('suffix', fallback = '_{0}'.format(APP_NAME))
MAIN_original_wallpaper_image = config_main.get('original_wallpaper_image', fallback = '')
MAIN_use_wallpaper_image      = config_main.getboolean('use_wallpaper_image', fallback = True)

### SECTION BACKGROUND ###
if 'BACKGROUND' not in config:
    config.add_section('BACKGROUND')
config_background = config["BACKGROUND"]
BACKGROUND_color = config_background.get('color', fallback = 'teal')

### SECTION TEXT ###
if 'TEXT' not in config.sections():
    config.add_section('TEXT')
config_text = config["TEXT"]
TEXT_gravity = config_text.get('gravity', fallback = 'North')
TEXT_title   = config_text.get('title', fallback = 'Test text')

### SECTION SHOW_INFO ###
if 'SHOW_INFO' not in config.sections():
    config.add_section('SHOW_INFO')
config_show = config["SHOW_INFO"]
SHOW_hostname     = config_show.getboolean('hostname', fallback = True)
SHOW_dns_suffix   = config_show.getboolean('dns_suffix', fallback = True)
SHOW_interfaces   = config_show.get('interfaces', fallback = '*')
SHOW_interface_ip = config_show.getboolean('interface_ip', fallback = True)
