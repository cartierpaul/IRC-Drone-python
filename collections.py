# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/collections
__all__ = ['deque',
 'defaultdict',
 'namedtuple',
 'OrderedDict']
from _abcoll import *
import _abcoll
__all__ += _abcoll.__all__
from _collections import deque, defaultdict
from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword
import sys as _sys
from itertools import imap as _imap
from operator import eq as _eq
try:
    from thread import get_ident as _get_ident
except ImportError:
    from dummy_thread import get_ident as _get_ident

class OrderedDict(dict):
    """Dictionary that remembers insertion order"""

    def __init__(self, *args, **kwds):
        """Initialize an ordered dictionary.  The signature is the same as
        regular dictionaries, but keyword arguments are not recommended because
        their insertion order is arbitrary.
        
        """
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = []
            root[:] = [root, root, None]
            self.__map = {}

        self.__update(*args, **kwds)
        return

    def __setitem__(self, key, value, dict_setitem = dict.__setitem__):
        """od.__setitem__(i, y) <==> od[i]=y"""
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        return dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem = dict.__delitem__):
        """od.__delitem__(y) <==> del od[y]"""
        dict_delitem(self, key)
        link_prev, link_next, _ = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        """od.__iter__() <==> iter(od)"""
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reversed__(self):
        """od.__reversed__() <==> reversed(od)"""
        root = self.__root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    def clear(self):
        """od.clear() -> None.  Remove all items from od."""
        root = self.__root
        root[:] = [root, root, None]
        self.__map.clear()
        dict.clear(self)
        return

    def keys(self):
        """od.keys() -> list of keys in od"""
        return list(self)

    def values(self):
        """od.values() -> list of values in od"""
        return [ self[key] for key in self ]

    def items(self):
        """od.items() -> list of (key, value) pairs in od"""
        return [ (key, self[key]) for key in self ]

    def iterkeys(self):
        """od.iterkeys() -> an iterator over the keys in od"""
        return iter(self)

    def itervalues(self):
        """od.itervalues -> an iterator over the values in od"""
        for k in self:
            yield self[k]

    def iteritems(self):
        """od.iteritems -> an iterator over the (key, value) pairs in od"""
        for k in self:
            yield (k, self[k])

    update = MutableMapping.update
    __update = update
    __marker = object()

    def pop(self, key, default = __marker):
        """od.pop(k[,d]) -> v, remove specified key and return the corresponding
        value.  If key is not found, d is returned if given, otherwise KeyError
        is raised.
        
        """
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default = None):
        """od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od"""
        if key in self:
            return self[key]
        self[key] = default
        return default

    def popitem(self, last = True):
        """od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.
        
        """
        if not self:
            raise KeyError('dictionary is empty')
        key = next(reversed(self) if last else iter(self))
        value = self.pop(key)
        return (key, value)

    def __repr__(self, _repr_running = {}):
        """od.__repr__() <==> repr(od)"""
        call_key = (id(self), _get_ident())
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())
        finally:
            del _repr_running[call_key]

    def __reduce__(self):
        """Return state information for pickling"""
        items = [ [k, self[k]] for k in self ]
        inst_dict = vars(self).copy()
        for k in vars(OrderedDict()):
            inst_dict.pop(k, None)

        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        else:
            return (self.__class__, (items,))

    def copy(self):
        """od.copy() -> a shallow copy of od"""
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value = None):
        """OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S.
        If not specified, the value defaults to None.
        
        """
        self = cls()
        for key in iterable:
            self[key] = value

        return self

    def __eq__(self, other):
        """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.
        
        """
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(_imap(_eq, self, other))
        return dict.__eq__(self, other)

    def __ne__(self, other):
        """od.__ne__(y) <==> od!=y"""
        return not self == other

    def viewkeys(self):
        """od.viewkeys() -> a set-like object providing a view on od's keys"""
        return KeysView(self)

    def viewvalues(self):
        """od.viewvalues() -> an object providing a view on od's values"""
        return ValuesView(self)

    def viewitems(self):
        """od.viewitems() -> a set-like object providing a view on od's items"""
        return ItemsView(self)


def namedtuple(typename, field_names, verbose = False):
    """Returns a new subclass of tuple with named fields.
    
    >>> Point = namedtuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)
    
    """
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split()
    field_names = tuple(map(str, field_names))
    for name in (typename,) + field_names:
        if not all((c == '_' for c in name if not c.isalnum())):
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)

    seen_names = set()
    for name in field_names:
        if name.startswith('_'):
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    numfields = len(field_names)
    argtxt = repr(field_names).replace("'", '')[1:-1]
    reprtxt = ', '.join(('%s=%%r' % name for name in field_names))
    dicttxt = ', '.join(('%r: t[%d]' % (name, pos) for pos, name in enumerate(field_names)))
    template = "class %(typename)s(tuple):\n        '%(typename)s(%(argtxt)s)' \n\n        __slots__ = () \n\n        _fields = %(field_names)r \n\n        def __new__(_cls, %(argtxt)s):\n            return _tuple.__new__(_cls, (%(argtxt)s)) \n\n        @classmethod\n        def _make(cls, iterable, new=tuple.__new__, len=len):\n            'Make a new %(typename)s object from a sequence or iterable'\n            result = new(cls, iterable)\n            if len(result) != %(numfields)d:\n                raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))\n            return result \n\n        def __repr__(self):\n            return '%(typename)s(%(reprtxt)s)' %% self \n\n        def _asdict(t):\n            'Return a new dict which maps field names to their values'\n            return {%(dicttxt)s} \n\n        def _replace(_self, **kwds):\n            'Return a new %(typename)s object replacing specified fields with new values'\n            result = _self._make(map(kwds.pop, %(field_names)r, _self))\n            if kwds:\n                raise ValueError('Got unexpected field names: %%r' %% kwds.keys())\n            return result \n\n        def __getnewargs__(self):\n            return tuple(self) \n\n" % locals()
    for i, name in enumerate(field_names):
        template += '        %s = _property(_itemgetter(%d))\n' % (name, i)

    if verbose:
        print template
    namespace = dict(_itemgetter=_itemgetter, __name__='namedtuple_%s' % typename, _property=property, _tuple=tuple)
    try:
        exec template in namespace
    except SyntaxError as e:
        raise SyntaxError(e.message + ':\n' + template)

    result = namespace[typename]
    if hasattr(_sys, '_getframe'):
        result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    return result


if __name__ == '__main__':
    from cPickle import loads, dumps
    Point = namedtuple('Point', 'x, y', True)
    p = Point(x=10, y=20)
    raise p == loads(dumps(p)) or AssertionError

    class Point(namedtuple('Point', 'x y')):
        __slots__ = ()

        @property
        def hypot(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5

        def __str__(self):
            return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)


    for p in (Point(3, 4), Point(14, 5 / 7.0)):
        print p

    class Point(namedtuple('Point', 'x y')):
        """Point class with optimized _make() and _replace() without error-checking"""
        __slots__ = ()
        _make = classmethod(tuple.__new__)

        def _replace(self, _map = map, **kwds):
            return self._make(_map(kwds.get, ('x', 'y'), self))


    print Point(11, 22)._replace(x=100)
    Point3D = namedtuple('Point3D', Point._fields + ('z',))
    print Point3D.__doc__
    import doctest
    TestResults = namedtuple('TestResults', 'failed attempted')
    print TestResults(*doctest.testmod())