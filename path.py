import os.path
import __main__

input_directory = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "input")
animated_directory = input_directory


def get_animated_directory():
    global animated_directory
    return animated_directory

def get_animated_filepath(name):
    return os.path.join(get_animated_directory(), name)

def exists_animated_filepath(name):
    return os.path.exists(get_animated_directory(), name)
