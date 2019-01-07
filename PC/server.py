from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol

class Echo(Protocol):
    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
        with open('Server_dump.txt','w') as f:
                f.write(str(data))
        print(str(data))
        #self.transport.write(data)

if __name__ == '__main__':
    factory = Factory()
    factory.protocol = Echo
    reactor.listenSSL(8000, factory,
                      ssl.DefaultOpenSSLContextFactory(
            'server.key', 'server.crt'))
    reactor.run()
