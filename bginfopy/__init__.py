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
    if ORIGINAL_WALLPAPER <> '':
        in_img = image(ORIGINAL_WALLPAPER)
    else:
        in_img = image(wallpapers.get_wallpaper())
    if in_img.file_exist():
        if VERBOSE: print('File {0} is exist!'.format(in_img.full_path))
        out_img = image((USER_CONF_DIR + "/" + in_img.file_name() + SUFFIX + "." + in_img.file_ext()))
    else:
        print('File {0} does not exist!'.format(in_img.full_path))
        return 1
    imagemagic.put_text(in_img.full_path, out_img.full_path)

    return 0

main()
