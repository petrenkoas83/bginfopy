import os
import wallpapers
import collectingdata
from preferences import *

# http://www.imagemagick.org/Usage/text/\
def put_text(in_img, out_img):
    verboseprint("Input image: '{0}'; Output image: '{1}'.".format(in_img, out_img))

    label = [config['TEXT']['title']]
    if str2bool(config['SHOW']['hostname']):
        label.append("Hostname: {0}".format(os.uname()[1]))
    if str2bool(config['SHOW']['interface_ip']):
        label.extend(collectingdata.get_ifipv4())
    label = "\n".join(label)

    # http://stackoverflow.com/questions/25079140/python-subprocess-popen-check-for-success-and-errors
    # https://docs.python.org/2/library/subprocess.html#subprocess.check_call
    try:
        if (out_img == '') or not str2bool(config['MAIN']['use_wallpaper_image']):
            verboseprint("Use blank background, because (out_img == '') or not config['MAIN']['use_wallpaper_image']")
            output = subprocess.check_output(["convert",
                                              "-size", wallpapers.determine_screen_resolution(),
                                              "-background", config['BACKGROUND']['color'],
                                              "-pointsize", "24",
                                              "-splice", "24x24",
                                              # TODO: Try to get system default UI font and use it
                                              "-font", "Liberation-Sans-Bold", # convert -list font
                                              "-strokewidth", "1",
                                              "-stroke", "black",
                                              "-fill", "yellow",
                                              #"-undercolor", "white",
                                              "-gravity", config['TEXT']['gravity'],
                                              "label:{0}".format(label),
                                              out_img],
                                             stderr=subprocess.STDOUT)
        else:
            verboseprint("config['MAIN']['use_wallpaper_image']")
            # os.popen("convert {0} -gravity {2} -pointsize 30 -annotate +0+100 'TestText' {1}".format(in_img, out_img, config['TEXT']['gravity']))
            output = subprocess.check_output(["convert",
                                              in_img,
                                              "-gravity", config['TEXT']['gravity'],
                                              "-pointsize", "24",
                                              "-font", "Liberation-Sans-Bold",
                                              "-strokewidth", "1",
                                              "-stroke", "black",
                                              "-fill", "yellow",
                                              #"-undercolor", "yellow",
                                              "-annotate","+0+100",
                                              "{0}".format(label),
                                              out_img],
                                             stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as error:
        # self.isCommandExecutionSuccessful = False
        print("Converting error:\n Code: '{0}'\n Output: '{1}'\n Message: '{2}'\n Command: '{3}'".format(error.returncode, error.output, error.message, error.cmd))
        return error.returncode

    return 0

