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
VERBOSE = True
USER_CONF_DIR = expanduser("~") + '/.' + APP_NAME
USER_CONF_FILE = APP_NAME + '.ini'

# Ini values
SUFFIX = '_' + APP_NAME
USE_WALLPAPER_IMAGE = True
ORIGINAL_WALLPAPER_IMAGE = ''
BACKGROUND_COLOR = 'teal'  # white is too much
# TODO: move TEXT to config file so imagemagic read it from config
TEXT_LABEL = 'Test text'
TEXT_GRAVITY = 'North'

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

if 'SUFFIX' in config_main:
    SUFFIX = config['MAIN']['SUFFIX']
else:
    config.set('MAIN', 'SUFFIX', SUFFIX)

if 'USE_WALLPAPER_IMAGE' in config_main:
    USE_WALLPAPER_IMAGE = str2bool(config['MAIN']['USE_WALLPAPER_IMAGE'])
else:
    config.set('MAIN', 'USE_WALLPAPER_IMAGE', str(USE_WALLPAPER_IMAGE))

if 'ORIGINAL_WALLPAPER_IMAGE' in config_main:
    ORIGINAL_WALLPAPER_IMAGE = config['MAIN']['ORIGINAL_WALLPAPER_IMAGE']
else:
    config.set('MAIN', 'ORIGINAL_WALLPAPER_IMAGE', ORIGINAL_WALLPAPER_IMAGE)

### SECTION BACKGROUND ###
if 'BACKGROUND' not in config: config.add_section('BACKGROUND')
config_background = config["BACKGROUND"]

if 'COLOR' in config_background:
    BACKGROUND_COLOR = config_background['COLOR']
else:
    config.set('BACKGROUND', 'COLOR', BACKGROUND_COLOR)

### SECTION TEXT ###
if 'TEXT' not in config.sections(): config.add_section('TEXT')
config_text = config["TEXT"]

if 'GRAVITY' in config_text:
    TEXT_GRAVITY = config['TEXT']['GRAVITY']
else:
    config.set('TEXT', 'GRAVITY', TEXT_GRAVITY)

if 'TEXT_LABEL' in config_text:
    TEXT_LABEL = config_text['TEXT_LABEL']
else:
    config.set('TEXT', 'TEXT_LABEL', TEXT_LABEL)
