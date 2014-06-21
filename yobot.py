# Ben Eggers
# Much of this code was borrowed

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

import time, sys


class Yobot(irc.IRCClient):
        
    nickname = "yobot"

    def __init__(self):
        self.shut_up = False

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        if msg == "YO" and not self.shut_up:
            self.msg(channel, "YO")
        elif msg == "SHUT UP YOBOT":
            self.msg(channel, "You got it, fleshbag")
            self.shut_up = True
        elif msg[0:9] == "YO, YOBOT":
            self.msg(channel, "What's up, boss?")
            self.shut_up = False

class YobotFactory(protocol.ClientFactory):

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = Yobot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    f = YobotFactory(sys.argv[1])
    reactor.connectTCP("irc.adelais.net", 6667, f)
    reactor.run()