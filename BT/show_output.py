from bluetooth import *

a=""

client_socket= BluetoothSocket( RFCOMM )

client_socket.connect(("30:AE:A4:18:16:FA",2))

client_socket.read(a)

print(a)


client_socket.close()
