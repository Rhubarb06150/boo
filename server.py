import socket,pickle,sys
from random import randint
from threading import Thread

sys.tracebacklimit=0

class Server:

    def client_handler(self):
        while True:
            dt_lst=[]
            for cli in self.client_list:
                try:
                    dt_lst.append(pickle.loads(cli.recv(1024)))
                except:
                    self.client_list.remove(cli)
                    print(f'{cli} est parti')
                    print(f'{len(self.client_list)} joueur(s) connectés')
                    break
            for cli in self.client_list:
                try:
                    cli.send(pickle.dumps(dt_lst))
                except:
                    pass
            for pseudo in dt_lst:
                if str(dt_lst).count(pseudo[3])>=2:
                    print('deux joueurs avec le meme pseudo :o')
                    for j in range(len(self.client_list)):
                        if dt_lst[-j+1][3]:
                            self.client_list[-j+1].send('same name'.encode('utf-8'))
                            self.client_list[-j+1].close()
                            break
        
    def __init__(self):

        self.client_list=[]
        try:
            self.port=int(open('port','r').read())
        except:
            self.port=12500
            print(f"/!\ Le port du fichier port n'a pas pu être lu, le port à donc été mis en 12500 par défault")

        self.server_ip='0.0.0.0'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.server_ip, self.port))
        self.server.listen(5)

        print(f'Serveur ouvert et en écoute sur {self.server_ip}:{self.port}')

        while True:
            conn, addr = self.server.accept()
            try:
                print(f"{(socket.gethostbyaddr(addr[0])[0])} s'est connecté ({(addr[0])})")
            except:
                print(f"{addr} s'est connecté")
            
            self.client_list.append(conn)
            print(f'{len(self.client_list)} joueur(s) connectés')

            t = Thread(target=self.client_handler)
            t.start()
serv=Server()