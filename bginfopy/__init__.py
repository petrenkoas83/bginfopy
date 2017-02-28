#!/usr/bin/python
import wallpapers
import imagemagic
import os.path
from preferences import *

class image:
    def __init__(self, full_path):
        self.full_path = full_path
    def directory_path(self):
        return "/".join(self.full_path.split('/')[0:-1])
    def file_full_name(self):
        return self.full_path.split('/')[-1]
    def file_name(self):
        return "".join((self.file_full_name()).split('.')[0:-1])
    def file_ext(self):
        return (self.file_full_name()).split('.')[-1]
    def file_exist(self):
        return os.path.exists(self.full_path)


def main():
    global USE_WALLPAPER_IMAGE
    # Check current wallpaper
    in_img = image(wallpapers.get_wallpaper())
    if in_img.file_name().endswith(SUFFIX):
        if VERBOSE and (ORIGINAL_WALLPAPER_IMAGE == ''): print("Can not find original wallpaper: '{0}'".format(ORIGINAL_WALLPAPER_IMAGE))
        in_img = image(ORIGINAL_WALLPAPER_IMAGE)
    if in_img.file_exist():
        if VERBOSE: print('File {0} is exist!'.format(in_img.full_path))
        out_img = image((USER_CONF_DIR + "/" + in_img.file_name() + SUFFIX + "." + in_img.file_ext()))
    else:
        print('File {0} does not exist! I will use blank bagckround.'.format(in_img.full_path))
        USE_WALLPAPER_IMAGE = False
        in_img.full_path = ''

    # Process wallpaper image
    if VERBOSE: print("Try to process wallpaper image.")
    if imagemagic.put_text(in_img.full_path, out_img.full_path) == 0:
        # Set new wallpaper
        if wallpapers.set_wallpaper(out_img.full_path) == 0:
            # Renew path to original wallpaper image
            if VERBOSE: print("Previous value of [MAIN][ORIGINAL_WALLPAPER_IMAGE]: '{0}'".format(config['MAIN']['ORIGINAL_WALLPAPER_IMAGE']))
            config.set('MAIN', 'ORIGINAL_WALLPAPER_IMAGE', in_img.full_path)
            # Try to write user config
            if VERBOSE: print("Renew parametr in config [MAIN][ORIGINAL_WALLPAPER_IMAGE] = '{0}'".format(in_img.full_path))
            with open(USER_CONF_DIR + "/" + USER_CONF_FILE, 'w') as config_file:  # save
                config.write(config_file)
                config_file.close()
    else:
        print('Error occurred during put_text')
    return 0

main()
