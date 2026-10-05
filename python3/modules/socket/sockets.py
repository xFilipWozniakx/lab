import socket
# model
# create communication channel ( socket )
# bind address + port to that socket ( bind )
# start listening ( listen )
# accept incoming connection ( accept )

#
# ┌──────────┬──────────────┬──────────────────────┐
# │ TYPE     │ LENGTH       │ PAYLOAD              │
# │ 1 bajt   │ 4 bajty      │ LENGTH bajtów        │
# └──────────┴──────────────┴──────────────────────┘
#

#
# 1. odbiera 1 bajt TYPE
# 2. sprawdza TYPE
# 3. odbiera 4 bajty LENGTH
# 4. sprawdza LENGTH
# 5. odbiera dokładnie LENGTH bajtów
# 6. sprawdza, czy odebrał kompletny payload
# 7. interpretuje payload zależnie od TYPE
#

# AF_INET for ipv4 / SOCK_STREAM for TCP protocol

server = socket.socket(AF_INET, SOCK_STREAM)
server.bind(("0.0.0.0", 5555))
