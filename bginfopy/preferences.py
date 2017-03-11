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
config = configparser.ConfigParser()
verboseprint("User config file: {0}".format(USER_CONF_DIR + "/" + USER_CONF_FILE))
config.read(USER_CONF_DIR + "/" + USER_CONF_FILE)
verboseprint("User config contains sections: {0}".format(config.sections()))

### SECTION MAIN ###
if 'MAIN' not in config: config.add_section('MAIN')
config_main = config["MAIN"]

if 'suffix' in config_main:
    MAIN_suffix = config_main['suffix']
else:
    MAIN_suffix = '_' + APP_NAME
    config_main.set('suffix', MAIN_suffix)

if 'use_wallpaper_image' in config_main:
    MAIN_use_wallpaper_image = str2bool(config_main['use_wallpaper_image'])
else:
    MAIN_use_wallpaper_image = True
    config_main.set('use_wallpaper_image', str(MAIN_use_wallpaper_image))

if 'original_wallpaper_image' in config_main:
    MAIN_original_wallpaper_image = config_main['original_wallpaper_image']
else:
    MAIN_original_wallpaper_image = ''
    config_main.set('original_wallpaper_image', MAIN_original_wallpaper_image)

### SECTION BACKGROUND ###
if 'BACKGROUND' not in config: config.add_section('BACKGROUND')
config_background = config["BACKGROUND"]

if 'color' in config_background:
    BACKGROUND_color = config_background['color']
else:
    BACKGROUND_color = 'teal'  # white is too much
    config_background.set('color', BACKGROUND_color)

### SECTION TEXT ###
if 'TEXT' not in config.sections(): config.add_section('TEXT')
config_text = config["TEXT"]

if 'gravity' in config_text:
    TEXT_gravity = config_text['gravity']
else:
    TEXT_gravity = 'North'
    config_text.set('gravity', TEXT_gravity)

if 'TITLE' in config_text:
    TEXT_title = config_text['title']
else:
    TEXT_title = 'Test text'
    config_text.set('title', TEXT_title)

### SECTION SHOW_INFO ###
if 'SHOW_INFO' not in config.sections(): config.add_section('SHOW_INFO')
config_show = config["SHOW_INFO"]

if 'hostname' in config_show:
    SHOW_hostname = str2bool(config_show['hostname'])
else:
    SHOW_hostname = True
    config_show.set['hostname'] = str(SHOW_hostname)

if 'dns_suffix' in config_show:
    SHOW_dns_suffix = str2bool(config_show['dns_suffix'])
else:
    SHOW_dns_suffix = True
    config_show.set['dns_suffix'] = str(SHOW_dns_suffix)

if 'interfaces' in config_show:
    SHOW_interfaces = config_show['interfaces']
else:
    SHOW_interfaces = '*'
    config_show.set['interfaces'] = SHOW_interfaces

if 'interface_ip' in config_show:
    SHOW_interface_ip = str2bool(config_show['interface_ip'])
else:
    SHOW_interface_ip = True
    config_show.set['interface_ip'] = str(SHOW_interface_ip)
