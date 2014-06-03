#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:luozijun
#email:gnulinux@126.com

import os,sys,time,re
import socket

# Numeric table mostly stolen from the Perl IRC module (Net::IRC).
numeric_events = {
    "001": "welcome",
    "002": "yourhost",
    "003": "created",
    "004": "myinfo",
    "005": "featurelist",  # XXX
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
]






class IRC:
    def __init__(self,server,nick,name,realname):
        "初始化"
        self.server = server  # tuple , like (HOST,PORT)
        self.nick = nick
        self.name = name
        self.realname = realname
        self.conn = self.connection()
    def connection(self):
        "建立IRC协议连接"
        s = socket.socket()
        s.connect(self.server)
        s.send("NICK %s\nUSER %s %s bla :%s\n" % (self.nick,self.name, self.server[0], self.realname))
        return s
    def send(self,msg):
        "发送信息"
        return self.conn.send(msg)
    def recv(self):
        "接收信息"
        buff = ''
        while True:
            temp = self.conn.recv(4096)
            if not temp:
                break
            buff = buff + temp
            if temp[len(temp)-2:] == '\r\n' or temp[len(temp)-1:] == '\n':
                # 数据结束,解析
                self.parse(buff)
                buff = ''
    def parse(self,buff):
        buff = buff.replace('\r\n','\n').split('\n')
        for line in buff:
            line = line.rstrip()
            if line:
                _rfc_1459_command_regexp = re.compile("^(:(?P<prefix>[^ ]+) +)?(?P<command>[^ ]+)( *(?P<argument> .+))?")
                m = _rfc_1459_command_regexp.match(line)
                if m.group("prefix"):
                    "server name/nick mask/protocol event"
                    "verne.freenode.net / luozijun!~luozijun@58.48.138.43 / "
                    # 当 command 为 mode 时，prefix 为 nick.
                    # 当 command 为 ping 时，prefix为 空
                    prefix = m.group("prefix")
                if m.group("command"):
                    command = m.group("command").lower()
                if m.group("argument"):
                    a = m.group("argument").split(" :", 1)
                    arguments = a[0].split()
                    if len(a) == 2:
                        arguments.append(a[1])

                if command == 'ping':
                    print('心跳：' + arguments[0] )
                    self.send('PONG ' + arguments[0]+'\r\n')
                elif command in ["privmsg", "notice"]:
                    target, message = arguments[0], arguments[1]
                    #messages = _ctcp_dequote(message)
                    if command == "privmsg":
                        if target[0:1] in "#&+!":
                            command = "pubmsg"
                    else:
                        if target[0:1] in "#&+!":
                            command = "pubnotice"
                        else:
                            command = "privnotice"
                    if '@' in prefix:
                        source = prefix.split('!')[0]
                    else:
                        source = prefix
                    print("%s From %s To %s : %s" %(command,source,target,message.decode('GB18030')))
                    if '#' in message:
                        # 加入频道
                        self.send('JOIN %s\r\n' %message )
                        self.send("PRIVMSG %s :我来了。\r\n" %(message) )
                    elif message == 'quit':
                        self.send('PART %s %s\r\n' %(message,'我要躲起来～') )
                        self.conn.close()
                    elif message == 'part':
                        self.send("PRIVMSG %s :yes I'm receiving it !receiving it !\r\n" %(source) )
                        self.send('QUIT %s\r\n' %('我被终结了==') )
                        
                elif command in numeric_events:
                    # 代码消息（系统代码）
                    if int(command) == 433:
                        # 需要检查 nickserver@!NickServer 的对话，避免昵称已被占用
                        print('系统：昵称 %s 已经被占用' %arguments[1] )
                    else:
                        print(repr(str(line)))
                        #print("System %s : %s    command: %s" %(str(prefix),str(arguments),str(command)) )
                elif command in protocol_events:
                    # 协议消息（ERROR/PONG....）
                    try:
                        print("command : %s  %s" %(command,arguments[1]))
                    except:
                        print('协议消息打印异常：%s' % ( repr(str(line)) ))
                else:
                    print(repr(str(line)))


if __name__ == '__main__':
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
