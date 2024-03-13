from pygame import *
from random import randint
from bots import pseudos
import pygame
import socket
import pickle
import re
import sys
import time
import command_boo
import bots
import os
import shutil
import json

direction=['L','R']
states_list=['chasing','running','hiding','mock_1','mock_2']

class Game:

    def __init__(self):
        pygame.init()
        try:
            self.pseudo=(open('assets/.pseudo','r').read())
        except:
            self.pseudo=f'User-{randint(0,999)}'
            
        self.player_list=[]
        self.pseudo_view=False
        self.serv_list=[]
        # self.gb_horror=image.load('assets/gb.png')
        self.screen=display.set_mode((640,576), vsync=1)
        # self.screen.blit(self.gb_horror,(0,0))
        # self.screen.set_clip(112,119,420,361)
        self.screen.set_clip(0,0,640,576)
        self.running=True
        self.clock=pygame.time.Clock()
        display.set_icon(image.load('assets/boo/classic/chasing.png'))

        self.message_delay=None
        self.message=''
        self.msg_esc=False
        self.cmd=False
        self.map_sur=image.load(f'map/level.png')
        self.map_collision=json.loads(open('map/level.json').read())["hitboxes"]
        self.collision_vars=[]
        for i in range(len(self.map_collision)):
            self.collision_vars.append('')
        self.start_pos=json.loads(open('map/level.json').read())["start"]

        self.map_sur=image.load(f'map/level.png')
        self.map_sur=transform.scale(self.map_sur,(self.map_sur.get_size()[0]*3,self.map_sur.get_size()[1]*3))


        self.bg_sur1=image.load(f'map/bg/bg1.png')

        self.bg_sur1=transform.scale(self.bg_sur1,(self.bg_sur1.get_size()[0]*3,self.bg_sur1.get_size()[1]*3))

        self.velocity=10 #DEFAUT 10
        self.velocity_fv=self.velocity
        self.max_speed=60 #DEFAUT 60
        self.max_speed_fv=self.max_speed
        self.real_max_speed=100 #DEFAUT 100
        self.brake=1 #DEFAUT 1
        self.font_pseudo = pygame.font.Font("assets/font/font.ttf", 25)
               
        self.state='chasing'
        self.color='classic'

        self.players_nb=0
        self.bot_list=[]

        self.index=0
        self.connected=False

        self.player_speed_r,self.player_speed_l,self.player_speed_u,self.player_speed_d=0,0,0,0
        self.moving_d,self.moving_u,self.moving_r,self.moving_l=False,False,False,False

        self.default_sprite=transform.scale(image.load('assets/boo/classic/chasing.png'),(46,42))
        self.other_default_sprite=transform.scale(image.load('assets/boo/classic/chasing.png'),(46,42))
        self.direction='R'
        self.other_direction='R'

        self.wall_bounce=0.5 #DEFAUT 0.8

        self.demo=False
        self.player_pos=[0,0]
        self.player_pos[0],self.player_pos[1]=self.start_pos[0]*48,self.start_pos[1]*48

        self.other_player_pos=[0,0]
        self.other_player_state='chasing'

        pygame.key.set_repeat(1,10)

        display.set_caption(f'{self.pseudo} - Boogie the game')

    #FONCTIONS POUR LES BOTS ___________________________________________________________________________________________________

    def SpawnBot(self,pse,precision,frequency):
        if not self.connected:
            if len(self.bot_list)!=len(bots.pseudos):
                while True:
                    pse=bots.pseudos[randint(0,len(bots.pseudos)-1)]
                    already_took=False
                    for bot in self.bot_list:
                        if bot.pseudo==pse:
                            already_took=True
                    if not already_took:
                        bot=bots.Bot(self,pse,randint(1,8),randint(1,8))
                        self.bot_list.append(bot)
                        self.Message('Bot apparu')
                        break
            else:
                self.Message('Le nombre maximal de bots a été atteint')
        else:
            self.Message('Impossible de faire apparaître un bot en ligne')
        

    def ShowBots(self):
        if not self.connected:
            for bot in self.bot_list:
                bot.ShowBot(self)
                bot.Move(self,self.player_pos[0]-bot.player_pos[0],self.player_pos[1]-bot.player_pos[1])


    #FONCTIONS D'AFFICHAGE DES TRUCS IMPORTANT ___________________________________________________________________________________________________

    def ShowBG(self):
        self.screen.blit(self.bg_sur1,(-abs(self.player_pos[0])/2,-abs(self.player_pos[1])/2))

    def ShowLevel(self):
        self.screen.blit(self.map_sur,(-abs(self.player_pos[0])+256,-abs(self.player_pos[1])+256))

    def ShowPlayer(self):

        boo=pygame.transform.scale2x(image.load(f'assets/boo/{self.color}.png'))
        self.default_sprite=pygame.Surface((46,42))
        for i in range(len(states_list)):
            if self.state==states_list[i]:
                break
        self.default_sprite.blit(boo, (0,0),(i*46,0,i*46+46,42))

        # self.default_sprite=transform.scale(image.load(f'assets/boo/{self.color}/{self.state}.png'),(46,42))
        if self.direction!='L':
            self.player=transform.flip(self.default_sprite,True,False)
        else:
            self.player=self.default_sprite
        self.screen.blit(self.player,(256,256))
    
    def ShowOtherPlayers(self):
        self.player_list=[]
        for i in range(self.players_nb):
            print(self.other_players_infos)
            if self.other_players_infos[i]!=self.other_players_infos[-1]:
                self.other_default_sprite=transform.scale(image.load(f'assets/boo/{self.other_players_infos[i][1]}.png'),(46,42))
                if self.other_players_infos[i][2]!='L':
                    self.other_player=transform.flip(self.other_default_sprite,True,False)
                else:
                    self.other_player=self.other_default_sprite
                if self.other_players_infos[i][3] !=self.pseudo:
                    self.screen.blit(self.other_player,(int(self.other_players_infos[i][0][0]-self.player_pos[0]+256),int(self.other_players_infos[i][0][1]-self.player_pos[1]+256)))
        for i in range(self.players_nb):
            if self.other_players_infos[i]!=self.other_players_infos[-1]:
                self.player_list.append(self.other_players_infos[i][3])

    #FONCTION POUR L'INTERFACE ET LE GUI C LA MEME CHOSE JE SAIS ___________________________________________________________________________________________________

    def CheckMessage(self,message):

        if not self.msg_esc:

            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        self.msg_esc=True
                    if event.unicode=='!':
                        self.msg_esc=True

            if self.message_delay!=None:
                self.font = pygame.font.Font("assets/font/font.ttf", 36)
                self.text = self.font.render(f"> {message}", True, (0, 255, 0))
                wtext,htext=self.text.get_size()
                if time.time()-self.message_delay<=2:
                    self.screen.blit(self.text,(0,(self.screen.get_size())[1]-htext))

    def Message(self,message):
        self.msg_esc=False
        self.message_delay=time.time()
        self.message=message

    def ShowPseudos(self):
        if self.connected:
            for e in self.other_players_infos:
                if e!=self.other_players_infos[-1]:
                    if e[3]!=self.pseudo:
                        self.text = self.font_pseudo.render(f"{e[3]}", True, (255, 255, 255))
                        self.screen.blit(self.text,(e[0][0]-self.player_pos[0]-(self.text.get_size()[0]-46)/2+256,e[0][1]-self.player_pos[1]+230))

                    else:
                        self.text = self.font_pseudo.render(self.pseudo, True, (255, 255, 255))
                        self.screen.blit(self.text,(256-(self.text.get_size()[0]-46)/2,230))
        else:
            for bot in self.bot_list:
                self.text = self.font_pseudo.render(bot.pseudo, True, (255, 255, 255))
                self.screen.blit(self.text,(bot.player_pos[0]-self.player_pos[0]-(self.text.get_size()[0]-46)/2+256,bot.player_pos[1]-self.player_pos[1]+230))

            self.text = self.font_pseudo.render(self.pseudo, True, (255, 255, 255))
            self.screen.blit(self.text,(256-(self.text.get_size()[0]-46)/2,230))

    #FONCTIONS POUR LA CONNEXION ET POUR GÉRER LA PARTIE EN LIGNE ___________________________________________________________________________________________________

    def CheckIp(self,ip_address):

        if not re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", "127.0.0.1", ip_address):
            return False

        bytes = ip_address.split(".")

        for ip_byte in bytes:
            if int(ip_byte) < 0 or int(ip_byte) > 255:
                return False
        return True

    def JoinGame(self,ip):

        port=''

        if ':' in ip:
            st=False
            for e in ip:
                if not st:
                    if e==':':
                        st=True
                if st:
                    port+=e
            for i in range(len(ip)):
                if ip[-i+1] !=':':
                    ip=ip[:-1]
                if ip[-i+1]==':':
                    ip=ip[:-1]
                    break
        
        port=port.replace(':','')
        ip=ip.replace(':','')
        self.host=Connexion(ip,port)
        try:
            self.host.client.send(''.encode('utf-8'))
            self.connected=True

            #  RECEPTION MAP ___
            # file=open('srvtemp/server-map.png','wb')
            # image_chunk=self.host.client.recv(2048)
            # self.host.client.settimeout(0.10)
            # try:
            #     for i in image_chunk:
            #         file.write(image_chunk)
            #         image_chunk=self.host.client.recv(2048)
            # except:
            #     pass
            # file.close()
            # self.map_sur=pygame.image.load('srvtemp/server-map.png')
            # self.map_sur=transform.scale(self.map_sur,(self.map_sur.get_size()[0]*3,self.map_sur.get_size()[1]*3))
            #  ________________


            self.Message('Connecté au serveur')
            
        except Exception as e:
            print(e)
            try:
                self.host.client.close()
            except:
                pass
            self.connected=False
            self.Message('Connexion impossible')

    def ServerCommunication(self):

        try:
            
            self.host.client.send(pickle.dumps([[int(self.player_pos[0]),int(self.player_pos[1])],(self.color+'/'+self.state),self.direction,self.pseudo]))
            self.other_players_infos=pickle.loads(self.host.client.recv(1024))
            self.players_nb=len(self.other_players_infos)-1

            if self.players_nb!=1:
                display.set_caption(f'{self.pseudo} - Connecté à {self.host.server_ip} ({self.players_nb} joueurs)')
            else:
                display.set_caption(f'{self.pseudo} - Connecté à {self.host.server_ip} (1 joueur)')

            if self.other_players_infos=='same name':
                self.connected=False
                self.host.client.close()
                self.Message('Un joueur du même nom est déjà connecté')
                return

        except socket.error as e:
            self.connected=False
            self.host.client.close()
            self.Message('La connexion avec le serveur a été intérompue')
        except Exception as e:
            pass

    def Kick(self,player):
        
        if self.connected:
            if self.pseudo in self.other_players_infos[-1]:
                if player in self.player_list:
                    self.host.client.send(pickle.dumps([[int(self.player_pos[0]),int(self.player_pos[1])],(self.color+'/'+self.state),self.direction,self.pseudo,f'kick {player}']))
                    self.Message(f'{player} a été expulsé')
                    return
                else:
                    self.Message(f"Le joueur '{player}' n'a pas été trouvé")
                    return
            else:
                self.Message(f"Vous n'êtes pas opérateur")
                return
        else:
            self.Message(f"Cette commande fonctionne uniquement en ligne")
        
    def PyServ(self,code):

        if self.connected:
            if self.pseudo in self.other_players_infos[-1]:
                    self.host.client.send(pickle.dumps([[int(self.player_pos[0]),int(self.player_pos[1])],(self.color+'/'+self.state),self.direction,self.pseudo,f'pyserv {code}']))
                    self.Message('Code envoyé au serveur')

                    return
            else:
                self.Message(f"Vous n'êtes pas opérateur")
                return
        else:
            self.Message(f"Cette commande fonctionne uniquement en ligne")
        
    #FONCTIONS PHYSIQUES ___________________________________________________________________________________________________
            
    def CheckMapCollision(self):
        index=0
        for hitbox in self.map_collision:

            self.collision_vars[index]

            if self.player_pos[0]+46<hitbox[0]*48:
                self.collision_vars[index]=('L')
            if self.player_pos[0]>hitbox[0]*48+hitbox[2]*48:
                self.collision_vars[index]=('R')

            if self.player_pos[1]+42<hitbox[1]*48:
                self.collision_vars[index]=('U')
            if self.player_pos[1]>hitbox[1]*48+hitbox[3]*48:
                self.collision_vars[index]=('D')

            if self.collision_vars[index]=='L' and int(self.player_pos[0])+46>=hitbox[0]*48:
                self.player_speed_l=self.player_speed_r*self.wall_bounce
                self.player_speed_r=0
                self.player_pos[0]=hitbox[0]*48-46
            
            if self.collision_vars[index]=='R' and int(self.player_pos[0])<hitbox[0]*48+hitbox[2]*48:
                self.player_speed_r=self.player_speed_l*self.wall_bounce
                self.player_speed_l=0
                self.player_pos[0]=hitbox[0]*48+hitbox[2]*48

            if self.collision_vars[index]=='U' and int(self.player_pos[1])+42>=hitbox[1]*48:
                self.player_speed_u=self.player_speed_d*self.wall_bounce
                self.player_speed_d=0
                self.player_pos[1]=hitbox[1]*48-42
            if self.collision_vars[index]=='D' and int(self.player_pos[1])<hitbox[1]*48+hitbox[3]*48:
                self.player_speed_d=self.player_speed_u*self.wall_bounce
                self.player_speed_u=0
                self.player_pos[1]=hitbox[1]*48+hitbox[3]*48

            index+=1

    def CheckCollision(self):
        
        w,h=self.map_sur.get_size()

        if self.player_pos[0]+46>=w:
            self.player_speed_l=self.player_speed_r*self.wall_bounce
            self.player_speed_r=0
            self.player_pos[0]=w-46

        if self.player_pos[0]<=0:
            self.player_speed_r=self.player_speed_l*self.wall_bounce
            self.player_speed_l=0
            self.player_pos[0]=0
            
        if self.player_pos[1]+42>=h:
            self.player_speed_u=self.player_speed_d*self.wall_bounce
            self.player_speed_d=0
            self.player_pos[1]=h-42

        if self.player_pos[1]<=0:
            self.player_speed_d=self.player_speed_u*self.wall_bounce
            self.player_speed_u=0
            self.player_pos[1]=0 

        if self.player_speed_d<0:
            self.player_speed_d=0
        if self.player_speed_u<0:
            self.player_speed_u=0
        if self.player_speed_l<0:
            self.player_speed_l=0
        if self.player_speed_r<0:
            self.player_speed_r=0

        if self.player_speed_d>self.real_max_speed:
            self.player_speed_d=self.real_max_speed
        if self.player_speed_u>self.real_max_speed:
            self.player_speed_u=self.real_max_speed
        if self.player_speed_r>self.real_max_speed:
            self.player_speed_r=self.real_max_speed
        if self.player_speed_l>self.real_max_speed:
            self.player_speed_l=self.real_max_speed

    def PlayerInertia(self):
        if not self.moving_r:
            if self.player_speed_r!=0:
                self.player_speed_r-=self.brake
        if not self.moving_l:
            if self.player_speed_l!=0:
                self.player_speed_l-=self.brake
        if not self.moving_d:
            if self.player_speed_d!=0:
                self.player_speed_d-=self.brake
        if not self.moving_u:
            if self.player_speed_u!=0:
                self.player_speed_u-=self.brake

        self.player_pos[1]-=self.player_speed_u/self.velocity/self.brake
        self.player_pos[1]+=self.player_speed_d/self.velocity/self.brake
        self.player_pos[0]-=self.player_speed_l/self.velocity/self.brake
        self.player_pos[0]+=self.player_speed_r/self.velocity/self.brake

    def MainLoop(self):
        
        self.clock.tick(60)
        
        self.index+=1

        if self.demo:
            if self.index!=0:
                ch=randint(0,3)
                if ch==0:
                    self.player_speed_d=randint(30,60)
                elif ch==1:
                    self.player_speed_u=randint(30,60)
                elif ch==2:
                    self.player_speed_l=randint(30,60)
                elif ch==3:
                    self.player_speed_r=randint(30,60)
            if self.index%10==0:
                self.direction=direction[randint(0,1)]

        for event in pygame.event.get():

            if event.type==KEYUP:
                if event.key==K_d:
                    self.demo = not self.demo

                if event.key==K_p:
                    self.pseudo_view = not self.pseudo_view

                if event.key==K_b:
                    self.SpawnBot(pseudos[randint(0,len(pseudos)-1)],randint(0,8),randint(0,8))

            if event.type==QUIT:
                self.running=False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                
            if event.type==KEYDOWN:
                if event.unicode=='!' and not self.cmd:
                    command_boo.OpenCMD(self)

        self.cmd=False
        keys=pygame.key.get_pressed()

        self.CheckCollision()
        self.CheckMapCollision()


        if keys[K_LSHIFT]:
            self.state='hiding'
            self.max_speed=0
            self.velocity=self.velocity_fv

        elif keys[K_SPACE]:

            self.state='running'
            self.max_speed=self.real_max_speed
            self.velocity=8

        else:
            self.state='chasing'
            self.max_speed=self.max_speed_fv
            self.velocity=self.velocity_fv

        if self.state!='hiding':

            if keys[K_RIGHT]:
                self.direction='R'
                self.moving_r=True
                if self.player_speed_r<self.max_speed:
                    self.player_speed_r+=self.brake
                else:
                    self.player_speed_r-=self.brake
            else:
                self.moving_r=False

            if keys[K_LEFT]:
                self.direction='L'
                self.moving_l=True
                if self.player_speed_l<self.max_speed:
                    self.player_speed_l+=self.brake
                else:
                    self.player_speed_l-=self.brake
            else:
                self.moving_l=False
            if keys[K_UP]:
                self.moving_u=True
                if self.player_speed_u<self.max_speed:
                    self.player_speed_u+=self.brake
                else:
                    self.player_speed_u-=self.brake
            else:
                self.moving_u=False
            if keys[K_DOWN]:
                self.moving_d=True
                if self.player_speed_d<self.max_speed:
                    self.player_speed_d+=self.brake
                else:
                    self.player_speed_d-=self.brake
            else:
                self.moving_d=False

        if self.state=='hiding':
            self.moving_u,self.moving_d,self.moving_r,self.moving_l=False,False,False,False

        
        if self.state=='hiding':
            if keys[K_f]:
                self.state='mock_2'

        try:
            if self.connected:
                self.ServerCommunication()
        except Exception as err:
            if self.connected:
                self.host.client.close()
            display.set_caption(f'{self.pseudo} - Boogie the game')
            self.Message('Connexion avec le serveur perdue/intérompue')
            self.connected,self.hosting=False,False

        self.screen.fill((0,0,0))
        self.PlayerInertia()
        self.ShowBG()
        self.ShowLevel()
        self.ShowBots()

        if self.connected:
            self.ShowOtherPlayers()
            
        self.ShowPlayer() 
        if self.pseudo_view:
            self.ShowPseudos()

        self.CheckMessage(self.message)

        if not self.connected:
            display.set_caption(f'{self.pseudo} - Boogie the game')

        display.update()

class Connexion:

    def __init__(self,ip,port):
        if not os.path.exists('srvtemp/'):
            os.mkdir('srvtemp/')
        self.port=12500
        if port !='':
            self.port=int(port)
        self.server_ip=ip
        pygame.display.set_caption(f'{game.pseudo} - Tentative de connexion à {self.server_ip}:{self.port}...')
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        self.client.connect_ex((ip, self.port))

game=Game()
while game.running:
    game.MainLoop()

if os.path.isdir("srvtemp/"):
    shutil.rmtree('srvtemp/')
else:
    print('pas de dossier')