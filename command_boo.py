import pygame,re,sys,string
from pygame import *
from random import randint

list_char=['0','1','2','3','4','5','6','7','8','9','.',':','-','_',' ','=','(',')','[',']','{','}',"'",'"',',','*','/',';','\\','@']
for e in string.ascii_lowercase:
    list_char.append(e)
for e in string.ascii_uppercase:
    list_char.append(e)

list_commands_offline=['pse','color','py','bot','kill']
list_commands_online=['tpto','stop']
list_color=['classic','gold','ash']

def CheckLetters(text):
    letters=False
    for e in text:
        if e in string.ascii_letters:
            letters=True
    return letters

def CheckInts(text):
    ints=False
    for e in text:
        if e in ['0','1','2','3','4','5','6','7','8','9']:
            ints=True
    return ints

def OpenCMD(self):
    self.cmd=True
    a=0
    index=0
    pygame.event.clear()
    cur_text=''
    self.font = pygame.font.Font("assets/font/font.ttf", 36)
    self.cur = self.font.render("|", True, (0, 255, 0))
    stop=False
    esc=False
    comm_error=True
    while True:
        self.clock.tick(60)
        text_tp=cur_text
        for event in pygame.event.get():

            if event.type==QUIT:
                self.running=False
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN:

                if event.unicode in list_char:
                    if event.unicode=='!' and cur_text=='':
                        pass
                    else:
                        if index==len(cur_text):
                            cur_text+=event.unicode
                        else:
                            cur_text=cur_text[:index] + event.unicode + cur_text[index:]
                        index+=1

                if event.key == pygame.K_BACKSPACE and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    if len(cur_text)>0:
                        while cur_text[index-1]!=' ' and cur_text[index-1]!='.' and cur_text[index-1]!=':' and index!=0:
                            cur_text = cur_text[:index-1] + cur_text[index:]
                            index-=1
                            if index==0:
                                break

                if event.key==K_BACKSPACE:
                    if index!=0:
                        if index==len(cur_text):
                            cur_text=cur_text[:-1]
                        else:
                            cur_text = cur_text[:index-1] + cur_text[index:]
                        index-=1

                if event.key==K_RETURN or event.key==K_KP_ENTER:
                    stop=True
                    if cur_text!='':
                        self.serv_list.append(cur_text)

                if event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    if index>0:
                        index-=1
                    if len(cur_text)>0:
                        while cur_text[index]!=' ' and cur_text[index]!='.' and cur_text[index]!=':' and index!=0:
                            if index==1:
                                index-=1
                                break
                            index-=1

                elif event.key==K_LEFT:
                    if index>0:
                        index-=1

                if event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    if index<len(cur_text):
                        index+=1
                    if len(cur_text)>0:
                        if index!=len(cur_text):
                            while cur_text[index]!=' ' and cur_text[index]!='.' and cur_text[index]!=':' and index!=0:
                                if index==len(cur_text)-1:
                                    index+=1
                                    break
                                index+=1
                        
                elif event.key==K_RIGHT:
                    if index<len(cur_text):
                        index+=1
                
                if index<0:
                    index=0
                if event.key==K_UP:
                    if self.serv_list!=[]:

                        a+=1
                        if a>len(self.serv_list):
                            a-=1
                        cur_text=self.serv_list[-a]
                        index=len(cur_text)

                if event.key==K_TAB:

                    if not self.connected:
                        for command in list_commands_offline:
                            if re.match(rf'^{cur_text}',command):
                                cur_text=command
                                index=len(cur_text)
                                break

                        if re.match(r'^kill .',cur_text):
                            for bot in self.bot_list:
                                if re.match(rf"^{cur_text.replace('kill ','')}",bot.pseudo):
                                    cur_text=f'kill {bot.pseudo}'
                                    index=len(cur_text)
                                    break

                        if re.match(r'^color .',cur_text):
                            for color in list_color:
                                if re.match(rf"^{cur_text.replace('color ','')}",color):
                                    cur_text=f'color {color}'
                                    index=len(cur_text)
                                    break

                        

                    if self.connected:
                        for command in list_commands_online:
                            if re.match(rf'^{cur_text}',command):
                                cur_text=command
                                index=len(cur_text)
                                break

                        if re.match(r'^tpto .',cur_text):
                            for player in self.other_players_infos:
                                if re.match(rf"^{cur_text.replace('tpto ','')}",player[3]):
                                    cur_text=f'tpto {player[3]}'
                                    index=len(cur_text)
                                    break

                if event.key==K_DOWN:
                    a-=1
                    if a<0:
                        a=0
                    if a == 0:
                        cur_text=''
                    if a!=0:
                        cur_text=self.serv_list[-a]
                        index=len(cur_text)

                if event.key==K_ESCAPE:
                    esc=True
                    stop=True
                    break

        self.screen.fill((0,0,0))
        self.ShowMap()
        self.PlayerInertia()
        self.CheckCollision() 
        self.ShowBots()

        if self.connected:
            self.ServerCommunication()
            self.ShowOtherPlayers()
        if self.pseudo_view:
            self.ShowPseudos()
        self.ShowPlayer()
        try:
            pygame.draw.rect(self.screen,(0,0,0),(0,self.screen.get_size()[1]-self.text.get_size()[1],self.screen.get_size()[0],self.text.get_size()[1]))
        except:
            pass
        if index-len(cur_text)!=0:
            txt_cur=text_tp[:index-len(cur_text)]
        else:
            txt_cur=cur_text
        self.text_for_cur = self.font.render(f"> {txt_cur}", True, (0, 255, 0))
        self.text = self.font.render(f"> {text_tp}", True, (0, 255, 0))
        wtext,htext=self.text.get_size()
        self.screen.blit(self.text,(0,(self.screen.get_size())[1]-htext))

        if pygame.time.get_ticks()%800<=400:
            self.screen.blit(self.cur,(self.text_for_cur.get_size()[0]-4,(self.screen.get_size())[1]-htext))

        display.update()
        if stop:
            self.cmd=False
            break
        if '!' not in list_char:
            list_char.append('!')
        pygame.key.set_repeat(450,45)
        
    self.cmd=True

    if not esc:

        if not self.connected:

            #commandes pour connexion vers serveur avec la verif de l'ip

            if cur_text=='':
                display.update()
            elif re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", cur_text):
                text_tp=f'Tentative de connexion vers {text_tp}...'
                self.screen.fill((0,0,0))
                self.screen.blit(self.player,(self.player_pos[0],self.player_pos[1]))
                self.text = self.font.render(f"> {text_tp}", True, (0, 255, 0))
                wtext,htext=self.text.get_size()
                self.screen.blit(self.text,(0,(self.screen.get_size())[1]-htext))
                display.update()
                comm_error=False
                self.JoinGame(cur_text)

            #commandes plus longues que 2 donc les commandes pour le localhost et les autres

            elif len(cur_text)>2:
                if cur_text[0]=='0' and cur_text[1]==':':
                    cur_text=cur_text.replace('0:','')
                    text_tp=f'Tentative de connexion vers localhost:{cur_text}...'
                    self.screen.fill((0,0,0))
                    self.screen.blit(self.player,(self.player_pos[0],self.player_pos[1]))
                    self.text = self.font.render(f"> {text_tp}", True, (0, 255, 0))
                    wtext,htext=self.text.get_size()
                    self.screen.blit(self.text,(0,(self.screen.get_size())[1]-htext))
                    display.update()
                    comm_error=False
                    self.JoinGame(f"localhost:{cur_text}")
                if cur_text=='pse' or cur_text=='pse ':
                    comm_error=False
                    self.Message(f'Veuillez indiquer votre pseudo exemple: pse Fox')
                if re.match(r'^pse ',cur_text):
                    pse_chang=True
                    bak=self.pseudo
                    self.pseudo=''
                    for i in range(len(cur_text)):
                        if i > 3:
                            if cur_text[i]!=' ':
                                self.pseudo+=cur_text[i]
                            
                            if cur_text[i]==' ':
                                self.pseudo=bak
                                self.Message("Votre pseudo ne peut pas contenir d'espaces")
                                pse_chang=False
                                comm_error=False
                                break
                    if not CheckLetters(cur_text.replace('pse ','')):
                        self.pseudo=bak
                        self.Message("Votre pseudo doit contenir des lettres")
                        pse_chang=False
                        comm_error=False
                    if pse_chang:
                        comm_error=False
                        pse_fil=open('assets/.pseudo','w+').write(self.pseudo)
                        display.set_caption(f'{self.pseudo} - Boogie the game')
                        self.Message(f'pseudo changé en {self.pseudo}')
                if re.match(r'^mv',cur_text):
                    if re.match(r'^mv [0-9]{1,3}.$',cur_text):
                        mov_factor=cur_text.replace('mv ','').replace('u','').replace('d','').replace('l','').replace('r','').replace(' ','')
                        if not CheckLetters(cur_text.replace('mv ','')) and not CheckInts(cur_text.replace('mv ','')):                      
                            if cur_text[-1]=='u':
                                direction='le haut'
                                self.player_pos[1]-=int(mov_factor)
                            if cur_text[-1]=='d':
                                direction='le bas'
                                self.player_pos[1]+=int(mov_factor)
                            if cur_text[-1]=='r':
                                direction='la droite'
                                self.player_pos[0]+=int(mov_factor)
                            if cur_text[-1]=='l':
                                direction='la gauche'
                                self.player_pos[0]-=int(mov_factor)
                            comm_error=False
                            self.Message(f'Déplacé vers {direction} de {mov_factor}')
                
                if re.match(r'^py .',cur_text):
                    comm_error=False
                    try:
                        exec(cur_text[3:])
                        self.Message('Code éxécuté sans erreur')
                    except Exception as e:
                        self.Message(f'Erreur: {e}')

                if re.match(r'^color',cur_text):
                    if re.match(r'^color$',cur_text) or re.match(r'^color $',cur_text):
                        comm_error=False
                        self.Message('Veuillez indiquer la couleur')
                    if re.match(r'^color .',cur_text):
                        comm_error=False
                        if cur_text.replace('color ','') in list_color:
                            self.color=cur_text.replace('color ','')
                            col=cur_text.replace('color ','')
                            self.Message(f'Couleur changée en {col}')
                        else:
                            self.Message('La couleur est inconnue, liste dans le README')

                if re.match(r'^kill',cur_text):
                    if re.match(r'^kill$',cur_text) or re.match(r'^kill $',cur_text):
                        comm_error=False
                        self.Message('Veuillez indiquer le bot a tuer')
                    if re.match(r'^kill .',cur_text):
                        comm_error=False
                        btk=cur_text.replace('kill ','')
                        if len(self.bot_list)>0:
                            if btk!='all' and btk!='@r':
                                found=False
                                for bot in self.bot_list:
                                    if bot.pseudo==btk:
                                        self.bot_list.remove(bot)
                                        found=True
                                        break
                                if found:
                                    self.Message(f'Le bot {btk} a bien été tué')
                                else:
                                    self.Message(f"Aucun bot au nom de {btk} n'a été trouvé")
                            elif btk=='all':
                                self.bot_list=[]
                                self.Message('Tout les bots ont été tués')
                            elif btk=='@r':
                                kill=self.bot_list[randint(0,len(self.bot_list)-1)]
                                self.bot_list.remove(kill)
                                self.Message(f'Le sort est tombé sur {kill.pseudo}')
                            else:
                                self.Message("L'argument donné n'a pas pu être exploité")
                        else:
                            self.Message("Il n'y a aucun bot a tuer ici")


                
                if cur_text=='bot':
                    self.SpawnBot()
                    comm_error=False

            elif cur_text=='0':
                text_tp=f'Tentative de connexion vers localhost:12500...'
                self.screen.fill((0,0,0))
                self.screen.blit(self.player,(self.player_pos[0],self.player_pos[1]))
                self.text = self.font.render(f"> {text_tp}", True, (0, 255, 0))
                wtext,htext=self.text.get_size()
                self.screen.blit(self.text,(0,(self.screen.get_size())[1]-htext))
                display.update()
                comm_error=False
                self.JoinGame(f"localhost:12500")
        else:

            if cur_text=='stop':
                self.host.client.close()
                self.Message('Serveur quitté')
                display.set_caption(f'{self.pseudo} - Boogie the game')
                comm_error=False
                self.connected=False

            if cur_text=='tpto' or cur_text=='tpto ':
                comm_error=False
                self.Message(f'Veuillez indiquer un joueur sur lequel se téléporter')
            if re.match(r'^tpto .',cur_text):
                found=False
                for player in self.other_players_infos:
                    if player[3] == cur_text.replace('tpto ',''):
                        self.player_pos=player[0]
                        self.direction=player[2]
                        comm_error=False
                        found=True
                        self.Message(f'Téléporté sur {player[3]}')
                if not found:
                    comm_error=False
                    pse_totp=cur_text.replace('tpto ','')
                    self.Message(f'Joueur "{pse_totp}" non trouvé')
            if re.match(r'^py .',cur_text):
                comm_error=False
                try:
                    exec(cur_text[3:])
                    self.Message('Code éxécuté sans erreur')
                except Exception as e:
                    self.Message(f'Erreur: {e}')

        if comm_error:
            self.Message('Commande invalide')

    pygame.event.clear()