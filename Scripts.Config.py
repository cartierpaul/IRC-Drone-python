# Embedded file name: /home/boris/undernetbot/build/run/out00-PYZ.pyz/Scripts.Config
from Vars import MAXSERVERS, MAXADMINS, DEFCMDCHAR, PID_FILE, DEBUG
from Functions import decode, encode
from random import randrange
import time, Bot, Daemon, threading

class MyDaemon(Daemon.Daemon):

    def run(self, cfg):
        nbots = len(cfg.bots)
        for bot in cfg.bots:
            t = threading.Thread(target=bot.run, args=(randrange(nbots * 10),))
            cfg.threads.append(t)
            t.start()


class Config:

    def __init__(self):
        self.threads = []
        self.uptime = time.time()
        self.servers = []
        self.admins = []
        self.bots = []
        self.bot = None
        self.savecfg = False
        return

    def addserver(self, server, port):
        if len(self.servers) >= MAXSERVERS or server.upper() in map(str.upper, [ x[0] for x in self.servers ]):
            return False
        self.servers.append((server, port))
        return True

    def delserver(self, server):
        server = server.upper()
        self.servers = [ x for x in self.servers if x[0].upper() != server ]
        return True

    def addadmin(self, host):
        if len(self.admins) >= MAXADMINS or host.upper() in map(str.upper, self.admins):
            return False
        self.admins.append(host)
        return True

    def deladmin(self, host):
        host = host.upper()
        self.admins = [ x for x in self.admins if x.upper() != host ]
        return True

    def parseline(self, line):
        if len(line) < 2:
            return
        else:
            if line[0].upper() == 'SERVER':
                server = line[1]
                try:
                    port = int(line[2])
                except:
                    port = 6667

                self.addserver(server, port)
            elif line[0].upper() == 'ADMIN' and len(self.servers):
                try:
                    admin = decode(line[1])
                except:
                    return

                self.addadmin(admin)
            elif line[0].upper() == 'IDENT' and len(self.servers):
                if self.bot == None:
                    self.bot = Bot.Bot(self)
                elif len(self.bot.ident) and len(self.bot.realname):
                    self.bots.append(self.bot)
                    self.bot = Bot.Bot(self)
                self.bot.setident(line[1])
            elif line[0].upper() == 'REALNAME' and self.bot and len(self.bot.ident):
                self.bot.setrealname(' '.join(line[1:]))
            elif line[0].upper() == 'VHOST' and self.bot and len(self.bot.ident):
                self.bot.setvhost(line[1])
            elif line[0].upper() == 'CMDCHAR' and self.bot and len(self.bot.ident):
                self.bot.setcmdchar(line[1])
            elif line[0].upper() == 'AUTOLOGIN' and self.bot and len(self.bot.ident):
                try:
                    autologin = decode(line[1])
                except:
                    return

                autologin = autologin.split()
                self.bot.setautologin(autologin[0], autologin[1])
            elif line[0].upper() == 'NICKNAMES' and self.bot and len(self.bot.ident):
                for x in line[1:]:
                    self.bot.addnickname(x)

            elif line[0].upper() == 'CHANNEL' and self.bot and len(self.bot.ident):
                try:
                    channel = decode(line[1])
                except:
                    return

                channel = channel.split()
                key = None
                if len(channel) == 1:
                    channel.append(key)
                self.bot.addchannel(channel[0], channel[1])
            return

    def read(self, filename):
        fh = open(filename)
        for line in fh:
            self.parseline(line.split())

        if self.bot and len(self.bot.ident) and len(self.bot.realname):
            self.bots.append(self.bot)
        self.bot = None
        fh.close()
        return

    def save(self, filename):
        success = False
        if self.savecfg == True:
            return success
        self.savecfg = True
        try:
            fh = open(filename, 'w')
            for x in self.servers:
                fh.write('SERVER %s %d\n' % x)

            for x in self.admins:
                fh.write('ADMIN %s\n' % encode(x))

            count = 1
            for b in self.bots:
                fh.write('######## bot %d ########\n' % count)
                fh.write('IDENT %s\n' % b.ident)
                fh.write('REALNAME %s\n' % b.realname)
                if b.nicknames:
                    fh.write('NICKNAMES %s\n' % ' '.join(b.nicknames))
                for c in b.channels:
                    if c[1]:
                        ch = ' '.join(c)
                    else:
                        ch = c[0]
                    fh.write('CHANNEL %s\n' % encode(ch))

                if b.vhost:
                    fh.write('VHOST %s\n' % b.vhost)
                if b.autologin:
                    fh.write('AUTOLOGIN %s\n' % encode(' '.join(b.autologin)))
                fh.write('CMDCHAR %s\n' % b.cmdchar)
                count += 1

            success = True
        except IOError:
            pass
        finally:
            fh.close()
            self.savecfg = False

        return success

    def showread(self):
        print '[+] AU PORNIT:', len(self.bots)

    def show(self):
        for x in self.servers:
            print 'SERVER', x[0], x[1]

        for x in self.admins:
            print 'ADMIN', x

        for b in self.bots:
            print '###################################'
            print 'IDENT', b.ident
            print 'REALNAME', b.realname
            print 'NICKNAMES', b.nicknames
            print 'CMDCHAR', b.cmdchar
            print 'VHOST', b.vhost
            print 'AUTOLOGIN', b.autologin
            print 'CHANNELS', b.channels

    def run(self):
        daemon = MyDaemon(PID_FILE)
        if daemon.daemon_running():
            print '[-] VEZI PID IN PLM CA RULEAZA!'
            return
        if DEBUG:
            daemon.debugstart(self)
        else:
            daemon.start(self)
