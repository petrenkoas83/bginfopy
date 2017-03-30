import os
import wallpapers
import collectingdata
from preferences import *

# http://www.imagemagick.org/Usage/text/\
def put_text(in_img, out_img):
    verboseprint("Input image: '{0}'; Output image: '{1}'.".format(in_img, out_img))

    label = [config['TEXT']['title']]
    if str2bool(config['SHOW']['hostname']):
        label.append("Hostname:{0}".format(os.uname()[1]))
    if str2bool(config['SHOW']['interface_ip']):
        label.extend(collectingdata.get_ifipv4())
    label = "\n".join(label)

    # http://stackoverflow.com/questions/25079140/python-subprocess-popen-check-for-success-and-errors
    # https://docs.python.org/2/library/subprocess.html#subprocess.check_call
    try:
        if (out_img == '') or not str2bool(config['MAIN']['use_wallpaper_image']):
            verboseprint("(out_img == '') or not config['MAIN']['use_wallpaper_image']")
            output = subprocess.check_output(["convert",
                                              "-background", config['BACKGROUND']['color'],
                                              "-fill", "dodgerblue",
                                              # TODO: Try to get system default UI font and use it
                                              "-font", "Candice",
                                              "-strokewidth", "2",
                                              "-stroke", "blue",
                                              "-undercolor", "lightblue",
                                              "-size", wallpapers.determine_screen_resolution(),
                                              "-gravity", config['TEXT']['gravity'],
                                              label,
                                              out_img],
                                             stderr=subprocess.STDOUT)
        else:
            verboseprint("config['MAIN']['use_wallpaper_image']")
            # os.popen("convert {0} -gravity {2} -pointsize 30 -annotate +0+100 'TestText' {1}".format(in_img, out_img, config['TEXT']['gravity']))
            output = subprocess.check_output(["convert",
                                              in_img,
                                              "-gravity", config['TEXT']['gravity'],
                                              "-pointsize","30",
                                              "-annotate","+0+100",
                                              label,
                                              out_img],
                                             stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as error:
        # self.isCommandExecutionSuccessful = False
        print("Error: '{0}': '{1}': '{2}'".format(error.returncode, error.output, error.message))
        return error.returncode

    return 0

