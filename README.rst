Python IRC
=====================

:Date: 2014-06-01


.. contents::


介绍
--------

使用 Python 编写的一个 `irc` 库，可以用来对某些 `irc` 频道做日志（记录）。

使用
--------

直接命令行使用:

.. code:: bash
    
    git clone git@github.com:LuoZijun/pyirc.git
    cd pyirc
    python irc.py



在你的代码当中引用：

.. code:: python

    import irc

    host = "irc.freenode.net"
    port = 6667
    irc  = Irc(host=host, port=port, nickname="pyirc", username="python", realname="pythonbot")
    irc.connect()
    irc.loop()


资料
-------

*   `RFC7194 Default Port for Internet Relay Chat (IRC) via TLS/SSL <https://tools.ietf.org/html/rfc7194>`_
*   `RFC2813 Internet Relay Chat: Server Protocol <https://tools.ietf.org/html/rfc2813>`_
*   `RFC2812 Internet Relay Chat: Client Protocol <https://tools.ietf.org/html/rfc2812>`_
*   `RFC2811 Internet Relay Chat: Channel Management <https://tools.ietf.org/html/rfc2811>`_
*   `RFC2810 Internet Relay Chat: Architecture <https://tools.ietf.org/html/rfc2810>`_
*   `RFC1459 Internet Relay Chat Protocol <https://tools.ietf.org/html/rfc1459>`_

