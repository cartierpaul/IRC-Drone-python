# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/urllib
"""Open an arbitrary URL.

See the following document for more info on URLs:
"Names and Addresses, URIs, URLs, URNs, URCs", at
http://www.w3.org/pub/WWW/Addressing/Overview.html

See also the HTTP spec (from which the error codes are derived):
"HTTP - Hypertext Transfer Protocol", at
http://www.w3.org/pub/WWW/Protocols/

Related standards and specs:
- RFC1808: the "relative URL" spec. (authoritative status)
- RFC1738 - the "URL standard". (authoritative status)
- RFC1630 - the "URI spec". (informational status)

The object returned by URLopener().open(file) will differ per
protocol.  All you know is that is has methods read(), readline(),
readlines(), fileno(), close() and info().  The read*(), fileno()
and close() methods work like those of open files.
The info() method returns a mimetools.Message object which can be
used to query various info about the object, if available.
(mimetools.Message objects are queried with the getheader() method.)
"""