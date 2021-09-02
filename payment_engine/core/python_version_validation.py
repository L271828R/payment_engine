import platform

def validate(needed_major, needed_minor, current=platform.python_version_tuple()):
    try:
        major, minor, micro = current
        assert(int(major) >= needed_major)
        assert(int(minor) >= needed_minor)
        return True
    except AssertionError:
        raise(AssertionError("Error: Python 3.4 or above is supported"))