import os

from preferences import *


def get_wallpaper():
    picture = ''
    # http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    determine_platform()
    desktop_session = determine_desktop_session()

    if desktop_session in ["mate", "mate-session"]:
        picture = get_wallpaper_mate()
    elif desktop_session in ["lubuntu", "lxsession"]:
        picture = get_wallpaper_lxde()
    else:
        sys.exit("Unknown desktop session: '{0}'".format(desktop_session))

    picture = picture.rstrip('\n\r')
    picture = picture.strip("'")

    verboseprint("Wallpaper: '{0}'".format(picture))
    return picture


def get_wallpaper_mate():
    return os.popen("gsettings get org.mate.background picture-filename").read()


def get_lxde_profile_name():
    return os.popen(
        "grep -i \"^@pcmanfm\" /etc/xdg/lxsession/Lubuntu/autostart | grep -oP \"\\-\\-profile[\\s=].*[\\s\\n\\r]*\""
    ).read()


def get_wallpaper_lxde():
    profile_name = get_lxde_profile_name()
    parser = configparser.ConfigParser()

    verboseprint("Profile name: '{0}'".format(profile_name))

    if (profile_name is not None) and (profile_name <> ''):
        config_path = os.path.join(os.path.expandvars('$HOME'), '.config/pcmanfm', profile_name, 'desktop-items-0.conf')
    else:
        config_path = os.path.join(os.path.expandvars('$HOME'), '.config/pcmanfm/lubuntu/desktop-items-0.conf')

    parser.read(config_path)
    return parser['*']['wallpaper']


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
    verboseprint('Platform: {0}'.format(sys.platform))
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
        verboseprint('Desktop session: {0}'.format(desktop_session))
        return desktop_session
    else:
        sys.exit("Desktop session is None")


def determine_screen_resolution():
    screen_resolution = "640x480"
    output = os.popen('xrandr --display :0 | grep -oP "current\s\d+\sx\s\d+"').read()
    output = output.rstrip('\n')
    verboseprint("xrandr output current: '{0}'".format(output))
    if output <> '':
        output = output.split()
        output.pop(0)
        output = "".join(output)
        screen_resolution = output
    verboseprint("Screen resolution: '{0}'".format(screen_resolution))
    return screen_resolution


def wallpaper_is_set():
    # type: () -> bool
    desktop_session = determine_desktop_session()

    if desktop_session in ["mate", "mate-session"]:
        if os.popen("gsettings get org.mate.background picture-filename").read() <> '':
            return True
        else:
            return False

    elif desktop_session in ["lubuntu", "lxsession"]:
        profile_name = get_lxde_profile_name()

        if (profile_name is not None) and (profile_name <> ''):
            config_path = os.path.expandvars('$HOME') + '/.config/pcmanfm/{0}/desktop-items-0.conf'.format(profile_name)
        else:
            config_path = os.path.expandvars('$HOME') + '/.config/pcmanfm/lubuntu/desktop-items-0.conf'
        # endif

        # Parse config for:
        # [*]
        # wallpaper_mode = color
        # if 'color' => False | smth else => True
        parser = configparser.ConfigParser()
        parser.read(config_path)

        if parser['*']['wallpaper_mode'] <> 'color':
            return True
        else:
            return False

    else:
        sys.exit("Unknown desktop session: '{0}'".format(desktop_session))
