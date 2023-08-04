from Vars import MAXCHANNELS, MAXNICKNAMES, MAXBUFFERSIZE, DEFCMDCHAR, DEBUG, VERSION, CODER, ISONINTERVAL, CONFIG_FILE, DA
from Functions import goodident, goodnickname, randnick, idle2str, enqueue_output, decode
import inspect, time, socket, select, errno
from subprocess import PIPE, Popen
from threading import Thread
from Queue import Queue, Empty

class UserCommands():
    """
    Metodele din clasa TREBUIE sa fie de tipul 'def do_command_nrparam(self, params):'
    params[0] = nickul adminului
    params[1] = destinatia mesajului (canalul sau daca e privat, nickul botului)
    params[2] = comanda propriuzisa
    params[3+] = argumentele
    """

    def do_die_0(self, params):
        """die (save is automatically executed)"""
        if len(self.cfg.bots) < 2:
            self.notice(params[0], "Nu poti ucide ultimul samurai!")
            return
        self.quit('Decapitat de %s.' % params[0])
        time.sleep(1)
        self.disconnect()
        self.cfg.bots = [ b for b in self.cfg.bots if b != self ]
        self.cfg.save(CONFIG_FILE)
        raise

    def do_save_0(self, params):
        """save - save to cfg file"""
        try:
            success = self.cfg.save(CONFIG_FILE)
        except:
            return False

        if not success:
            self.notice(params[0], 'Salvam pe fratesu, fututa treaba...')
        return success

    def do_show_1(self, params):
        """show <servers|admins|channels|autologin|vhost|nicknames|messages>"""
        if params[3].upper() == 'SERVERS':
            servers = ''
            for s in self.cfg.servers:
                servers += s[0] + ':' + str(s[1]) + ', '

            self.notice(params[0], 'Servers: %s.' % servers[:-2])
        elif params[3].upper() == 'ADMINS':
            admins = ''
            for a in self.cfg.admins:
                admins += a + ', '

            self.notice(params[0], 'SEFII: %s.' % admins[:-2])
        elif params[3].upper() == 'CHANNELS':
            channels = ''
            for c in self.channels:
                channels += c[0] + ':' + str(c[1]) + ', '

            self.notice(params[0], 'Channels: %s.' % channels[:-2])
        elif params[3].upper() == 'AUTOLOGIN':
            if self.autologin:
                a = self.autologin[0] + ' ' + self.autologin[1]
            else:
                a = 'None'
            self.notice(params[0], 'Autologin: %s.' % a)
        elif params[3].upper() == 'VHOST':
            if self.vhost:
                a = self.vhost
            else:
                a = 'None'
            self.notice(params[0], 'Vhost: %s.' % a)
        elif params[3].upper() == 'NICKNAMES':
            self.notice(params[0], 'Nicknames: %s.' % (' '.join(self.nicknames) or '-0-'))
        elif params[3].upper() == 'MESSAGES':
            msgfor = ''
            for x in self.messages:
                msgfor += x[2] + ', '

            if msgfor:
                msgfor = str(len(self.messages)) + ' messages for ' + msgfor[:-2]
            else:
                msgfor = 'None'
            self.notice(params[0], 'Messages: %s.' % msgfor)

    def do_add_2(self, params):
        """add <server|admin|channel|nick> <value>"""
        if params[3].upper() == 'SERVER':
            if len(params) > 5:
                try:
                    port = int(params[5])
                except:
                    port = 6667

            else:
                port = 6667
            return self.cfg.addserver(params[4], port)
        elif params[3].upper() == 'ADMIN':
            return self.cfg.addadmin(params[4])
        elif params[3].upper() == 'CHANNEL':
            key = None
            if len(params) > 5:
                key = params[5]
            return self.addchannel(params[4], key)
        elif params[3].upper() == 'NICK':
            if params[4].upper() == self.nickname.upper():
                self.timers = []
            return self.addnickname(params[4])
        else:
            return
            return

    def do_del_2(self, params):
        """del <server|admin|channel|nick> <value>"""
        if params[3].upper() == 'SERVER':
            return self.cfg.delserver(params[4])
        if params[3].upper() == 'ADMIN':
            return self.cfg.deladmin(params[4])
        if params[3].upper() == 'CHANNEL':
            return self.delchannel(params[4])
        if params[3].upper() == 'NICK':
            if params[4].upper() == self.nickname.upper():
                self.addtimer('ison', 0, ISONINTERVAL, self.ison)
            return self.delnickname(params[4])

    def do_set_2(self, params):
        """set <vhost|autologin> <value|null>"""
        success = False
        if params[3].upper() == 'VHOST':
            if params[4].upper() == 'NULL':
                self.delvhost()
            else:
                self.setvhost(params[4])
            success = True
        elif params[3].upper() == 'AUTOLOGIN':
            if params[4].upper() == 'NULL':
                self.delautologin()
                success = True
            elif len(params) > 5:
                self.setautologin(params[4], params[5])
                success = True
        return success

    def do_delmessages_0(self, params):
        """delmessages"""
        self.messages = []
        return True

    def do_leavemsg_2(self, params):
        """leavemsg <username|host> <message> - leave messages for users when they are active on channel (max 20 messages and use on channel only)"""
        if len(self.messages) <= 20 and params[1][0] == '#' and params[3].isalnum() and len(params[3]) > 1:
            message = ' '.join(params[4:])
            self.messages.append((params[0],
             params[1],
             params[3],
             message))
            adminreply = 'Message saved.'
        else:
            adminreply = 'Something is wrong.'
        self.notice(params[0], adminreply)

    def do_op_0(self, params):
        """op [channels] [nicknames]"""
        channel = None
        nicknames = []
        if params[1][0] == '#':
            channel = params[1]
        parlen = len(params)
        if parlen > 3:
            if params[3][0] == '#':
                channel = params[3]
            else:
                nicknames.append(params[3])
            if parlen > 4:
                for nick in params[4:]:
                    nicknames.append(nick)

            elif params[3][0] == '#':
                nicknames.append(params[0])
        elif params[1][0] == '#':
            channel = params[1]
            nicknames.append(params[0])
        if channel and nicknames:
            if '*' in nicknames:
                self.names(channel)
            else:
                self.op(channel, nicknames)
        return

    def do_deop_0(self, params):
        """deop [channels] [nicknames]"""
        channel = None
        nicknames = []
        if params[1][0] == '#':
            channel = params[1]
        parlen = len(params)
        if parlen > 3:
            if params[3][0] == '#':
                channel = params[3]
            else:
                nicknames.append(params[3])
            if parlen > 4:
                for nick in params[4:]:
                    nicknames.append(nick)

            elif params[3][0] == '#':
                nicknames.append(params[0])
        elif params[1][0] == '#':
            channel = params[1]
            nicknames.append(params[0])
        if channel and nicknames:
            if '*' in nicknames:
                self.names(channel)
            else:
                self.deop(channel, nicknames)
        return

    def do_voice_0(self, params):
        """voice [channels] [nicknames]"""
        channel = None
        nicknames = []
        if params[1][0] == '#':
            channel = params[1]
        parlen = len(params)
        if parlen > 3:
            if params[3][0] == '#':
                channel = params[3]
            else:
                nicknames.append(params[3])
            if parlen > 4:
                for nick in params[4:]:
                    nicknames.append(nick)

            elif params[3][0] == '#':
                nicknames.append(params[0])
        elif params[1][0] == '#':
            channel = params[1]
            nicknames.append(params[0])
        if channel and nicknames:
            if '*' in nicknames:
                self.names(channel)
            else:
                self.voice(channel, nicknames)
        return

    def do_devoice_0(self, params):
        """devoice [channels] [nicknames]"""
        channel = None
        nicknames = []
        if params[1][0] == '#':
            channel = params[1]
        parlen = len(params)
        if parlen > 3:
            if params[3][0] == '#':
                channel = params[3]
            else:
                nicknames.append(params[3])
            if parlen > 4:
                for nick in params[4:]:
                    nicknames.append(nick)

            elif params[3][0] == '#':
                nicknames.append(params[0])
        elif params[1][0] == '#':
            channel = params[1]
            nicknames.append(params[0])
        if channel and nicknames:
            if '*' in nicknames:
                self.names(channel)
            else:
                self.devoice(channel, nicknames)
        return

    def do_invite_1(self, params):
        """invite <channel> [nickname]"""
        success = False
        parlen = len(params)
        if params[3][0] == '#':
            channel = params[3]
            if parlen > 4:
                nick = params[4]
            else:
                nick = params[0]
            self.invite(channel, nick)
            success = True
        elif params[1][0] == '#':
            self.invite(params[1], params[3])
            success = True
        return success

    def do_msg_2(self, params):
        """msg <nick/#channel> <msg>"""
        self.privmsg(params[3], ' '.join(params[4:]))
        return True

    def do_notice_2(self, params):
        """notice <nick/#channel> <msg>"""
        self.notice(params[3], ' '.join(params[4:]))
        return True

    def do_away_0(self, params):
        """away [away msg]"""
        awaymsg = None
        if len(params) > 3:
            awaymsg = ' '.join(params[3:])
        self.away(awaymsg)
        return True

    def do_nextserver_0(self, params):
        """nextserver [ident] [realname]"""
        if len(params) > 4:
            self.setident(params[3])
            self.setrealname(' '.join(params[4:]))
        self.quit('ZNC 1.7.5+deb4 - https://znc.in')
        time.sleep(1)
        self.disconnect()

    def do_server_1(self, params):
        """server <server> [port] [ident] [realname]"""
        parlen = len(params)
        server = params[3]
        if parlen > 4:
            try:
                port = int(params[4])
            except:
                port = 6667

        else:
            port = 6667
        if parlen > 6:
            self.setident(params[5])
            self.setrealname(' '.join(params[6:]))
        self.quit('ZNC 1.7.5+deb4 - https://znc.in')
        time.sleep(1)
        self.disconnect()
        self.connect((server, port))

    def do_login_2(self, params):
        """login <user> <pass> - login to x@channels.undernet.org"""
        self.privmsg('x@channels.undernet.org', 'login ' + params[3] + ' ' + params[4])
        return True

    def do_cmdchar_0(self, params):
        """cmdchar [cmdchar]"""
        if len(params) > 3:
            self.setcmdchar(params[3])
        self.notice(params[0], "Simbolul folosit actual este '%s'" % self.cmdchar)

    def do_shell_1(self, params):
        """shell <shell command>"""
        p = Popen(' '.join(params[3:]), shell=True, stdout=PIPE)
        q = Queue()
        t = Thread(target=enqueue_output, args=(p.stdout, q))
        t.start()
        while True:
            try:
                line = q.get(timeout=1)
            except Empty:
                break
            else:
                self.notice(params[0], line)

    def do_ontime_0(self, params):
        """ontime"""
        self.notice(params[0], self.getontime())

    def do_uptime_0(self, params):
        """uptime"""
        self.notice(params[0], self.getuptime())

    def do_cserv_0(self, params):
        """cserv"""
        self.notice(params[0], 'Sunt conectat pe: %s' % self.servername)

    def do_part_1(self, params):
        """part [channel] [message]"""
        channel = None
        msg = None
        parlen = len(params)
        if parlen > 3:
            if params[3][0] == '#':
                channel = params[3]
                if parlen > 4:
                    msg = ' '.join(params[4:])
            elif params[1][0] == '#':
                channel = params[1]
                msg = ' '.join(params[3:])
        elif params[1][0] == '#':
            channel = params[1]
        if channel:
            if msg:
                self.part(channel, msg)
            else:
                self.part(channel)
        return

    def do_join_1(self, params):
        """join <channel> [key]"""
        channel = None
        key = None
        parlen = len(params)
        if parlen > 3:
            if params[3][0] == '#':
                channel = params[3]
            if parlen > 4:
                key = params[4]
            if channel:
                self.join((channel, key))
        return

    def do_nick_1(self, params):
        """nick <nickname>"""
        if len(params) > 3:
            self.nick(params[3])

    def do_rnick_0(self, params = None):
        """rnick"""
        self.nick(randnick())

    def do_version_0(self, params):
        """version"""
        self.notice(params[0], 'VERS. %s BY %s' % (4.1, -CARTIER- #Cristi uNET))

    def do_help_0(self, params):
        """help [command]"""
        if len(params) > 3:
            for cmd in inspect.getmembers(UserCommands, predicate=inspect.ismethod):
                if params[3].upper() == cmd[0][3:].split('_')[0].upper():
                    self.notice(params[0], 'Usage: %s' % cmd[1].__doc__)
                    return

            self.notice(params[0], 'AMICE: COMANDA ASTA O DAI TU IN PADURE!')
        elif len(params) == 3:
            cmds = ''
            for cmd in inspect.getmembers(UserCommands, predicate=inspect.ismethod):
                cmds += cmd[0][3:].split('_')[0] + ', '

            self.notice(params[0], 'Commands: %s' % cmds[:-2])


class ServerEvents():
    """
    Fiecare metoda prelucreaza comanda respectiva
    Daca comanda primita de la server nu este gasita aici, ea este ignorata
    Formatul metodelor: def on_command(self, params):
    params[0] = de cine este trimisa comanda (server/user)
    params[1] = comanda propriuzisa, on_ + comanda mereu e la fel ca numele functiei
    params[2+] = argumentele
    """

    def on_ping(self, param):
        """ping message"""
        self.send('PONG %s' % param)

    def on_join(self, params):
        """join message"""
        if self.isadmin(params[0].split('@')[1]):
            self.mode(params[2], '+o', params[0][1:].split('!')[0])
        if self.messages:
            channel = params[2]
            user = params[0].split('@')[1]
            if user.endswith('.users.undernet.org'):
                user = user[:-19]
            for x in self.messages:
                if x[1].upper() == channel.upper() and x[2].upper() == user.upper():
                    self.notice(params[0][1:].split('!')[0], 'Message from %s: "%s"' % (x[0], x[3]))
                    self.messages.remove(x)

    def on_quit(self, params):
        """quit message"""
        nickquit = params[0][1:].split('!')[0]
        nickquit = self.isnickwanted(nickquit)
        if nickquit and not self.isnickwanted(self.nickname):
            self.send('NICK %s' % nickquit)

    def on_nick(self, params):
        """nick event, when someone is changing nickname"""
        nickfrom = params[0][1:].split('!')[0]
        if params[2][0] == ':':
            params[2] = params[2][1:]
        nickto = params[2]
        if nickfrom == nickto:
            return
        if nickfrom == self.nickname:
            self.nickname = nickto
            if self.isnickwanted(nickto):
                self.deltimer('ison')
                self.away(decode(DA))
            elif self.isnickwanted(nickfrom):
                self.addtimer('ison', 0, ISONINTERVAL, self.ison)
        elif not self.isnickwanted(self.nickname):
            nick = self.isnickwanted(nickfrom)
            if nick:
                self.send('NICK %s' % nick)

    def on_privmsg(self, params):
        """privmsg event, when someone msg on privat or channel"""
        if self.messages:
            channel = params[2]
            user = params[0].split('@')[1]
            if user.endswith('.users.undernet.org'):
                user = user[:-19]
            for x in self.messages:
                if x[1].upper() == channel.upper() and x[2].upper() == user.upper():
                    self.notice(params[0][1:].split('!')[0], 'Message from %s: "%s"' % (x[0], x[3]))
                    self.messages.remove(x)

        if self.isadmin(params[0].split('@')[1]):
            params[0] = params[0][1:].split('!')[0]
            del params[1]
            params[2] = params[2][1:]
            if params[2].upper() == self.nickname.upper():
                if len(params) > 3:
                    del params[2]
                    self.do_command(params)
            elif len(params[2]) > 1 and params[2][0] == self.cmdchar:
                params[2] = params[2][1:]
                self.do_command(params)
            elif params[1][0] != '#':
                self.do_command(params)

    def on_kick(self, params):
        """kick event, when someone got kicked"""
        if params[3] == self.nickname:
            self.join((params[2], None))
        return

    def on_001(self, params):
        """First server message (Welcome message)"""
        self.flags['erroronconnect'] = 0
        self.flags['nextconnect'] = 5
        self.nickname = params[2]
        self.servername = params[0][1:]
        self.setontime()

    def on_303(self, params):
        """ISON server message"""
        params[3] = params[3][1:]
        self.checkison(params[3:])

    def on_353(self, params):
        """NAMES reply"""
        params[5] = params[5][1:]
        self.channelnames += params[5:]

    def on_366(self, params):
        """End of /NAMES list"""
        if self.cmd == 'op':
            nicklist = [ nick for nick in self.channelnames if nick[0] is not '@' and nick[0] is not '+' ]
            nicklist += [ nick[1:] for nick in self.channelnames if nick[0] is '+' ]
            self.op(params[3], nicklist)
        elif self.cmd == 'deop':
            self.deop(params[3], [ nick[1:] for nick in self.channelnames if nick[0] is '@' and nick[1:] != self.nickname ])
        elif self.cmd == 'voice':
            self.voice(params[3], [ nick for nick in self.channelnames if nick[0] is not '@' and nick[0] is not '+' ])
        elif self.cmd == 'devoice':
            self.devoice(params[3], [ nick[1:] for nick in self.channelnames if nick[0] is '+' ])
        self.channelnames = []

    def on_376(self, params):
        """End of MOTD"""
        if self.autologin:
            self.addtimer('login', 1, 1, self.do_login_2, [None,
             None,
             None,
             self.autologin[0],
             self.autologin[1]])
        self.addtimer('modeix', 1, 1, self.mode, self.nickname, '+ix')
        self.addtimer('joinchannels', 1, 3, self.joinallchannels)
        self.addtimer('silence', 1, 5, self.silence)
        self.addtimer('ison', 0, ISONINTERVAL, self.ison)
        return

    def on_422(self, params):
        """No MOTD"""
        self.on_376(params)

    def on_433(self, params):
        """Nickname already in use"""
        if params[2] == '*':
            self.do_rnick_0()

    def on_432(self, params):
        """Erroneous Nickname"""
        self.on_433(params)

    def on_465(self, params):
        """Banned from server (G-Line)"""
        self.flags['nextconnect'] = 7200


class BotCommands():
    """
    Aceasta clasa contine comenzile pe care botul le poate trimite serverului
    """

    def away(self, msg = None):
        """set away msg"""
        if msg:
            self.send('AWAY :%s' % msg)
        else:
            self.send('AWAY')

    def names(self, channel):
        """send names command"""
        self.send('NAMES %s' % channel)

    def invite(self, channel, nick):
        """invite a nickname to a channel"""
        self.send('INVITE %s %s' % (nick, channel))

    def mode(self, dest, flags, values = ''):
        """set modes on channel and users"""
        self.send('MODE %s %s %s' % (dest, flags, values))

    def op(self, channel, nicknames):
        """op nicknames on channel"""
        if type(nicknames) == str:
            nicknames = [nicknames]
        index = 0
        nickblock = nicknames[index:index + 6]
        while nickblock:
            nnicks = len(nickblock)
            flags = '+' + 'o' * nnicks
            self.mode(channel, flags, ' '.join(nickblock))
            index += 6
            nickblock = nicknames[index:index + 6]

    def deop(self, channel, nicknames):
        """deop nicknames on channel"""
        if type(nicknames) == str:
            nicknames = [nicknames]
        index = 0
        nickblock = nicknames[index:index + 6]
        while nickblock:
            nnicks = len(nickblock)
            flags = '-' + 'o' * nnicks
            self.mode(channel, flags, ' '.join(nickblock))
            index += 6
            nickblock = nicknames[index:index + 6]

    def voice(self, channel, nicknames):
        """voice nicknames on channel"""
        if type(nicknames) == str:
            nicknames = [nicknames]
        index = 0
        nickblock = nicknames[index:index + 6]
        while nickblock:
            nnicks = len(nickblock)
            flags = '+' + 'v' * nnicks
            self.mode(channel, flags, ' '.join(nickblock))
            index += 6
            nickblock = nicknames[index:index + 6]

    def devoice(self, channel, nicknames):
        """devoice nicknames on channel"""
        if type(nicknames) == str:
            nicknames = [nicknames]
        index = 0
        nickblock = nicknames[index:index + 6]
        while nickblock:
            nnicks = len(nickblock)
            flags = '-' + 'v' * nnicks
            self.mode(channel, flags, ' '.join(nickblock))
            index += 6
            nickblock = nicknames[index:index + 6]

    def notice(self, to, msg):
        """send a notice message 'msg' to 'to'"""
        self.send('NOTICE %s :%s' % (to, msg))

    def nick(self, nickname):
        """send nick command"""
        self.send('NICK %s' % nickname)

    def privmsg(self, to, msg):
        """send a privmsg message 'msg' to 'to'"""
        self.send('PRIVMSG %s :%s' % (to, msg))

    def silence(self):
        """set silence for all users that are not logged in to cservice"""
        self.send('SILENCE +*!*@*,~*!*@*.users.undernet.org')

    def part(self, channel, msg = 'Left all channels'):
        """part a channel with given msg"""
        self.send('PART %s :%s' % (channel, msg))

    def join(self, channels):
        """join channel, multiple channels allowed"""
        if type(channels) == list:
            cmd = ''
            for ch in channels:
                cmd += ch[0] + ','

            cmd = cmd[:-1] + ' '
            for ch in self.channels:
                if ch[1] is not None:
                    cmd += ch[1] + ','
                else:
                    cmd += ','

            cmd = cmd[:-1]
            self.send('JOIN %s' % cmd)
        elif type(channels) == tuple:
            self.send('JOIN %s %s' % (channels[0], channels[1]))
        return

    def quit(self, msg = 'ZNC 1.6.6+deb1ubuntu0.2 - http://znc.in'):
        """send quit message"""
        self.send('QUIT :%s' % msg)


class Bot(BotCommands, ServerEvents, UserCommands):

    def __init__(self, cfg):
        self.cfg = cfg
        self.messages = []
        self.channelnames = []
        self.nicknames = []
        self.nickname = ''
        self.hostname = ''
        self.servername = ''
        self.channels = []
        self.ident = ''
        self.realname = ''
        self.vhost = ''
        self.cmdchar = DEFCMDCHAR
        self.autologin = ()
        self.buffer = ''
        self.timers = []
        self.flags = {}
        self.cmd = None
        self.lastmsgrecv = None
        self.flags['connected'] = False
        self.flags['nextserver'] = 0
        self.flags['nextconnect'] = 0
        self.flags['erroronconnect'] = 0
        self.flags['laggy'] = False
        self.flags['freeze'] = False
        return

    def do_command(self, params):
        """Executing command `params[2]` if is found in UserCommands"""
        for cmd in inspect.getmembers(UserCommands, predicate=inspect.ismethod):
            if cmd[0].startswith('do_'):
                try:
                    prefix, command, nparam = cmd[0].split('_')
                    nparam = int(nparam)
                except:
                    continue

                if params[2].upper() == command.upper():
                    if len(params) < nparam + 3:
                        params[2] = 'help'
                        params = params[:3]
                        params.append(command)
                        self.do_help_0(params)
                        return
                    else:
                        self.cmd = command
                        if cmd[1](self, params):
                            self.notice(params[0], 'Done.')
                        return

    def disconnect(self):
        if DEBUG:
            print '[%d] Disconnect' % self.socket.getsockname()[1]
        self.socket.close()
        self.flags['connected'] = False
        if not self.flags['nextconnect']:
            self.flags['nextconnect'] = 5
        self.timers = []
        self.channelnames = []
        self.lastmsgrecv = None
        self.flags['laggy'] = False
        self.flags['freeze'] = False
        return

    def isadmin(self, host):
        """Check if host is in admins list"""
        return host.upper() in map(str.upper, self.cfg.admins)

    def ison(self):
        if self.flags['freeze']:
            self.flags['freeze'] += 1
            if self.flags['freeze'] == 4:
                self.flags['freeze'] = 0
            return
        if len(self.nicknames) > 10:
            self.send('ISON %s' % ' '.join(self.nicknames), 0)
        elif len(self.nicknames) == 10:
            self.send('NICK %s' % self.nicknames[0], 0)

    def checkison(self, nicks):
        n = set((item.upper() for item in nicks))
        fn = next((item for item in self.nicknames if item.upper() not in n), '')
        if fn:
            self.send('NICK %s' % fn)

    def joinallchannels(self):
        if not len(self.channels):
            return
        self.join(self.channels)

    def setontime(self):
        self.ontime = time.time()

    def getontime(self):
        ontime = int(time.time() - self.ontime)
        return 'Ontime: %s' % idle2str(ontime)

    def getuptime(self):
        uptime = int(time.time() - self.cfg.uptime)
        return 'Uptime: %s' % idle2str(uptime)

    def isnickwanted(self, nick):
        return next((n for n in self.nicknames if n.upper() == nick.upper()), None)

    def addnickname(self, nick):
        if len(self.nicknames) >= MAXNICKNAMES or not goodnickname(nick) or nick.upper() in map(str.upper, [ n for n in self.nicknames ]):
            return False
        self.nicknames.append(nick)
        return True

    def delnickname(self, nick):
        nick = nick.upper()
        self.nicknames = [ x for x in self.nicknames if x.upper() != nick ]
        return True

    def addchannel(self, channel, key = None):
        if channel[0] is not '#' or len(self.channels) >= MAXCHANNELS or channel.upper() in map(str.upper, [ x[0] for x in self.channels ]):
            return False
        self.channels.append((channel, key))
        return True

    def delchannel(self, channel):
        channel = channel.upper()
        self.channels = [ x for x in self.channels if x[0].upper() != channel ]
        return True

    def setident(self, ident):
        if not goodident(ident):
            return False
        self.ident = ident
        return True

    def setrealname(self, realname):
        self.realname = realname

    def setvhost(self, vhost):
        self.vhost = vhost

    def delvhost(self):
        self.vhost = ''

    def setcmdchar(self, cmdchar):
        if len(cmdchar) != 1:
            return False
        self.cmdchar = cmdchar
        return True

    def setautologin(self, user, password):
        if not len(user) or not len(password):
            return False
        self.autologin = (user, password)
        return True

    def delautologin(self):
        self.autologin = ()

    def send(self, msg, freeze = 1):
        if DEBUG:
            print '[->%d] %s' % (self.socket.getsockname()[1], msg)
        msg += '\r\n'
        self.socket.send(msg)
        self.flags['freeze'] = freeze

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server):
        time.sleep(self.flags['nextconnect'])
        if DEBUG:
            print '[+] Ma conectez la %s:%d\n' % server
        try:
            self.create_socket()
            self.socket.settimeout(20)
            self.socket.bind((self.vhost, 0))
            self.socket.connect(server)
            self.do_rnick_0()
            self.send('USER %s "" "%s" :%s' % (self.ident, server[0], self.realname))
            self.flags['connected'] = True
            return True
        except socket.error as e:
            if e.errno == errno.EADDRNOTAVAIL:
                self.delvhost()
            self.disconnect()
            return False

    def readlines(self):
        self.buffer += self.socket.recv(MAXBUFFERSIZE)
        while '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            yield line

    def readdata(self):
        self.lastmsgrecv = time.time()
        try:
            for line in self.readlines():
                if DEBUG:
                    print '[<-%d] %s' % (self.socket.getsockname()[1], line)
                line = line.split()
                if len(line):
                    if line[0][0] == ':':
                        for cmd in inspect.getmembers(ServerEvents, predicate=inspect.ismethod):
                            if line[1].lower() == cmd[0][3:]:
                                cmd[1](self, line)
                                continue

                    elif line[0] == 'PING':
                        self.on_ping(line[1])
                    elif line[0] == 'ERROR':
                        self.disconnect()

        except socket.error as e:
            if e.errno == errno.ECONNRESET or e.errno == errno.ECONNABORTED:
                self.flags['erroronconnect'] += 1
                if self.flags['erroronconnect'] >= 5:
                    self.flags['erroronconnect'] = 0
                    self.flags['nextconnect'] = 61
                self.disconnect()

    def checkdata(self):
        if not self.flags['connected']:
            return False
        else:
            read_s, write_s, err_s = select.select([self.socket], [], [], 0.1)
            if self.socket in read_s:
                return True
            return False

    def addtimer(self, name, iter, timeout, func, *params):
        if timeout <= 0 or iter < 0:
            return False
        for timer in self.timers:
            if timer[0] is name:
                return False

        self.timers.append([name,
         0,
         0,
         iter,
         timeout,
         func,
         params])
        return True

    def deltimer(self, name):
        self.timers = [ timer for timer in self.timers if timer[0] is not name ]

    def dotimers(self):
        for timer in self.timers:
            if round(timer[2], 1) == timer[4]:
                timer[5](*timer[6])
                timer[2] = 0
                if timer[3] != 0:
                    timer[1] += 1
                    if timer[1] >= timer[3]:
                        self.deltimer(timer[0])
            timer[2] += 0.1

    def run(self, sleeptime):
        time.sleep(sleeptime)
        while True:
            if not self.flags['connected']:
                self.connect(self.cfg.servers[self.flags['nextserver']])
                self.flags['nextserver'] += 1
                if self.flags['nextserver'] >= len(self.cfg.servers):
                    self.flags['nextserver'] = 0
            if self.checkdata():
                self.readdata()
            else:
                self.dotimers()
                if self.lastmsgrecv:
                    timeago = time.time() - self.lastmsgrecv
                    if timeago > 150 and not self.flags['laggy']:
                        self.flags['laggy'] = True
                        self.send('PING :TIMEOUTCHECK')
                    elif timeago > 210:
                        self.quit("Pong timeout")
                        self.disconnect()