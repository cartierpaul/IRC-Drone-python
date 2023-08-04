# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/encodings.cp864
""" Python Character Mapping Codec generated from 'VENDORS/MICSFT/PC/CP864.TXT' with gencodec.py.

"""
import codecs

class Codec(codecs.Codec):

    def encode(self, input, errors = 'strict'):
        return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors = 'strict'):
        return codecs.charmap_decode(input, errors, decoding_table)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final = False):
        return codecs.charmap_encode(input, self.errors, encoding_map)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final = False):
        return codecs.charmap_decode(input, self.errors, decoding_table)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='cp864', encode=Codec().encode, decode=Codec().decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamreader=StreamReader, streamwriter=StreamWriter)


decoding_map = codecs.make_identity_dict(range(256))
decoding_map.update({37: 1642,
 128: 176,
 129: 183,
 130: 8729,
 131: 8730,
 132: 9618,
 133: 9472,
 134: 9474,
 135: 9532,
 136: 9508,
 137: 9516,
 138: 9500,
 139: 9524,
 140: 9488,
 141: 9484,
 142: 9492,
 143: 9496,
 144: 946,
 145: 8734,
 146: 966,
 147: 177,
 148: 189,
 149: 188,
 150: 8776,
 151: 171,
 152: 187,
 153: 65271,
 154: 65272,
 155: None,
 156: None,
 157: 65275,
 158: 65276,
 159: None,
 161: 173,
 162: 65154,
 165: 65156,
 166: None,
 167: None,
 168: 65166,
 169: 65167,
 170: 65173,
 171: 65177,
 172: 1548,
 173: 65181,
 174: 65185,
 175: 65189,
 176: 1632,
 177: 1633,
 178: 1634,
 179: 1635,
 180: 1636,
 181: 1637,
 182: 1638,
 183: 1639,
 184: 1640,
 185: 1641,
 186: 65233,
 187: 1563,
 188: 65201,
 189: 65205,
 190: 65209,
 191: 1567,
 192: 162,
 193: 65152,
 194: 65153,
 195: 65155,
 196: 65157,
 197: 65226,
 198: 65163,
 199: 65165,
 200: 65169,
 201: 65171,
 202: 65175,
 203: 65179,
 204: 65183,
 205: 65187,
 206: 65191,
 207: 65193,
 208: 65195,
 209: 65197,
 210: 65199,
 211: 65203,
 212: 65207,
 213: 65211,
 214: 65215,
 215: 65217,
 216: 65221,
 217: 65227,
 218: 65231,
 219: 166,
 220: 172,
 221: 247,
 222: 215,
 223: 65225,
 224: 1600,
 225: 65235,
 226: 65239,
 227: 65243,
 228: 65247,
 229: 65251,
 230: 65255,
 231: 65259,
 232: 65261,
 233: 65263,
 234: 65267,
 235: 65213,
 236: 65228,
 237: 65230,
 238: 65229,
 239: 65249,
 240: 65149,
 241: 1617,
 242: 65253,
 243: 65257,
 244: 65260,
 245: 65264,
 246: 65266,
 247: 65232,
 248: 65237,
 249: 65269,
 250: 65270,
 251: 65245,
 252: 65241,
 253: 65265,
 254: 9632,
 255: None})
decoding_table = u'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$\u066a&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\xb0\xb7\u2219\u221a\u2592\u2500\u2502\u253c\u2524\u252c\u251c\u2534\u2510\u250c\u2514\u2518\u03b2\u221e\u03c6\xb1\xbd\xbc\u2248\xab\xbb\ufef7\ufef8\ufffe\ufffe\ufefb\ufefc\ufffe\xa0\xad\ufe82\xa3\xa4\ufe84\ufffe\ufffe\ufe8e\ufe8f\ufe95\ufe99\u060c\ufe9d\ufea1\ufea5\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669\ufed1\u061b\ufeb1\ufeb5\ufeb9\u061f\xa2\ufe80\ufe81\ufe83\ufe85\ufeca\ufe8b\ufe8d\ufe91\ufe93\ufe97\ufe9b\ufe9f\ufea3\ufea7\ufea9\ufeab\ufead\ufeaf\ufeb3\ufeb7\ufebb\ufebf\ufec1\ufec5\ufecb\ufecf\xa6\xac\xf7\xd7\ufec9\u0640\ufed3\ufed7\ufedb\ufedf\ufee3\ufee7\ufeeb\ufeed\ufeef\ufef3\ufebd\ufecc\ufece\ufecd\ufee1\ufe7d\u0651\ufee5\ufee9\ufeec\ufef0\ufef2\ufed0\ufed5\ufef5\ufef6\ufedd\ufed9\ufef1\u25a0\ufffe'
encoding_map = {0: 0,
 1: 1,
 2: 2,
 3: 3,
 4: 4,
 5: 5,
 6: 6,
 7: 7,
 8: 8,
 9: 9,
 10: 10,
 11: 11,
 12: 12,
 13: 13,
 14: 14,
 15: 15,
 16: 16,
 17: 17,
 18: 18,
 19: 19,
 20: 20,
 21: 21,
 22: 22,
 23: 23,
 24: 24,
 25: 25,
 26: 26,
 27: 27,
 28: 28,
 29: 29,
 30: 30,
 31: 31,
 32: 32,
 33: 33,
 34: 34,
 35: 35,
 36: 36,
 38: 38,
 39: 39,
 40: 40,
 41: 41,
 42: 42,
 43: 43,
 44: 44,
 45: 45,
 46: 46,
 47: 47,
 48: 48,
 49: 49,
 50: 50,
 51: 51,
 52: 52,
 53: 53,
 54: 54,
 55: 55,
 56: 56,
 57: 57,
 58: 58,
 59: 59,
 60: 60,
 61: 61,
 62: 62,
 63: 63,
 64: 64,
 65: 65,
 66: 66,
 67: 67,
 68: 68,
 69: 69,
 70: 70,
 71: 71,
 72: 72,
 73: 73,
 74: 74,
 75: 75,
 76: 76,
 77: 77,
 78: 78,
 79: 79,
 80: 80,
 81: 81,
 82: 82,
 83: 83,
 84: 84,
 85: 85,
 86: 86,
 87: 87,
 88: 88,
 89: 89,
 90: 90,
 91: 91,
 92: 92,
 93: 93,
 94: 94,
 95: 95,
 96: 96,
 97: 97,
 98: 98,
 99: 99,
 100: 100,
 101: 101,
 102: 102,
 103: 103,
 104: 104,
 105: 105,
 106: 106,
 107: 107,
 108: 108,
 109: 109,
 110: 110,
 111: 111,
 112: 112,
 113: 113,
 114: 114,
 115: 115,
 116: 116,
 117: 117,
 118: 118,
 119: 119,
 120: 120,
 121: 121,
 122: 122,
 123: 123,
 124: 124,
 125: 125,
 126: 126,
 127: 127,
 160: 160,
 162: 192,
 163: 163,
 164: 164,
 166: 219,
 171: 151,
 172: 220,
 173: 161,
 176: 128,
 177: 147,
 183: 129,
 187: 152,
 188: 149,
 189: 148,
 215: 222,
 247: 221,
 946: 144,
 966: 146,
 1548: 172,
 1563: 187,
 1567: 191,
 1600: 224,
 1617: 241,
 1632: 176,
 1633: 177,
 1634: 178,
 1635: 179,
 1636: 180,
 1637: 181,
 1638: 182,
 1639: 183,
 1640: 184,
 1641: 185,
 1642: 37,
 8729: 130,
 8730: 131,
 8734: 145,
 8776: 150,
 9472: 133,
 9474: 134,
 9484: 141,
 9488: 140,
 9492: 142,
 9496: 143,
 9500: 138,
 9508: 136,
 9516: 137,
 9524: 139,
 9532: 135,
 9618: 132,
 9632: 254,
 65149: 240,
 65152: 193,
 65153: 194,
 65154: 162,
 65155: 195,
 65156: 165,
 65157: 196,
 65163: 198,
 65165: 199,
 65166: 168,
 65167: 169,
 65169: 200,
 65171: 201,
 65173: 170,
 65175: 202,
 65177: 171,
 65179: 203,
 65181: 173,
 65183: 204,
 65185: 174,
 65187: 205,
 65189: 175,
 65191: 206,
 65193: 207,
 65195: 208,
 65197: 209,
 65199: 210,
 65201: 188,
 65203: 211,
 65205: 189,
 65207: 212,
 65209: 190,
 65211: 213,
 65213: 235,
 65215: 214,
 65217: 215,
 65221: 216,
 65225: 223,
 65226: 197,
 65227: 217,
 65228: 236,
 65229: 238,
 65230: 237,
 65231: 218,
 65232: 247,
 65233: 186,
 65235: 225,
 65237: 248,
 65239: 226,
 65241: 252,
 65243: 227,
 65245: 251,
 65247: 228,
 65249: 239,
 65251: 229,
 65253: 242,
 65255: 230,
 65257: 243,
 65259: 231,
 65260: 244,
 65261: 232,
 65263: 233,
 65264: 245,
 65265: 253,
 65266: 246,
 65267: 234,
 65269: 249,
 65270: 250,
 65271: 153,
 65272: 154,
 65275: 157,
 65276: 158}