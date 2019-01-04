from twisted.internet import ssl, reactor,task
from twisted.internet.protocol import ClientFactory, Protocol
from os.path import getmtime

s=0
def run(self):
   global s
   h = getmtime("Pi_dump.txt")
   if h != s:
       s = h
       with open('Pi_dump.txt') as f:
           m = next(f)  
       self.write(b'%s'% m)

class EchoClient(Protocol):
    def connectionMade(self):
        d = task.LoopingCall(run,self.transport)
        d.start(0.07)
        print("k")

    def dataReceived(self, data):
        print("Server said:", data)
        #self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

if __name__ == '__main__':
    factory = EchoClientFactory()
    reactor.connectSSL('localhost', 8000, factory, ssl.ClientContextFactory())
    reactor.run()

