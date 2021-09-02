import platform

def validate(needed_major, needed_minor):
    try:
        major, minor, micro = platform.python_version_tuple()
        assert(int(major) <= needed_major)
        assert(int(minor) <= needed_minor)
        return True
    except AssertionError:
        raise(AssertionError("Error: Python 3.4 or above is supported"))