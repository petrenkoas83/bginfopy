from os.path import expanduser
import subprocess
import configparser
import sys

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
    sys.exit("Error: '{0}': '{1}': '{2}'".format(error.returncode, error.output, error.message))
else:
    if VERBOSE: print("Directory {0} successfully created or already exist: {1}: {2}".format(USER_CONF_DIR, output, subprocess.STDOUT))

# Try to read user config
config = configparser.ConfigParser()

if VERBOSE: print("User config file: {0}".format(USER_CONF_DIR + "/" + USER_CONF_FILE))
config.read(USER_CONF_DIR + "/" + USER_CONF_FILE)
if VERBOSE: print("User config contains sections: {0}".format(config.sections()))
### SECTION MAIN ###
if 'MAIN' not in config: config.add_section('MAIN')
config_main = config["MAIN"]

if 'SUFFIX' in config_main: SUFFIX = config['MAIN']['SUFFIX']
else: config.set('MAIN','SUFFIX',SUFFIX)

if 'ORIGINAL_WALLPAPER' is config_main: ORIGINAL_WALLPAPER = config['MAIN']['ORIGINAL_WALLPAPER']
else: config.set('MAIN','ORIGINAL_WALLPAPER',ORIGINAL_WALLPAPER)

### SECTION TEXT ###
if 'TEXT' not in config.sections(): config.add_section('TEXT')
config_text = config["TEXT"]
if 'GRAVITY' in config_text: TEXT_GRAVITY = config['TEXT']['GRAVITY']
else: config.set('TEXT','GRAVITY', TEXT_GRAVITY)