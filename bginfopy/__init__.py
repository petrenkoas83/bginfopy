#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import imagemagic
import wallpapers
from preferences import *


class Image:
    def __init__(self, full_path):
        self.full_path = full_path

    @property
    def directory_path(self):
        # type: () -> str
        return os.path.split(self.full_path)[0]

    @property
    def file_full_name(self):
        # type: () -> str
        # File name with extension
        return os.path.split(self.full_path)[-1]

    @property
    def file_name(self):
        # type: () -> str
        return "".join(self.file_full_name.split('.')[0:-1])

    @property
    def file_ext(self):
        # type: () -> str
        # http://stackoverflow.com/a/37273834/3711461
        # Returns empty string for names like "/something/.DS_Store" but we don't care
        return os.path.splitext(self.full_path)[-1]

    @property
    def file_exist(self):
        # type: () -> bool
        return os.path.exists(self.full_path)


def main():
    global config

    # Create Image objects
    in_img = Image(wallpapers.get_wallpaper())
    # Let's do it the right (and cross-platform) way: joining path instead of concatenation of strings
    out_img = Image(os.path.join(USER_CONF_DIR, in_img.file_name + config['MAIN']['suffix'] + in_img.file_ext))
    verboseprint("in_img.file_name: '{0}'".format(in_img.file_name))
    verboseprint("in_img.file_ext: '{0}'".format(in_img.file_ext))

    # Check current wallpaper
    if in_img.file_name.endswith(config['MAIN']['suffix']):
        # If current wallpaper created with bginfo, then try to get original wallpaper
        if config['MAIN']['original_wallpaper_image'] == '':
            # If original wallpaper is not set in config, then use blank background
            verboseprint("Can not find original wallpaper: '{0}'".format(config['MAIN']['original_wallpaper_image']))
            in_img.full_path = ''
        else:
            # If original wallpaper is set in config, then use original wallpaper
            in_img.full_path = config['MAIN']['original_wallpaper_image']

    # Check file of original wallpaper
    if in_img.file_exist:
        verboseprint('File {0} is exist!'.format(in_img.full_path))
    else:
        # If file of original wallpaper does not exist, then use blank background
        verboseprint('File {0} does not exist! I will use blank background.'.format(in_img.full_path))
        config['MAIN']['use_wallpaper_image'] = 'False'
        in_img.full_path = ''

    # Process wallpaper image
    verboseprint("Try to process wallpaper image.")
    if imagemagic.put_text(in_img.full_path, out_img.full_path) == 0:
        # If convert successful, then set new wallpaper
        if wallpapers.set_wallpaper(out_img.full_path) == 0:
            # If set new wallpaper is successful, then renew path to original wallpaper image
            config.set('MAIN', 'original_wallpaper_image', in_img.full_path)
            # Try to write user config
            verboseprint("Renew parameter in config for [MAIN][original_wallpaper_image] = '{0}'".format(in_img.full_path))
            with open(USER_CONF_DIR + "/" + USER_CONF_FILE, 'w') as config_file:  # save
                config.write(config_file)
                config_file.close()
    else:
        print('Error occurred during put_text')
    return 0

main()
