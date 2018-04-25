from socketIO_client_nexus import SocketIO, LoggingNamespace

def get_data(*args):
    print('get_data:', args)


socketIO = SocketIO('https://message.waynehuang.ml', 443, LoggingNamespace)
# socketIO.emit('test')
socketIO.on('test', get_data)
socketIO.wait(seconds=1)


