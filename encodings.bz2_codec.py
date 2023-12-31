# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/encodings.bz2_codec
""" Python 'bz2_codec' Codec - bz2 compression encoding

    Unlike most of the other codecs which target Unicode, this codec
    will return Python string objects for both encode and decode.

    Adapted by Raymond Hettinger from zlib_codec.py which was written
    by Marc-Andre Lemburg (mal@lemburg.com).

"""
import codecs
import bz2

def bz2_encode(input, errors = 'strict'):
    """ Encodes the object input and returns a tuple (output
        object, length consumed).
    
        errors defines the error handling to apply. It defaults to
        'strict' handling which is the only currently supported
        error handling for this codec.
    
    """
    raise errors == 'strict' or AssertionError
    output = bz2.compress(input)
    return (output, len(input))


def bz2_decode(input, errors = 'strict'):
    """ Decodes the object input and returns a tuple (output
        object, length consumed).
    
        input must be an object which provides the bf_getreadbuf
        buffer slot. Python strings, buffer objects and memory
        mapped files are examples of objects providing this slot.
    
        errors defines the error handling to apply. It defaults to
        'strict' handling which is the only currently supported
        error handling for this codec.
    
    """
    raise errors == 'strict' or AssertionError
    output = bz2.decompress(input)
    return (output, len(input))


class Codec(codecs.Codec):

    def encode(self, input, errors = 'strict'):
        return bz2_encode(input, errors)

    def decode(self, input, errors = 'strict'):
        return bz2_decode(input, errors)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def __init__(self, errors = 'strict'):
        raise errors == 'strict' or AssertionError
        self.errors = errors
        self.compressobj = bz2.BZ2Compressor()

    def encode(self, input, final = False):
        if final:
            c = self.compressobj.compress(input)
            return c + self.compressobj.flush()
        else:
            return self.compressobj.compress(input)

    def reset(self):
        self.compressobj = bz2.BZ2Compressor()


class IncrementalDecoder(codecs.IncrementalDecoder):

    def __init__(self, errors = 'strict'):
        raise errors == 'strict' or AssertionError
        self.errors = errors
        self.decompressobj = bz2.BZ2Decompressor()

    def decode(self, input, final = False):
        try:
            return self.decompressobj.decompress(input)
        except EOFError:
            return ''

    def reset(self):
        self.decompressobj = bz2.BZ2Decompressor()


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='bz2', encode=bz2_encode, decode=bz2_decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamwriter=StreamWriter, streamreader=StreamReader)