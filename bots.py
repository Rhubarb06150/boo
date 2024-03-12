from pygame import *
from random import randint
import pygame
import json

direction=['L','R']
pseudos=['Captain Falcon','Fox','Falco','Ness','Pikachu','Mewtwo','Juloxus','Matheal','Rhubarb','Benoît','Donkey Kong','Diddy Kong','Luigi','Mario','Ryu','Ho-Oh']
list_color=['classic','gold','ash']

class Bot:

    def __init__(self,player,pseudo,precision,frequency):

        self.velocity=10 #DEFAUT 10
        self.velocity_fv=self.velocity
        self.max_speed=60 #DEFAUT 60
        self.max_speed_fv=self.max_speed
        self.real_max_speed=100 #DEFAUT 100
        self.brake=1 #DEFAUT 1
        self.font_pseudo = pygame.font.Font("assets/font/font.ttf", 25)
        self.precision=precision
        self.frequency=frequency

        self.map_collision=json.loads(open('map/level.json').read())["hitboxes"]
        self.collision_vars=[]
        for i in range(len(self.map_collision)):
            self.collision_vars.append('')
               
        self.state='chasing'
        if randint(0,1)==1:
            self.pattern='chasing'
        else:
            self.pattern='running_away'
        self.running=False
        self.color=list_color[randint(0,len(list_color)-1)]
        self.pseudo=pseudo

        self.player_speed_r,self.player_speed_l,self.player_speed_u,self.player_speed_d=0,0,0,0
        self.moving_d,self.moving_u,self.moving_r,self.moving_l=False,False,False,False

        self.default_sprite=transform.scale(image.load(f'assets/boo/{player.color}/{player.state}.png'),(46,42))
        self.direction=player.direction

        self.wall_bounce=0.8 #DEFAUT 0.8

        self.player_pos=[player.player_pos[0],player.player_pos[1]]
    
    def ShowBot(self,player):

        self.default_sprite=transform.scale(image.load(f'assets/boo/{self.color}/{self.state}.png'),(46,42))
        if self.direction!='L':
            self.player=transform.flip(self.default_sprite,True,False)
        else:
            self.player=self.default_sprite
        player.screen.blit(self.player,(int(256-player.player_pos[0]+self.player_pos[0]),int(256-player.player_pos[1]+self.player_pos[1])))

    def CheckCollision(self,player):
        
        w,h=player.map_sur.get_size()

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

    def CheckMapCollision(self):
        index=0
        for hitbox in self.map_collision:

            self.collision_vars[index]

            if self.player_pos[0]+38<hitbox[0]*48:
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
                self.player_pos[0]=hitbox[0]*48+hitbox[2]*48+0.05

            if self.collision_vars[index]=='U' and int(self.player_pos[1])+42>=hitbox[1]*48:
                self.player_speed_u=self.player_speed_d*self.wall_bounce
                self.player_speed_d=0
                self.player_pos[1]=hitbox[1]*48-42
            if self.collision_vars[index]=='D' and int(self.player_pos[1])<hitbox[1]*48+hitbox[3]*48:
                self.player_speed_d=self.player_speed_u*self.wall_bounce
                self.player_speed_u=0
                self.player_pos[1]=hitbox[1]*48+hitbox[3]*48+0.05

            index+=1

    def Move(self,player,x,y):

        self.CheckCollision(player)
        self.CheckMapCollision()

        #POUR UNE SORTE DE COMPORTEMENT ALÉATOIRE

        if self.state=='running':
            self.max_speed=self.real_max_speed
            self.velocity=8
        else:
            self.max_speed=self.max_speed_fv
            self.velocity=self.velocity_fv

        if self.pattern=='chasing':

            if randint(1,10)<=self.frequency:

                if x>self.precision:
                    self.direction='R'
                    self.moving_r=True
                    if self.player_speed_r<self.max_speed:
                        self.player_speed_r+=self.brake
                    else:
                        self.player_speed_r-=self.brake
                else:
                    self.moving_r=False

                if x<-abs(self.precision):
                    self.direction='L'
                    self.moving_l=True
                    if self.player_speed_l<self.max_speed:
                        self.player_speed_l+=self.brake
                    else:
                        self.player_speed_l-=self.brake
                else:
                    self.moving_l=False

                if y<-abs(self.precision):
                    self.moving_u=True
                    if self.player_speed_u<self.max_speed:
                        self.player_speed_u+=self.brake
                    else:
                        self.player_speed_u-=self.brake
                else:
                    self.moving_u=False

                if y>self.precision:
                    self.moving_d=True
                    if self.player_speed_d<self.max_speed:
                        self.player_speed_d+=self.brake
                    else:
                        self.player_speed_d-=self.brake
                else:
                    self.moving_d=False

            if randint(1,240)==1:
                self.running = not self.running

            if self.running:
                self.state='running'
            else:
                self.state='chasing'

        elif self.pattern=='running_away':

            if randint(1,5)<3:

                if x<10 or self.player_pos[0]<200:
                    self.direction='R'
                    self.moving_r=True
                    if self.player_speed_r<self.max_speed:
                        self.player_speed_r+=self.brake
                    else:
                        self.player_speed_r-=self.brake
                else:
                    self.moving_r=False

                if x>-10 or player.map_sur.get_size()[0]-self.player_pos[0]<200:
                    self.direction='L'
                    self.moving_l=True
                    if self.player_speed_l<self.max_speed:
                        self.player_speed_l+=self.brake
                    else:
                        self.player_speed_l-=self.brake
                else:
                    self.moving_l=False

                if y>-10 or player.map_sur.get_size()[1]-self.player_pos[1]<200:
                    self.moving_u=True
                    if self.player_speed_u<self.max_speed:
                        self.player_speed_u+=self.brake
                    else:
                        self.player_speed_u-=self.brake
                else:
                    self.moving_u=False

                if y<10 or self.player_pos[1]<200:
                    self.moving_d=True
                    if self.player_speed_d<self.max_speed:
                        self.player_speed_d+=self.brake
                    else:
                        self.player_speed_d-=self.brake
                else:
                    self.moving_d=False

            if randint(1,240)==1:
                self.running = not self.running

            if self.running:
                self.state='running'
            else:
                self.state='chasing'


        self.PlayerInertia()