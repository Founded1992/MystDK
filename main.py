from __future__ import division
from Tkinter import *
from tkSnack import *
from PIL import Image, ImageTk
from threading import Thread
import time
import sys

root = Tk()

def close(evt):
    root.destroy()
    
root.title("Cube Island")
root.bind("<Escape>", close)
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (sw, sh))
root.configure(bg="black")
c = Canvas(root)
c.configure(bg="black", bd=0, width=sw, height=sh, highlightthickness=0)
c.pack()

ThemeLength = 184000
initializeSnack(root)
s = Sound()
s.read('Thief in the Night.mp3')
def playThemeSmooth():
    while True:
        s.play()
        time.sleep(ThemeLength)
t = Thread(target=playThemeSmooth)
#t.start()

'''def playTheme():
    s.play()
    root.after(ThemeLength, playTheme)
playTheme()'''

currScene = None
d = None

class SceneBasic():
    def __init__(self, img, clkZns):
        self.image = img
        self.clickZones = clkZns
    def getImg(self):
        return self.image
    def slideImg(self, targetStr, direction):
        global currScene
        im = Image.open(self.image)
        imw = im.size[0]
        imh = im.size[1]
        scale = 1
        if imw/imh < sw/sh: #If image is taller than screen
            #set scale by height, not width
            scale = sh/imh
        else:
            #set scale by width, not height
            scale = sw/imw
        currScene.imw = int(scale*imw)
        currScene.imh = int(scale*imh)
        currScene.offx = (sw - currScene.imw) / 2
        currScene.offy = (sh - currScene.imh) / 2
        im = im.resize((currScene.imw, currScene.imh), Image.ANTIALIAS)
        self.imp = ImageTk.PhotoImage(im)
        self.currScHndl = c.create_image((sw/2, sh/2), image=self.imp)
        ##SLIDE
        im = Image.open(world[targetStr].getImg())
        imw = im.size[0]
        imh = im.size[1]
        scale = 1
        if imw/imh < sw/sh: #If image is taller than screen
            #set scale by height, not width
            scale = sh/imh
        else:
            #set scale by width, not height
            scale = sw/imw
        imw = int(scale*imw)
        imh = int(scale*imh)
        im = im.resize((imw, imh), Image.ANTIALIAS)
        self.impsl2 = ImageTk.PhotoImage(im)
        sloffx = 0
        sloffy = 0
        incsox = 0
        incsoy = 0
        if direction == 0:
            sloffy = imh
            incsoy = imh / -16
        elif direction == 1:
            sloffx = imw * -1
            incsox = imw / 16
        elif direction == 2:
            sloffy = imh * -1
            incsoy = imh / 16
        else:
            sloffx = imw
            incsox = imw / -16
        self.slScHndl = c.create_image((sw/2 + sloffx, sh/2 + sloffy), image=self.impsl2)
        for i in range(0, 16):
            currSloffx = int(sloffx * ((16-i)/16))
            currSloffy = int(sloffy * ((16-i)/16))
            c.move(self.slScHndl, incsox, incsoy)
            c.move(self.currScHndl, incsox, incsoy)
            c.update()
            #print("cake awesome cake")
            time.sleep(0.01)
    def dispImg(self):
        global currScene
        im = Image.open(self.image)
        imw = im.size[0]
        imh = im.size[1]
        scale = 1
        if imw/imh < sw/sh: #If image is taller than screen
            #set scale by height, not width
            scale = sh/imh
        else:
            #set scale by width, not height
            scale = sw/imw
        currScene.imw = int(scale*imw)
        currScene.imh = int(scale*imh)
        currScene.offx = (sw - currScene.imw) / 2
        currScene.offy = (sh - currScene.imh) / 2
        im = im.resize((currScene.imw, currScene.imh), Image.ANTIALIAS)
        self.imp = ImageTk.PhotoImage(im)
        self.currScHndl = c.create_image((sw/2, sh/2), image=self.imp)
class ObjScene(SceneBasic):
    pass
class ClickZone():
    def __init__(self, x, y, w, h, TRL):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.TRL = TRL
class TRLBasic():
    def __init__(self, targetString):
        self.targetString = targetString
    def action(self):
        global currScene
        currScene = world[self.targetString]
        currScene.dispImg()
class TRLSlide():
    def __init__(self, targetString, direction):
        self.targetString = targetString
        self.direction = direction
    def action(self):
        global currScene
        currScene.slideImg(self.targetString, self.direction)
        currScene = world[self.targetString]
        currScene.dispImg()
        
world = {
    "cube_room":SceneBasic("RenderPictures/Cube_Y_G_Face.png", [ClickZone(0, 0, 0.1, 1, TRLSlide("hallway_code", 1)), ClickZone(0.9, 0, 0.1, 1, TRLSlide("hallway_code", 3))]),
    "hallway_code":SceneBasic("RenderPictures/Hallway_Code.png", [ClickZone(0, 0, 0.1, 1, TRLSlide("cube_room", 1)), ClickZone(0.9, 0, 0.1, 1, TRLSlide("cube_room", 3)), ClickZone(0.3, 0, 0.4, 1, TRLBasic("code_room"))]),
    "code_room":SceneBasic("RenderPictures/Code-Room.png", [ClickZone(0, 0, 0.1, 1, TRLSlide("hallway_cube", 1)), ClickZone(0.9, 0, 0.1, 1, TRLSlide("hallway_cube", 3))]),
    "hallway_cube":SceneBasic("RenderPictures/Hallway_Cube_Y_G_Face.png", [ClickZone(0, 0, 0.1, 1, TRLSlide("code_room", 1)), ClickZone(0.9, 0, 0.1, 1, TRLSlide("code_room", 3)), ClickZone(0.3, 0, 0.4, 1, TRLBasic("cube_room"))]),
}

currScene = world["cube_room"]
currScene.dispImg()

def clickHandle(e):
    scenex = (e.x - currScene.offx) / currScene.imw
    sceney = (e.y - currScene.offy) / currScene.imh
    for i in currScene.clickZones:
        if scenex > i.x and scenex < (i.x + i.w) and sceney > i.y and sceney < (i.y + i.h):
            i.TRL.action()
        
root.bind("<Button 1>", clickHandle)

root.mainloop()
