# 8/01/9:45
import tkinter as tk
from tkinter import messagebox,ttk,filedialog
from tkinter import *
import PIL,os,json
from PIL import Image,ImageTk
import cv2
from map_create import *

choosen_map='route2'

lis=[]
warps=[]
start_pos=[]
saved=False
w=0
h=0
im=None

dir_path = 'assets/tiles/'
tiles_list = []
for file_path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, file_path)):
        if '.png' in file_path:
            tiles_list.append(str(file_path))

for i in range(len(tiles_list)):
    tiles_list[i]=str(tiles_list[i]).replace('.png','')

def hex_to_rgb(hex):

    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    
    return tuple(rgb)


def rm_color(color,image):

    color_=hex_to_rgb(color)
    img = Image.open(image)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []

    for item in datas:
        if item[0] == color_[0] and item[1] == color_[1] and item[2] == color_[2]:
            newData.append((231, 255, 132, 255))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(image)
    
dir_path = 'assets/sounds/musics/'
music_list = []
for file_path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, file_path)):
        music_list.append(str(file_path))

for i in range(len(music_list)):
    music_list[i]=str(music_list[i]).replace('.wav','')

def RBGAImage(path):
    return Image.open(path).convert("RGBA")

def create_label(label,i,j):

    global lis
    def_img = ImageTk.PhotoImage(Image.open('assets/tiles/'+default_tile.get()+'.png').resize((16*int(zoom.get()),16*int(zoom.get())),Image.NEAREST))
    empty=ImageTk.PhotoImage(RBGAImage('assets/tiles/empty.png').resize((16*int(zoom.get()),16*int(zoom.get())),Image.NEAREST))
    label=Label(root, image=empty,borderwidth=0)
    label.im=empty
    label.place(x=92+j*16*int(zoom.get()),y=4+i*16*int(zoom.get()))
    label.bind('<Button-1>',lambda event:pick(i,j))
    lis.append(label)

lis_=[]
def create_tile(tile,i,j,e):

    already=False
    global lis_
    global liste_tiles,im
    img=im
    cop=Image.open('assets/tiles/'+tile+'.png').resize((16*int(zoom.get()),16*int(zoom.get())),Image.NEAREST)
    cop_=cop.copy()
    img.paste(cop_, (j*16*int(zoom.get()), i*16*int(zoom.get())))
    print('oui')
    if e == 'r':
        fill_load()

def mouse(e):
   
   xm= e.x
   ym= e.y
   y.set(int(xm/int(zoom.get())/16))
   x.set(int(ym/int(zoom.get())/16))
   for w in warps:
        if w[1]==int(x.get()) and w[2]==int(y.get()):
            map_w.delete(0,END)
            map_w.insert(0,w[0])
            x_warp.set(w[3])
            y_warp.set(w[4])
            warp_type.set(w[5])
            break
        else:
            map_w.delete(0,END)
            x_warp.set(0)
            y_warp.set(0)
            warp_type.set('Escaliers')

def mouse_p(e):
   
   xm= e.x
   ym= e.y
   y.set(int(xm/int(zoom.get())/16))
   x.set(int(ym/int(zoom.get())/16))
   add_tile()

def mouse_rm(e):
   
   xm= e.x
   ym= e.y
   y.set(int(xm/int(zoom.get())/16))
   x.set(int(ym/int(zoom.get())/16))
   rm_tile()

def fill_load():

    global w,h,im
    print('fill load')
    map=json.load(open('maps/'+choosen_map+'.json'))
    w,h=map["height"],map["width"]
    global liste_tiles
    h,w,default=int(height.get()),int(width.get()),default_tile.get()
    im = Image.new(mode="RGB", size=(w*16*int(zoom.get()), h*16*int(zoom.get())))
    def_img=(Image.open('assets/tiles/'+default+'.png')).resize((16*int(zoom.get()),16*int(zoom.get())),Image.NEAREST)

    for i in range(h):
        for j in range(w):
            im.paste(def_img, (j*16*int(zoom.get()), i*16*int(zoom.get())))
    
    if liste_tiles!=[]:
        for i in liste_tiles:
            img = cv2.imread('assets/tiles/'+str(i[0])+'.png')
            hei,wid,c=img.shape
            cop=(Image.open('assets/tiles/'+str(i[0])+'.png')).resize((wid*int(zoom.get()),hei*int(zoom.get())),Image.NEAREST)
            im.paste(cop, (i[2]*16*int(zoom.get()), i[1]*16*int(zoom.get())))

    print(im)

    img_=ImageTk.PhotoImage(im)
    preview.configure(image=img_)
    preview.im=img_

def add_tile():
    global w,h,liste_tiles,im
    a=0

    for elm in liste_tiles:
        if elm[1]==int(x.get()) and elm[2]==int(y.get()):
            liste_tiles.remove(liste_tiles[a])
        a+=1

    liste_tiles.append([choosen_tile.get(),int(x.get()),int(y.get())])
    
    cop=(Image.open('assets/tiles/'+choosen_tile.get()+'.png')).resize((16*int(zoom.get()),16*int(zoom.get())),Image.NEAREST)
    im_=cv2.imread('assets/tiles/'+choosen_tile.get()+'.png')
    hei,wid,c=im_.shape
    cop=cop.resize((wid*int(zoom.get()),hei*int(zoom.get())),Image.NEAREST)
    im.paste(cop, (int(y.get())*16*int(zoom.get()),int(x.get())*16*int(zoom.get())))

    print('add tile')
    print(im)

    img_=ImageTk.PhotoImage(im)
    preview.configure(image=img_)
    preview.im=img_

def ctrlz():
    try:
        liste_tiles.remove(liste_tiles[-1])
        fill_load()
    except:
        msg=messagebox.showerror(title='erreur',message='aucune action a annuler')

def rm_tile():
    global liste_tiles,im
    a=0
    for elm in liste_tiles:
        if elm[1]==int(x.get()) and elm[2]==int(y.get()):
            liste_tiles.remove(liste_tiles[a])
        a+=1
    img=im.resize((w*16*int(zoom.get()),h*16*int(zoom.get())),Image.NEAREST)
    cop=(Image.open('assets/tiles/'+default.get()+'.png')).resize((16*int(zoom.get()),16*int(zoom.get())),Image.NEAREST)
    img.paste(cop, (int(y.get())*16*int(zoom.get()),int(x.get())*16*int(zoom.get())))
    img=ImageTk.PhotoImage(im)
    preview.configure(image=img)
    preview.im=img

def format_json(data):
    digits = [0,1,2,3,4,5,6,7,8,9]
    for i in digits:
        i = str(i)
        data = data.replace((i+',\n'), (i+','))
        data = data.replace((i+'\n],'), (i+'],\n'))
        data = data.replace((',\n'+i), (','+i))
        data = data.replace(('[\n"'), ('["'))
        data = data.replace(('], \n'), ('['))
        data = data.replace(('\n            '+i), i)
        data = data.replace((i+'\n        '), i)
        data = data.replace(('],\n\n'),('],\n'))
    data = data.replace(',', ', ')
    return data

def save_json():
    global saved
    global start_pos
    start_res=[]
    if start_pos == []:
        start_res=[0,0]
    else:
        start_res=start_pos
    print(start_res)
    fill_load()
    dic={
        "default":default_tile.get(),
        "name":str(name.get()),
        "height":height.get(),
        "width":width.get(),
        "start":start_res,
        "warps":warps,
        "tiles":liste_tiles,
        "music":str(music.get())

    }
    json_map = format_json(json.dumps(dic, indent=0, separators=(',', ':')))
    root.title('outil de map ('+name.get()+')')
    saved=True

    # Writing to sample.json
    with open('maps/'+name.get()+".json", "w") as outfile:
        outfile.write(json_map)

    create_map(name.get())
    

def load_map():
    global liste_tiles
    global start_pos
    global warps
    file_path = filedialog.askopenfilename()
    if file_path!='':
        map=open(file_path)
        file=json.load(map)
        root.title('outil de map ('+str(file['name'])+')')
        default_tile.set(file['default'])
        height.set(file['height'])
        width.set(file['width'])
        music.set(file["music"])
        name.delete(0,END)
        name.insert(0,file['name'])
        liste_tiles=file['tiles']
        try:
            start_pos=file["start"]
        except:
            pass    
        try:
            warps=file["warps"]
        except:
            pass
        fill_load()

def tile_preview():
    im = cv2.imread('assets/tiles/'+choosen_tile.get()+'.png')
    hei,wid,c=im.shape
    img=ImageTk.PhotoImage(Image.open('assets/tiles/'+choosen_tile.get()+'.png').resize((wid*2,hei*2),Image.NEAREST))
    t_pr.configure(image=img)
    t_pr.im=img

def pick(e):
    xm= e.x
    ym= e.y
    y.set(int(xm/int(zoom.get())/16))
    x.set(int(ym/int(zoom.get())/16))
    global liste_tiles
    a=0
    for elm in liste_tiles:
        if elm[1]==int(x.get()) and elm[2]==int(y.get()):
            choosen_tile.set(elm[0])
        a+=1
    tile_preview()

def start_pos_def():
    global start_pos
    start_pos=[int(x.get()),int(y.get())]
    msg=messagebox.showinfo(message=('start pos placée en '+str(x.get())+' '+str(y.get())))

def all_down():
    global start_pos
    global liste_tiles
    try:
        start_pos[0]-=1
    except:
        pass
    for i in liste_tiles:
        i[1]+=1
    fill_load()

def all_up():
    global start_pos
    global liste_tiles
    try:
        start_pos[0]+=1
    except:
        pass
    for i in liste_tiles:
        i[1]-=1
    fill_load()

def all_left():
    global start_pos
    global liste_tiles
    try:
        start_pos[1]-=1
    except:
        pass
    for i in liste_tiles:
        i[2]-=1
    fill_load()

def all_right():
    global start_pos
    global liste_tiles
    try:
        start_pos[1]+=1
    except:
        pass
    for i in liste_tiles:
        i[2]+=1
    fill_load()


root=Tk()
intvalues=[]
for i in range(99):
    intvalues.append(i+1)
tile_values=[]
for i in range(99):
    tile_values.append(i)
liste_tiles=[]
root.bind('<Control-o>', lambda event:load_map())
root.bind('<Control-O>', lambda event:load_map())
root.bind('<Control-Z>', lambda event:ctrlz())
root.bind('<Control-z>', lambda event:ctrlz())
root.bind('<Control-Down>', lambda event:all_down())
root.bind('<Control-Up>', lambda event:all_up())
root.bind('<Control-Left>', lambda event:all_left())
root.bind('<Control-Right>', lambda event:all_right())
root.title('outil map (pas de map)')
root.geometry('480x480')
default_tile=StringVar()
choosen_tile=StringVar()
default=ttk.Combobox(values=tiles_list,width=10,textvariable=default_tile,state='readonly')
default.place(x=2,y=2)
height=ttk.Combobox(values=intvalues,width=3,state='readonly')
height.place(x=2,y=24)
width=ttk.Combobox(values=intvalues,width=3,state='readonly')
width.place(x=2,y=46)
preview=Label()
preview.place(x=100,y=2)
zoom=ttk.Combobox(values=intvalues,width=3,state='readonly')
zoom.place(x=2,y=104)
zoom.set(2)
music=ttk.Combobox(values=music_list,width=10,state='readonly')
music.place(x=2,y=540)
music.set('violet')
height.set(8)
width.set(8)
default_tile.set('empty')
x=ttk.Combobox(values=tile_values,width=3,state='readonly')
y=ttk.Combobox(values=tile_values,width=3,state='readonly')
tile=ttk.Combobox(values=tiles_list,width=10,textvariable=choosen_tile,state='readonly')
tile.place(x=2,y=146)
y.place(x=2,y=170)
x.place(x=2,y=194)
add=Button(command=lambda:add_tile(),text='ajouter')
add.place(x=2,y=218)
rm=Button(command=lambda:rm_tile(),text='retirer')
rm.place(x=2,y=244)
save=Button(text='save',command=lambda:save_json())
save.place(x=2,y=280)

#WARPS
def add_warp():
    for i in range(len(warps)):
        if warps[i][1]==int(x.get()) and warps[i][2]==int(y.get()):
            warps.remove(warps[i])
    warps.append([map_w.get(),int(x.get()),int(y.get()),int(x_warp.get()),int(y_warp.get()),str(warp_type.get())])
    msg=messagebox.showinfo(message=('warp placé en',str(x.get()),str(y.get()),'vers',map_w.get(),'en',str(x_warp.get()),str(y_warp.get()),str(warp_type.get())))

def rm_warp():
    for i in range(len(warps)):
        if warps[i][1]==int(x.get()) and warps[i][2]==int(y.get()):
            warps.remove(warps[i])
            map_w.delete(0,END)
            x_warp.set(0)
            y_warp.set(0)
            warp_type.set('Escaliers')
            break

map_w=Entry(width=8)
map_w.place(x=2,y=390)
x_warp=ttk.Combobox(values=tile_values,width=3,state='readonly')
y_warp=ttk.Combobox(values=tile_values,width=3,state='readonly')
x_warp.place(x=2,y=420)
y_warp.place(x=2,y=450)
w_t=['Escaliers','INDOOR','OUTDOOR','Échelle']
warp_type=ttk.Combobox(values=w_t,width=7,state='readonly')
warp_type.place(x=2,y=480)
warp_type.set('Escaliers')
x_warp.set(0)
y_warp.set(0)

name=Entry(width=15)
name.place(x=2,y=304)
fast=IntVar()
f=ttk.Checkbutton(text='fast',variable=fast,onvalue=1,offvalue=0)
x.set(0)
y.set(0)
tile.set('grass')
tile.bind("<<ComboboxSelected>>", lambda event:tile_preview())
zoom.bind("<<ComboboxSelected>>", lambda event:fill_load())
height.bind("<<ComboboxSelected>>", lambda event:fill_load())
width.bind("<<ComboboxSelected>>", lambda event:fill_load())
default.bind("<<ComboboxSelected>>", lambda event:fill_load())
root.bind('<Return>', lambda event:add_tile())
root.bind('<Delete>', lambda event:rm_tile())
root.bind('<Up>', lambda event:x.set(int(x.get())-1))
root.bind('<Down>', lambda event:x.set(int(x.get())+1))
root.bind('<Left>', lambda event:y.set(int(y.get())-1))
root.bind('<Right>', lambda event:y.set(int(y.get())+1))
root.bind('<Control-P>', lambda event:start_pos_def())
root.bind('<Control-p>', lambda event:start_pos_def())
root.bind('<Control-W>', lambda event:add_warp())
root.bind('<Control-w>', lambda event:add_warp())
root.bind('<Control-Delete>', lambda event:rm_warp())
root.bind('<Control-Delete>', lambda event:rm_warp())
root.bind('<Button-1>',mouse)
root.bind('<Control-Button-1>',mouse_p)
root.bind('<Control-Button-3>',mouse_rm)
root.bind('<Button-3>',pick)
t_pr=Label(borderwidth=0)
t_pr.place(x=2,y=360)
fill_load()
root.mainloop()