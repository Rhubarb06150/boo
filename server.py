import socket,pickle,sys
from random import randint
from threading import Thread

sys.tracebacklimit=0

class Server:
        
    def __init__(self):
        try:
            self.ops=open('assets/.ops','r').read()
            self.ops=list(self.ops.split(" "))
        except:
            pass
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

    def client_handler(self):

        while True:

            dt_lst=[]

            #ICI C LE FORMATTAGE ET LE PAQUETAGE RECU DE TOUT LES CLIENTS

            for cli in self.client_list:
                try:
                    dt_lst.append(pickle.loads(cli.recv(1024)))
                except Exception as e:

                    #SI ON ARRIVE PAS A ENVOYER AU JOUEUR, DONC IL EST PARTI, ON LE VIRE DE LA LISTE ET ON ANNONCE SON DÉPART

                    self.client_list.remove(cli)
                    print(f'{cli} est parti')
                    print(f'{len(self.client_list)} joueur(s) connectés')
                    break

            #LISTE DES JOUEURS

            list_pseudo=[]
            for player in dt_lst:
                list_pseudo.append(player[3])

            #ÉVENTUALITÉ DE KICK

            for dt in dt_lst:
                ind=0
                if 'kick' in dt[-1]:
                    for player in dt_lst:
                        index=0
                        if player[3]==dt[-1].replace('kick ',''):
                            self.client_list[index].close()
                            print(dt[-1].replace('kick ','')+' exclu')
                            break
                        index+=1
                ind+=1

            #VERIFICATION DES OPS

            try:
                dt_lst.append(self.ops)
            except:
                pass

            #ENVOI DES DONNÉES A TOUT LES CLIENTS   

            for cli in self.client_list:
                try:
                    cli.send(pickle.dumps(dt_lst))
                except:
                    pass
            

            #POUR VIRER DES JOUEURS AYANT LE MEME PSEUDO, CA VIRE QUE CELUI QUI ESSAYE DE SE CONNECTER ET NON CELUI QUI EST DÉJA CONNECTÉ

            for pseudo in list_pseudo:
                if list_pseudo.count(pseudo)>=2:
                    print('deux joueurs avec le meme pseudo :o')
                    for j in range(len(self.client_list)):
                        if dt_lst[-j+1][3]==pseudo:
                            self.client_list[-j+1].send('same name'.encode('utf-8'))
                            self.client_list[-j+1].close()
                            break

serv=Server()