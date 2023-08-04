# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/site
"""
This is a fake 'site' module available in default Python Library.

The real 'site' does some magic to find paths to other possible
Python modules. We do not want this behaviour for frozen applications.

Fake 'site' makes PyInstaller to work with distutils and to work inside
virtualenv environment.
"""
PREFIXES = []
ENABLE_USER_SITE = False
USER_SITE = None
USER_BASE = None

class _Helper(object):
    """
    Define the builtin 'help'.
    This is a wrapper around pydoc.help (with a twist).
    """

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__(self, *args, **kwds):
        import pydoc
        return pydoc.help(*args, **kwds)