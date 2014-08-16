#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:luozijun
#email:gnulinux@126.com

from multiprocessing import Process, Queue, current_process
import os,sys,time,re
import socket
from termcolor import colored

# Numeric table mostly stolen from the Perl IRC module (Net::IRC).
numeric_events = {
    "001": "welcome",
    "002": "yourhost",
    "003": "created",
    "004": "myinfo",
    "005": "featurelist",  # XXX
    "042": "uniqueid", # :hybrid8.debian.local 042 PyBot 0HYAAAAAG :your unique ID (irc-hybrid)
    "200": "tracelink",
    "201": "traceconnecting",
    "202": "tracehandshake",
    "203": "traceunknown",
    "204": "traceoperator",
    "205": "traceuser",
    "206": "traceserver",
    "207": "traceservice",
    "208": "tracenewtype",
    "209": "traceclass",
    "210": "tracereconnect",
    "211": "statslinkinfo",
    "212": "statscommands",
    "213": "statscline",
    "214": "statsnline",
    "215": "statsiline",
    "216": "statskline",
    "217": "statsqline",
    "218": "statsyline",
    "219": "endofstats",
    "221": "umodeis",
    "231": "serviceinfo",
    "232": "endofservices",
    "233": "service",
    "234": "servlist",
    "235": "servlistend",
    "241": "statslline",
    "242": "statsuptime",
    "243": "statsoline",
    "244": "statshline",
    "250": "luserconns",
    "251": "luserclient",
    "252": "luserop",
    "253": "luserunknown",
    "254": "luserchannels",
    "255": "luserme",
    "256": "adminme",
    "257": "adminloc1",
    "258": "adminloc2",
    "259": "adminemail",
    "261": "tracelog",
    "262": "endoftrace",
    "263": "tryagain",
    "265": "n_local",
    "266": "n_global",
    "300": "none",
    "301": "away",
    "302": "userhost",
    "303": "ison",
    "305": "unaway",
    "306": "nowaway",
    "311": "whoisuser",
    "312": "whoisserver",
    "313": "whoisoperator",
    "314": "whowasuser",
    "315": "endofwho",
    "316": "whoischanop",
    "317": "whoisidle",
    "318": "endofwhois",
    "319": "whoischannels",
    "321": "liststart",
    "322": "list",
    "323": "listend",
    "324": "channelmodeis",
    "329": "channelcreate",
    "331": "notopic",
    "332": "currenttopic",
    "333": "topicinfo",
    "341": "inviting",
    "342": "summoning",
    "346": "invitelist",
    "347": "endofinvitelist",
    "348": "exceptlist",
    "349": "endofexceptlist",
    "351": "version",
    "352": "whoreply",
    "353": "namreply",
    "361": "killdone",
    "362": "closing",
    "363": "closeend",
    "364": "links",
    "365": "endoflinks",
    "366": "endofnames",
    "367": "banlist",
    "368": "endofbanlist",
    "369": "endofwhowas",
    "371": "info",
    "372": "motd",
    "373": "infostart",
    "374": "endofinfo",
    "375": "motdstart",
    "376": "endofmotd",
    "377": "motd2",        # 1997-10-16 -- tkil
    "381": "youreoper",
    "382": "rehashing",
    "384": "myportis",
    "391": "time",
    "392": "usersstart",
    "393": "users",
    "394": "endofusers",
    "395": "nousers",
    # ICQ Net Host. ( {'prefix': 'irc-k01a.orange.icq.com', 'command': '396', 'arguments': ['PyBot33', '4190E6.0D7E7D.D4682B.F5CF7D', 'is now your displayed host']} )
    "396": "displayhost",
    "401": "nosuchnick",
    "402": "nosuchserver",
    "403": "nosuchchannel",
    "404": "cannotsendtochan",
    "405": "toomanychannels",
    "406": "wasnosuchnick",
    "407": "toomanytargets",
    "409": "noorigin",
    "411": "norecipient",
    "412": "notexttosend",
    "413": "notoplevel",
    "414": "wildtoplevel",
    "421": "unknowncommand",
    "422": "nomotd",
    "423": "noadmininfo",
    "424": "fileerror",
    "431": "nonicknamegiven",
    "432": "erroneusnickname", # Thiss iz how its speld in thee RFC.
    "433": "nicknameinuse",
    "436": "nickcollision",
    "437": "unavailresource",  # "Nick temporally unavailable"
    "441": "usernotinchannel",
    "442": "notonchannel",
    "443": "useronchannel",
    "444": "nologin",
    "445": "summondisabled",
    "446": "usersdisabled",
    "451": "notregistered",
    "461": "needmoreparams",
    "462": "alreadyregistered",
    "463": "nopermforhost",
    "464": "passwdmismatch",
    "465": "yourebannedcreep", # I love this one...
    "466": "youwillbebanned",
    "467": "keyset",
    "471": "channelisfull",
    "472": "unknownmode",
    "473": "inviteonlychan",
    "474": "bannedfromchan",
    "475": "badchannelkey",
    "476": "badchanmask",
    "477": "nochanmodes",  # "Channel doesn't support modes"
    "478": "banlistfull",
    "481": "noprivileges",
    "482": "chanoprivsneeded",
    "483": "cantkillserver",
    "484": "restricted",   # Connection is restricted
    "485": "uniqopprivsneeded",
    "491": "nooperhost",
    "492": "noservicehost",
    "501": "umodeunknownflag",
    "502": "usersdontmatch",
}

generated_events = [
    # Generated events
    "dcc_connect",
    "dcc_disconnect",
    "dccmsg",
    "disconnect",
    "ctcp",
    "ctcpreply",
]

protocol_events = [
    # IRC protocol events
    "error",
    "join",
    "kick",
    "mode",
    "part",
    "ping",
    "privmsg",
    "privnotice",
    "pubmsg",
    "pubnotice",
    "quit",
    "invite",
    "pong",
    "notice",
]

class Event:
    "message event"
    def __init__(self, parent, message):
        pass
    def error(self):
        pass
    def join(self):
        pass
    def kick(self):
        pass
    def mode(self):
        pass
    def part(self):
        pass
    def ping(self):
        pass
    def pong(self):
        pass
    def quit(self):
        pass
    def invite(self):
        pass
    def privmsg(self):
        pass
    def privnotice(self):
        pass
    def pubmsg(self):
        pass
    def pubnotice(self):
        pass

class Command:
    "IRC Command"
    def __init__(self):
        pass


class IRC:
    def __init__(self, server, nick, name, realname, charcode="GB18030"):
        self.server = server   # ('irc.server.com', 6667)
        self.nick = nick
        self.name = name
        self.realname = realname
        self.charcode = charcode
        self.isauth = 0
    def connect(self):
        # connect to irc server
        self.connection = socket.socket()
        self.connection.connect(self.server)
    def send(self, message):
        "send message to irc server"
        return self.connection.send(message.decode('utf8').encode(self.charcode))
    def send_raw(self,raw_message):
        "send raw message to irc server"
        return self.connection.send(raw_message)
    def set_charset(self, charcode):
        "setting message charcode."
        self.charcode = charcode
    def recv(self, inbox):
        "recv message from irc server."
        buff = ''
        while True:
            temp = self.connection.recv(4096)
            if temp:
                buff += temp
                if temp[len(temp)-2:] == '\r\n' or temp[len(temp)-1:] == '\n':
                    try:
                        buff = buff.decode(self.charcode).encode('utf8')
                    except:
                        pass
                    lines = buff.split("\r\n")
                    for line in lines:
                        if line != '':
                            #print '>> %s' %(repr(line))
                            message = self.parse(line)
                            inbox.put(message)    # 队列
    def parse(self,buff):
        "parse irc message"
        regexp = re.compile("^(:(?P<prefix>[^ ]+) +)?(?P<command>[^ ]+)( *(?P<argument> .+))?")
        m = regexp.match(buff) #_rfc_1459_command_regexp
        message = {}
        if m.group("prefix"):
            message['prefix'] = m.group("prefix")
        if m.group("command"):
            message['command'] = m.group("command").lower()
        if m.group("argument"):
            a = m.group("argument").split(" :", 1)
            arguments = a[0].split()
            if len(a) == 2:
                arguments.append(a[1])
            message['arguments'] = arguments
        return message
    def process(self, inbox):
        "process irc message"
        while True:
            message = inbox.get(True)
            if message:
                command = message['command']
                #print "++++: %s" % repr(str(message))
                try:
                    prefix = message['prefix']
                except:
                    prefix = ''
                arguments = message['arguments']
                if command and command in numeric_events:
                    if len(arguments) > 2: body = ': '.join(arguments[1:])
                    else: body = arguments[1]
                    print colored('*: ', 'red') + body
                elif command and command in protocol_events:
                    if command == 'ping':
                        self.connection.send('PONG ' + arguments[0]+'\r\n')
                    elif command == 'error':
                        #print message
                        pass
                    elif command in ['notice', 'mode', 'ping', 'invite', 'pong']:
                        if command == 'notice' and arguments[0].lower() == 'auth' and self.isauth == 0:
                            "send nick and name infomation"
                            msg = "NICK %s\nUSER %s %s bla :%s\n" % (self.nick,self.name, self.server[0], self.realname)
                            self.connection.send(msg)
                            self.isauth = 1
                        elif command == 'mode':
                            if re.match(r"^#", arguments[0]):
                                "channel mode set"
                                print message
                                #output = "[%s] <%s>: %s"  % (colored(arguments[0], 'green'), colored(source, 'green'), arguments[1] )
                            else:
                                "system mode set"
                                #{'prefix': 'PyBot33!~Python@58.48.137.198', 'command': 'mode', 'arguments': ['PyBot33', '+i']}
                                output = "%s %s %s"  % (colored('*:', 'green'), command.upper(),':'.join(arguments) )
                            print output
                        elif command == 'notice':
                            output = "%s <%s> %s" %( colored('*:', 'red'), colored(arguments[0], 'red'), arguments[1]  )
                            print output
                        else:
                            print message
                    elif command in ['privmsg', 'privnotice', 'pubmsg', 'pubnotice']:
                        if command == 'privmsg':
                            target = arguments[0]
                            if re.match(r"^:*\S+!\S+@\S+", prefix):
                                source = re.compile(r"^:*(\S+)!\S+@").findall(prefix)[0]  # nick name
                            else: source = prefix    # system host name
                            
                            if re.match(r"^#", arguments[0]):
                                "channel public talk"
                                output = "[%s] <%s>: %s"  % (colored(arguments[0], 'green'), colored(source, 'green'), arguments[1] )
                            else:
                                "prvi msg"
                                output = "<%s>: %s"  % (colored(source, 'green'), arguments[1] )
                            print output
                            # CAUTION: this is one debug.
                            if arguments[1] == "test":
                                self.connection.send("JOIN #test\r\n")
                    elif command in ['quit', 'part', 'kick', 'join']:
                        source = prefix    # system host name
                        # {'prefix': 'yyz!~luozijun@58.48.137.198', 'command': 'part', 'arguments': ['#test', 'busy']}
                        # {'prefix': 'yyz!~luozijun@58.48.137.198', 'command': 'join', 'arguments': ['#test']}
                        if re.match(r"^#", arguments[0]):
                            output = "[%s] %s: %s is %s"  % (colored(arguments[0], 'green'), colored('*','red'), colored(source, 'red'), command)
                            if len(arguments) == 2:
                                output += "(%s)" % ( arguments[1] )
                        else:
                            output = message
                        print output
                else:
                    print "*****************************Unknow**************************"
                    print message
            else: break
    def loop(self):
        "Loop recv message from irc server."
        inbox = Queue()              # message inbox.
        read_handle = Process(target=self.recv, args=(inbox,))
        process_handle = Process(target=self.process, args=(inbox,))
        
        read_handle.start()
        process_handle.start()
        
        read_handle.join()
        process_handle.join()

"""
Command:
    'PRIVMSG %s :%s:%s\r\n' %(target,source,msg.replace(self.nick + ':','').replace(self.nick,''))
    'JOIN %s\r\n' %message
    "PRIVMSG %s :我是机器人。\r\n" %(message)
    'PART %s %s\r\n' %(message,'我要躲起来～')
    'QUIT %s\r\n' %('我被终结了==')
    'PRIVMSG %s :%s:%s\r\n' %(target,source,msg.replace(self.nick + ':','').replace(self.nick,''))
    "PRIVMSG %s :yes I'm receiving it !receiving it !\r\n" %('#chinese')
    
"""


if __name__ == '__main__':
    s = IRC(('luozijun.me',6670),'PyBot33','Python','PY')
    s.connect()
    s.loop()

    """
    server  = ('irc.icq.com',6667)
    nick = 'PyBot'              # 昵称
    name = 'pybot'            # 用户名
    realname = 'PYBOT'    # 真实名称
    irc = IRC( server, nick, name, realname )
    
    while True:
        msg = irc.recv()
        if not msg:
            print '**** The MSG is None.\n'
            break
    """