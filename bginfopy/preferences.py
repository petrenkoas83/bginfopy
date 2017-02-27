from os.path import expanduser
import subprocess
import configparser

# Default values
VERBOSE = True
USER_CONF_DIR = expanduser("~") + '/.bginfopy'
USER_CONF_FILE = 'bginfopy.ini'
SUFFIX = '_bginfopy'
ORIGINAL_WALLPAPER = ''
TEXT_GRAVITY = 'North'

# User configuration
# Try to create user conf dir
try:
    output = subprocess.check_output(["mkdir", "--verbose", "--parents", USER_CONF_DIR], stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as error:
    print("Error: '{0}': '{1}': '{2}'".format(error.returncode, error.output, error.message))
    exit()
else:
    if VERBOSE: print("Directory {0} successfully created or already exist: {1}: {2}".format(USER_CONF_DIR, output, subprocess.STDOUT))

# Try to read user config
config = configparser.ConfigParser()
if VERBOSE: print("User config file: {0}".format(USER_CONF_DIR + "/" + USER_CONF_FILE))
config.read(USER_CONF_DIR + "/" + USER_CONF_FILE)
if VERBOSE: print("User config contains sections: {0}".format(config.sections()))
if 'MAIN' in config.sections():
    if config['MAIN']['SUFFIX'] is not None:
        SUFFIX = config['MAIN']['SUFFIX']
        if VERBOSE: print("SUFFIX has been redefined to '{0}'".format(SUFFIX))
    if config['MAIN']['ORIGINAL_WALLPAPER'] is not None:
        ORIGINAL_WALLPAPER = config['MAIN']['ORIGINAL_WALLPAPER']
        if VERBOSE: print("ORIGINAL_WALLPAPER is '{0}'".format(ORIGINAL_WALLPAPER))
if 'TEXT' in config.sections():
    if config['TEXT']['GRAVITY'] is not None:
        TEXT_GRAVITY = config['TEXT']['GRAVITY']
        if VERBOSE: print("TEXT_GRAVITY has been redefined to '{0}'".format(TEXT_GRAVITY))