IRC协议分析笔记
=====================

:Author: Luo Zijun
:Date: 2014-06-01
:Version: 0.1
:Copyright: Open
:Category: IRC,Protocol,Python


.. contents::


介绍
-------------------------------
PyIRC是我为将来集 IRC/XMPP等协议为一体的bot写的 针对 IRC协议方面的库，我的设想是该BOT能在常用的通信协议里面游走，通过自定义的方式向我推送信息，执行我发送的指令，查找资料等。

目前，对于IRC的协议并未完全支持，但是可以处理一些事情了。
鉴于中文圈里面对于这些协议的资料少之又少，所以我会继续完善这个协议，特别是文档这块。


通信流程
------------------------------

建立连接
^^^^^^^^^^^^^^

.. code:: python
    
    import sys,time,socket,os,string
    
    HOST="irc.freenode.net"
    PORT=6667
    NICK="pybot"
    IDENT="PyBot"
    REALNAME="ipybot"
    
    s=socket.socket( )
    s.connect((HOST, PORT))
    s.send("NICK %s\n" % 'bot_nick')
    s.send("USER %s %s bla :%s\n" % ('username', HOST, 'realname'))

加入房间
^^^^^^^^^^^^^^^^^

.. code:: python
    
    s.send('JOIN #chinese\n')

响应服务器的PING检测
^^^^^^^^^^^^^^^^^^^^^^^^
PING命令并不是服务器必需发送给你的，但你要保证服务器一旦发送给你PING消息，你需要把PING消息的随机字符返回给服务器，证明你还在线。

.. code:: python
    
    # ['PING', 'asimov.freenode.net\r']
    readbuffer = s.recv(4096)
    temp=string.split(readbuffer, "\n")[0].split(' :')
    if temp[0] == 'PING':
        s.send("PONG %s\r\n" % temp[1].replace('\r',''))

代码及消息类型
-------------------------------

**消息类型**

*   NOTICE
*   PRIVMSG
*   PUBMSG

**代码**

未完成……

*   001 （公告）
*   002 （描述主机地址及版本）
*   003 （描述服务器创建时间）
*   004 （）

.. code:: text

    [':asimov.freenode.net NOTICE *', '*** Looking up your hostname...\r']
    [':asimov.freenode.net NOTICE *', '*** Checking Ident\r']
    [':asimov.freenode.net 001 bot_nick', 'Welcome to the freenode Internet Relay Chat Network bot_nick\r']

**例子：**

.. code::text

    :leguin.freenode.net NOTICE * :*** Looking up your hostname...

    :leguin.freenode.net NOTICE * :*** Checking Ident
    :leguin.freenode.net NOTICE * :*** Couldn't look up your hostname

    :leguin.freenode.net NOTICE * :*** No Ident response
    :leguin.freenode.net 001 bot_nick :Welcome to the freenode Internet Relay Chat Network bot_nick
    :leguin.freenode.net 002 bot_nick :Your host is leguin.freenode.net[130.239.18.172/6667], running version ircd-seven-1.1.3
    :leguin.freenode.net 003 bot_nick :This server was created Mon Dec 31 2012 at 22:37:58 CET
    :leguin.freenode.net 004 bot_nick leguin.freenode.net ircd-seven-1.1.3 DOQRSZaghilopswz CFILMPQSbcefgijklmnopqrstvz bkloveqjfI
    :leguin.freenode.net 005 bot_nick CHANTYPES=# EXCEPTS INVEX CHANMODES=eIbq,k,flj,CFLMPQScgimnprstz CHANLIMIT=#:120 PREFIX=(ov)@+ MAXLIST=bqeI:100 MODES=4 NETWORK=freenode KNOCK STATUSMSG=@+ CALLERID=g :are supported by this server
    :leguin.freenode.net 005 bot_nick CASEMAPPING=rfc1459 CHARSET=ascii NICKLEN=16 CHANNELLEN=50 TOPICLEN=390 ETRACE CPRIVMSG CNOTICE DEAF=D MONITOR=100 FNC TARGMAX=NAMES:1,LIST:1,KICK:1,WHOIS:1,PRIVMSG:4,NOTICE:4,ACCEPT:,MONITOR: :are supported by this server
    :leguin.freenode.net 005 bot_nick EXTBAN=$,arxz WHOX CLIENTVER=3.0 SAFELIST ELIST=CTU :are supported by this server
    :leguin.freenode.net 251 bot_nick :There are 198 users and 85571 invisible on 27 servers
    :leguin.freenode.net 252 bot_nick 27 :IRC Operators online
    :leguin.freenode.net 253 bot_nick 11 :unknown connection(s)
    :leguin.freenode.net 254 bot_nick 50199 :channels formed
    :leguin.freenode.net 255 bot_nick :I have 7919 clients and 1 servers

    :leguin.freenode.net 265 bot_nick 7919 12001 :Current local users 7919, max 12001
    :leguin.freenode.net 266 bot_nick 85769 101329 :Current global users 85769, max 101329
    :leguin.freenode.net 250 bot_nick :Highest connection count: 12002 (12001 clients) (4603927 connections received)
    :leguin.freenode.net 375 bot_nick :- leguin.freenode.net Message of the Day - 
    :leguin.freenode.net 372 bot_nick :- Welcome to leguin.freenode.net in Ume�, Sweden, EU! Thanks to
    :leguin.freenode.net 372 bot_nick :- the Academic Computer Club at Ume� University for sponsoring
    :leguin.freenode.net 372 bot_nick :- this server!
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- LE GUIN, URSULA K. (1929-) Born in Berkeley, California,
    :leguin.freenode.net 372 bot_nick :- Ursula Le Guin is an american author primarily known for
    :leguin.freenode.net 372 bot_nick :- her Science Fiction and Fantasy. She has been awarded the
    :leguin.freenode.net 372 bot_nick :- Hugo and Nebula awards, and is best known for her Earthsea
    :leguin.freenode.net 372 bot_nick :- and Hainish series.
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- Welcome to freenode - supporting the free and open source
    :leguin.freenode.net 372 bot_nick :- software communities since 1998.
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- By connecting to freenode you indicate that you have read 
    and
    :leguin.freenode.net 372 bot_nick :- accept our policies as set out on http://www.freenode.net
    :leguin.freenode.net 372 bot_nick :- freenode runs an open proxy scanner. Please join #freenode for
    :leguin.freenode.net 372 bot_nick :- any network-related questions or queries, where a number of
    :leguin.freenode.net 372 bot_nick :- volunteer staff and helpful users will be happy to assist you.
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- You can meet us at FOSSCON (http://www.fosscon.org) where we get
    :leguin.freenode.net 372 bot_nick :- together with like-minded FOSS enthusiasts for talks and
    :leguin.freenode.net 372 bot_nick :- real-life collaboration.
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- We would like to thank Private Internet Access
    :leguin.freenode.net 372 bot_nick :- (https://www.privateinternetaccess.com/) and the other
    :leguin.freenode.net 372 bot_nick :- organisations that help keep freenode and our other projects
    :leguin.freenode.net 372 bot_nick :- running for their sustained support.
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- In particular we would like to thank the sponsor
    :leguin.freenode.net 372 bot_nick :- of this server, details of which can be found above.
    :leguin.freenode.net 372 bot_nick :-  
    :leguin.freenode.net 372 bot_nick :- ***************************************************************
    :leguin.freenode.net 372 bot_nick :- Please read http://blog.freenode.net/2010/11/be-safe-out-there/
    :leguin.freenode.net 372 bot_nick :- ***************************************************************
    :leguin.freenode.net 376 bot_nick :End of /MOTD command.
    :bot_nick MODE bot_nick :+i


明文消息结束标识符
---------------------------------

是应该使用 "\r\n" 还是 "\r" 还是 "\n" ？
由于历史原因，IRC RFC 规定的是"\r\n"，但是绝大部分服务器支持"\n"结束符（FreeNode/AOL）。
推荐大家使用"\n"结束符标识，同时为了兼容性对"\r\n"做下替换处理。

.. code:: python

    "Recv Message"
    Message.replace('\r\n','\n')
    "Send Message"
    sock.send('JOIN #test\r\n')

所以当我们在使用"\n"时推荐使用 "\n" 来对标识，

附录
-----------------------
关于IRC的一些标准资料。

IRC Numeric CODE
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

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

IRC Protocol String
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

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

IRC DCC
^^^^^^^^^^^^^^^

资料暂时欠缺。