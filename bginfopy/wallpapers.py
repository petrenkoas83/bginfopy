import sys
import subprocess
import os
from preferences import *

def get_wallpaper():
    picture=''
    # http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    determine_platform()
    desktop_session = determine_desktop_session()
    if desktop_session in ["mate","mate-session"]:
        picture=get_wallpaper_mate()
    elif desktop_session in ["lubuntu","lxsession"]:
        picture = get_wallpaper_lxde()
    else:
        sys.exit("Unknown desktop session: '{0}'".format(desktop_session))
    picture = picture.rstrip('\n\r')
    picture = picture.strip("'")
    if VERBOSE: print("Wallpaper: '{0}'".format(picture))
    return(picture)

def get_wallpaper_mate():
    return os.popen("gsettings get org.mate.background picture-filename").read()

def get_wallpaper_lxde():
    profile_name=os.popen("grep -i \"^@pcmanfm\" /etc/xdg/lxsession/Lubuntu/autostart | grep -oP \"\\-\\-profile[\\s=].*[\\s\\n\\r]*\"").read()
    if VERBOSE: print("Profile name: '{0}'".format(profile_name))
    if (profile_name is not None) and (profile_name <> ''):
        #return os.popen("grep -i \"^wallpaper=\" $HOME/.config/pcmanfm/{0}/pcmanfm.conf | cut -d = -f2".format(profile_name)).read()
        cmd="grep -i \"^wallpaper=\" $HOME/.config/pcmanfm/{0}/desktop-items-0.conf | cut -d = -f2".format(profile_name)
    else:
        # return os.popen("grep -i \"^wallpaper=\" $HOME/.config/pcmanfm/LXDE/pcmanfm.conf | cut -d = -f2").read()
        cmd="grep -i \"^wallpaper=\" $HOME/.config/pcmanfm/lubuntu/desktop-items-0.conf | cut -d = -f2"
    if VERBOSE: print("Command to get wallpaper: '{0}'".format(cmd))
    picture = os.popen(cmd).read()
    return(picture)

def set_wallpaper(out_img):
    result = -1
    determine_platform()
    desktop_session = determine_desktop_session()
    if desktop_session in ["mate", "mate-session"]:
        result = set_wallpaper_mate()
    elif desktop_session in ["lubuntu", "lxsession"]:
        result = set_wallpaper_lxde()
    else:
        sys.exit("Unsupported desktop session: '{0}'".format(desktop_session))
    return result


def set_wallpaper_mate():
    print('set_wallpaper_mate')
    return 0


def set_wallpaper_lxde():
    print('set_wallpaper_lxde')
    return 0


def determine_platform():
    if VERBOSE: print('Platform: {0}'.format(sys.platform))
    # Since we're writing linux-only for now...
    if sys.platform.startswith('linux'):
        return sys.platform
    else:
        sys.exit("Unsupported platform: '{0}'".format(sys.platform))


def determine_desktop_session():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session is not None:
        desktop_session = desktop_session.lower()
    else:
        desktop_session = os.popen("ps -u $USER | grep -ioP '\S+session' | grep -v grep").read()
        desktop_session = desktop_session.rstrip('\n')
    if desktop_session is not None:
        if VERBOSE: print('Desktop session: {0}'.format(desktop_session))
        return desktop_session
    else:
        sys.exit("Desktop session is None")

def detemine_screen_resolution():
    output = ''
    screen_resolution = "640x480"
    try:
        # TODO: https://docs.python.org/2/library/subprocess.html#replacing-shell-pipeline

        #output=`dmesg | grep hda`
        #p1 = Popen(["dmesg"], stdout=PIPE)
        #p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
        #p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        #output = p2.communicate()[0]

        #p1 = subprocess.Popen(['/usr/bin/xrandr','--display',':0'], stdout=subprocess.PIPE)
        #p2 = subprocess.Popen(['/bin/grep','-oP','"current\s\d+\sx\s\d+"'], stdin=p1.stdout, stdout=subprocess.PIPE)
        #p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        #output = p2.communicate()[0]

        #screen_resolution = subprocess.check_output(['/usr/bin/xrandr','--display',':0',
        #                                             '|','/bin/grep','-oP','"current\s\d+\sx\s\d+"'],
        #                                            stderr=subprocess.STDOUT)

        output = os.popen('xrandr --display :0 | grep -oP "current\s\d+\sx\s\d+"').read()
        output = output.rstrip('\n')
    except subprocess.CalledProcessError as error:
        print("Error: '{0}': '{1}': '{2}'".format(error.returncode, error.output, error.message))
    else:
        if VERBOSE: print("xrandr output current: '{0}'".format(output))
        if output <> '':
            output = output.split()
            output.pop(0)
            output= "".join(output)
            screen_resolution = output
        if VERBOSE: print("Screen resolution: '{0}'".format(screen_resolution))
    return screen_resolution