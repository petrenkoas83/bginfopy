import subprocess
from preferences import *

#http://www.imagemagick.org/Usage/text/
def put_text(in_img, out_img):
    if VERBOSE: print("Input image: '{0}'; Output image: '{1}'.".format(in_img, out_img))
    #http://stackoverflow.com/questions/25079140/python-subprocess-popen-check-for-success-and-errors
    #https://docs.python.org/2/library/subprocess.html#subprocess.check_call
    try:
        # convert temp.jpg -gravity North -pointsize 30 -annotate +0+100 'Love you mom' temp1.jpg
        # convert -background white -fill dodgerblue  -font Candice \
        #       -strokewidth 2  -stroke blue   -undercolor lightblue \
        #       -size 165x70 -gravity center label:Anthony     label_color.gif
        #os.popen("convert {0} -gravity {2} -pointsize 30 -annotate +0+100 'TestText' {1}".format(in_img, out_img, TEXT_GRAVITY))
        output = subprocess.check_output(["convert",
                                          in_img,
                                          "-gravity",TEXT_GRAVITY,
                                          "-pointsize","30",
                                          "-annotate","+0+100",
                                          'TestText',
                                          out_img],
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        #self.isCommandExecutionSuccessful = False
        print("Error: '{0}': '{1}': '{2}'".format(error.returncode, error.output, error.message))
        return error.returncode
    else:
        if VERBOSE: print('Text put successfully. Here will be called set_wallpaper.')
        #self.isCommandExecutionSuccessful = True
    finally:
        if VERBOSE: print('Fin convert.')
    return 0

