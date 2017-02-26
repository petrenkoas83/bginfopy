import sys
import os
from preferences import *

def get_wallpaper():
    picture=''
    # http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    if VERBOSE: print('Platform: {0}'.format(sys.platform))
    if sys.platform in ["win32", "cygwin"]:
        sys.exit("Windows is not supporte")
    elif sys.platform == "darwin":
        sys.exit("MacOS in not supported")
    else:
        desktop_session = os.environ.get("DESKTOP_SESSION")
        if VERBOSE: print('Desktop session: {0}'.format(desktop_session))
        if desktop_session is not None:
            desktop_session = desktop_session.lower()
            if desktop_session == "mate":
                picture=get_wallpaper_mate()
            elif desktop_session == "lubuntu":
                picture = get_wallpaper_lxde()
            else:
                sys.exit("Unknown desktop session: '{0}'".format(desktop_session))
        else:
            #desktop_session = os.popen("ps ax | grep -ioP '/usr/bin/.+session' | grep -v grep").read()
            desktop_session = os.popen("ps -u $USER | grep -ioP '\S+session' | grep -v grep").read()
            desktop_session = desktop_session.rstrip('\n')
            if VERBOSE: print('Desktop session: {0}'.format(desktop_session))
            if desktop_session is not None:
                if desktop_session == 'lxsession':
                    picture = get_wallpaper_lxde()
                elif desktop_session == 'mate-session':
                    picture = get_wallpaper_mate()
                else:
                    sys.exit("Unknown desktop session: '{0}'".format(desktop_session))
            else:
                sys.exit("Desktop session is None")
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
