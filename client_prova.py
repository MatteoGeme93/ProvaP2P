import hashlib

import socket

from pathlib import Path

class Peer:

    def __init__(self):
        self.ip_dir = '10.14.98.199'  # edit for presentation
        self.dir_port = 3000
        self.dir_addr = (self.ip_dir, self.dir_port)

        self.my_ipv4 = '10.0.2.15'
        #self.my_ipv6 = 'fe80::ac89:c3f8:ea1a:ca4b'
        self.pPort = 50001  # peer port for receaving connection from other peer

    # -------- fase di login e logout con la directory --------

    def connection(self):
        try:
            # this is for ipv4 and ipv6
            self.infoS = socket.getaddrinfo(self.ip_dir, self.dir_port)
            self.s = socket.socket(*self.infoS[0][:3])
            self.s.connect(self.infoS[0][4])

        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.connect(self.dir_addr)
        except IOError as expt:  # l'eccezione ha una sotto eccez. per la socket
            print("Errore nella connessione alla directory --> " + expt)

    def deconnection(self):
        try:
            self.s.close()
        except IOError as expt:  # l'eccezione ha una sotto eccez. per la socket
            print("Errore nella connessione alla directory --> " + expt)

    def login(self):
        print("\n--- LOGIN ---\n")

        self.connection()

        # self.ipp2p_bf = self.s.getsockname()[0] #ip peer bad formatted

        # formattazione ip
        self.split_ip = self.my_ipv4.split(".")
        ip1 = self.split_ip[0].zfill(3)
        ip2 = self.split_ip[1].zfill(3)
        ip3 = self.split_ip[2].zfill(3)
        ip4 = self.split_ip[3].zfill(3)

        self.ipp2p = ip1 + '.' + ip2 + '.' + ip3 + '.' + ip4

        # formattazione porta
        self.pp2p_bf = self.s.getsockname()[1]  # porta peer bad formatted
        self.pp2p = '%(#)03d' % {"#": int(self.pp2p_bf)}

        data_login = "LOGI" + self.ipp2p + self.pp2p

        self.s.send(data_login.encode('ascii'))

        self.ack_login = self.s.recv(20)  # 4B di ALGI + 16B di SID

        print("Ip peer ---> " + str(self.ipp2p))
        print("Port peer ---> " + str(self.pp2p))
        print("First 4 byte from dir----> " + str(self.ack_login[:4].decode()))

        if (self.ack_login[:4].decode() == "ALGI"):
            self.sid = self.ack_login[4:20]

            if (self.sid == '0000000000000000'):
                print("Errore durante il login\n")
                exit()
            else:
                print("Session ID ---> " + str(self.sid.decode()) + "\n")
        else:
            print("Errore del pacchetto, string 'ALGI' non trovata")
            exit()

        self.deconnection()

    def aggiunta(self, file):

        print("\n--- AGGIUNTA ---\n")

        #verifico l'esistenza del file

        check_file = Path(file)

        if (check_file.is_file()):
        
            self.f = open(file, 'rb')
            self.contenuto = self.f.read()
            self.filename = self.f.name

            FileHash = hashlib.md5()
            FileHash.update(self.contenuto)
            FileHash.hexdigest()

            if (len(self.filename)<32):
                self.filename = self.filename.ljust(32, ' ')

            self.connection()

            # formattazione ip
            self.split_ip = self.my_ipv4.split(".")
            ip1 = self.split_ip[0].zfill(3)
            ip2 = self.split_ip[1].zfill(3)
            ip3 = self.split_ip[2].zfill(3)
            ip4 = self.split_ip[3].zfill(3)

            self.ipp2p = ip1 + '.' + ip2 + '.' + ip3 + '.' + ip4

            # formattazione porta
            self.pp2p_bf = self.s.getsockname()[1]  # porta peer bad formatted
            self.pp2p = '%(#)03d' % {"#": int(self.pp2p_bf)}

            data_add_file = "ADDF"+FileHash.hexdigest()+self.filename

            self.s.send(data_add_file.encode())

            print("Ip peer ---> " + str(self.ipp2p))
            print("Port peer ---> " + str(self.pp2p))
            print(data_add_file)

            self.ack_login = self.s.recv(7)  # 4B di AADD + 3B di copia del file

            if (self.ack_login[:4].decode() == "AADD"):
                self.sid = self.ack_login[0:7]
                print(str(self.sid.decode()),"\n")
            else:
                print("Errore del pacchetto, stringa 'AADD' non trovata")
                exit()

            self.deconnection()

        else:
         print("Controllare l'esistenza del file o il percorso indicato in fase di input")


    def logout(self):
        print("\n--- LOGOUT ---\n")

        self.connection()

        data_logout = "LOGO" + self.sid.decode()

        self.s.send(data_logout.encode('ascii'))

        self.ack_logout = self.s.recv(7)
        print("First 4 byte from dir----> " + str(self.ack_logout[:4].decode()))

        if (self.ack_logout[:4].decode() == "ALGO"):
            print("Numero di file eliminati ---> " + str(self.ack_logout[4:7].decode()))

        self.deconnection()



#def switch_case(peer, case):

#    cases = {"LI": peer.login(), "LO": peer.logout()}

#    cases[str(case)]

#    return 

# --- MAIN ---

if __name__ == "__main__":
    peer = Peer()
    file = input("Nome file da inviare\n")
    peer.aggiunta(file)
    #case = input("LI,LO,ADD\n")
    #switch_case(peer, case)