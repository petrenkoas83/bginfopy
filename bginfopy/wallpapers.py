import sys
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
