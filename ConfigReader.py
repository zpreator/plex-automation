from configparser import ConfigParser

def GetPaths():
    config = ConfigParser()
    config.read('config.ini')
    dictionary = {}
    dictionary['ffmpeg'  ] = config.get('paths', 'ffmpeg') # -> "value1"
    dictionary['youtube' ] = config.get('paths', 'youtube') # -> "value2"
    dictionary['podcasts'] = config.get('paths', 'podcasts') # -> "value3"
    dictionary['music'   ] = config.get('paths', 'music') # -> "value3"
    return dictionary

def GetUsernamePassword():
    config = ConfigParser()
    config.read('config.ini')
    dictionary = {}
    dictionary['username'] = config.get('email', 'username') # -> "value1"
    dictionary['password'] = config.get('email', 'password') # -> "value2"
    return dictionary