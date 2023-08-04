# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/email.mime.nonmultipart
"""Base class for MIME type messages that are not multipart."""
__all__ = ['MIMENonMultipart']
from email import errors
from email.mime.base import MIMEBase

class MIMENonMultipart(MIMEBase):
    """Base class for MIME multipart/* type messages."""
    __pychecker__ = 'unusednames=payload'

    def attach(self, payload):
        raise errors.MultipartConversionError('Cannot attach additional subparts to non-multipart/*')

    del __pychecker__