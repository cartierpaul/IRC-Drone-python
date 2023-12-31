# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/email.iterators
"""Various types of useful iterators and generators."""
__all__ = ['body_line_iterator', 'typed_subpart_iterator', 'walk']
import sys
from cStringIO import StringIO

def walk(self):
    """Walk over the message tree, yielding each subpart.
    
    The walk is performed in depth-first order.  This method is a
    generator.
    """
    yield self
    if self.is_multipart():
        for subpart in self.get_payload():
            for subsubpart in subpart.walk():
                yield subsubpart


def body_line_iterator(msg, decode = False):
    """Iterate over the parts, returning string payloads line-by-line.
    
    Optional decode (default False) is passed through to .get_payload().
    """
    for subpart in msg.walk():
        payload = subpart.get_payload(decode=decode)
        if isinstance(payload, basestring):
            for line in StringIO(payload):
                yield line


def typed_subpart_iterator(msg, maintype = 'text', subtype = None):
    """Iterate over the subparts with a given MIME type.
    
    Use `maintype' as the main MIME type to match against; this defaults to
    "text".  Optional `subtype' is the MIME subtype to match against; if
    omitted, only the main type is matched.
    """
    for subpart in msg.walk():
        if subpart.get_content_maintype() == maintype:
            if subtype is None or subpart.get_content_subtype() == subtype:
                yield subpart

    return


def _structure(msg, fp = None, level = 0, include_default = False):
    """A handy debugging aid"""
    if fp is None:
        fp = sys.stdout
    tab = ' ' * (level * 4)
    print >> fp, tab + msg.get_content_type(),
    if include_default:
        print >> fp, '[%s]' % msg.get_default_type()
    else:
        print >> fp
    if msg.is_multipart():
        for subpart in msg.get_payload():
            _structure(subpart, fp, level + 1, include_default)

    return