#!/usr/bin/python
# -*- coding: utf-8 -*-
import wallpapers
import imagemagic
import os.path
import re
from preferences import *


class Image:
    def __init__(self, full_path):
        self.full_path = full_path

    @property
    def directory_path(self):
        # type: () -> str
        return "/".join(self.full_path.split('/')[0:-1])

    @property
    def file_full_name(self):
        # type: () -> str
        return self.full_path.split('/')[-1]

    @property
    def file_name(self):
        # type: () -> str
        return "".join(self.file_full_name.split('.')[0:-1])

    @property
    def file_ext(self):
        # type: () -> str
        rPattern = '^.*/.*\.([^/\s]+)$'
        if re.search(rPattern, self.file_full_name) is not None:
            return re.sub(rPattern, r'\1', self.file_full_name)
        else:
            return ''  # Empty string = no extension


    @property
    def file_exist(self):
        # type: () -> bool
        return os.path.exists(self.full_path)


def main():
    global USE_WALLPAPER_IMAGE

    # Create Image objects
    in_img = Image(wallpapers.get_wallpaper())
    out_img = Image(USER_CONF_DIR + "/" + in_img.file_name + SUFFIX + "." + in_img.file_ext)

    # Check current wallpaper
    if in_img.file_name.endswith(SUFFIX):
        # If current wallpaper created with bginfo, then try to get original wallpaper
        if ORIGINAL_WALLPAPER_IMAGE == '':
            # If original wallpaper is not set in config, then use blank background
            if VERBOSE: print("Can not find original wallpaper: '{0}'".format(ORIGINAL_WALLPAPER_IMAGE))
            in_img.full_path = ''
        else:
            # If original wallpaper is set in config, then use original wallpaper
            in_img.full_path = ORIGINAL_WALLPAPER_IMAGE

    # Check file of original wallpaper
    if in_img.file_exist:
        if VERBOSE: print('File {0} is exist!'.format(in_img.full_path))
    else:
        # If file of original wallpaper does not exist, then use blank background
        if VERBOSE: print('File {0} does not exist! I will use blank background.'.format(in_img.full_path))
        USE_WALLPAPER_IMAGE = False
        in_img.full_path = ''

    # Process wallpaper image
    if VERBOSE: print("Try to process wallpaper image.")
    if imagemagic.put_text(in_img.full_path, out_img.full_path) == 0:
        # In convert successful, then set new wallpaper
        if wallpapers.set_wallpaper(out_img.full_path) == 0:
            # If set new wallpaper is successful, then renew path to original wallpaper image
            if VERBOSE: print("Previous value of [MAIN][ORIGINAL_WALLPAPER_IMAGE]: '{0}'".format(
                config['MAIN']['ORIGINAL_WALLPAPER_IMAGE']))
            config.set('MAIN', 'ORIGINAL_WALLPAPER_IMAGE', in_img.full_path)
            # Try to write user config
            if VERBOSE: print(
                "Renew parameter in config [MAIN][ORIGINAL_WALLPAPER_IMAGE] = '{0}'".format(in_img.full_path))
            with open(USER_CONF_DIR + "/" + USER_CONF_FILE, 'w') as config_file:  # save
                config.write(config_file)
                config_file.close()
    else:
        print('Error occurred during put_text')
    return 0


main()
