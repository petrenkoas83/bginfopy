#!/usr/bin/python
# -*- coding: utf-8 -*-
import wallpapers
import imagemagic
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


def main():
    in_img = image(wallpapers.get_wallpaper())
    out_img = image((in_img.directory_path() + "/" + in_img.file_name() + SUFFIX + "." + in_img.file_ext()))
    print(in_img.full_path, out_img.full_path)
    #imagemagic.put_text(in_img,out_img)

main()
