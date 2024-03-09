import PIL,json,cv2
from PIL import Image
import os.path
# calculate file size in KB, MB, GB
def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
def create_map(map):
    nm=map
    map=open('maps/'+map+'.json')
    map=json.load(map)
    h,w,default,name,tiles=int(map['height']),int(map['width']),map['default'],map['name'],map['tiles']
    def_img = Image.open('assets/tiles/'+default+'.png')
    im = PIL.Image.new(mode="RGB", size=(w*16, h*16))
    for i in range(w):
        for j in range(h):
            def_cop = def_img.copy()
            im.paste(def_cop, (i*16, j*16))
    for i in range(len(tiles)):
        wt,ht,ti=tiles[i][1],tiles[i][2],tiles[i][0]
        ti_img = Image.open('assets/tiles/'+ti+'.png')
        ti_cop = ti_img.copy()
        im.paste(ti_cop, (ht*16, wt*16))
    im.save('maps/'+name+'.png')
    img=cv2.imread('maps/'+name+'.png')
    h,w,c=img.shape
    im=Image.open('maps/'+name+'.png').save('maps/'+name+'.png')
    f_size = os.path.getsize('maps/'+name+'.png')
    img_size = convert_bytes(f_size)
    print('rendu fait')