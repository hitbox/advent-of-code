import os

__all__ = ['thisdir', 'input_path', 'safeint']

def thisdir():
    return os.path.dirname(os.path.abspath(__file__))

def input_path(filepath, part):
    """
    :param filepath: __file__ from the script
    :param part: the part number
    """

    root, ext = os.path.splitext(filepath)
    input_name = root + '.input' + ('2' if part == 2 else '')
    input_path = os.path.join(thisdir(), 'inputs', input_name)
    return input_path

def safeint(thing):
    try:
        return int(thing)
    except ValueError:
        return thing
