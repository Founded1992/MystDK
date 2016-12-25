from __future__ import division
from Tkinter import *
from tkSnack import *
from PIL import Image, ImageTk
import time

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
def playTheme():
    s.play()
    root.after(ThemeLength, playTheme)
playTheme()

currScene = None

class SceneBasic():
    def __init__(self, img, clkZns):
        self.image = img
        self.clickZones = clkZns
class ClickZone():
    def __init__(self, x, y, w, h, nextScene):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.nextScene = nextScene
class drawer():
    def BasicSelect(self, targetScene):
        global currScene
        currScene = world[targetScene]
        
        im = Image.open(currScene.image)
        imw = im.size[0]
        imh = im.size[1]
        scale = 1
        currScene.offx = 0
        currScene.offy = 0
        if imw/imh < sw/sh: #If image is taller than screen
            #set scale by height, not width
            scale = sh/imh
            currScene.offx = int( (sw-(scale*imw)) / 2)
        else:
            #set scale by width, not height
            scale = sw/imw
            currScene.offy = int( (sh-(scale*imh)) / 2)
        currScene.imw = int(scale*imw)
        currScene.imh = int(scale*imh)
        im = im.resize((currScene.imw, currScene.imh), Image.ANTIALIAS)
        self.imp = ImageTk.PhotoImage(im)
        c.create_image((sw/2, sh/2), image=self.imp)
        
world = {
    "cube_room":SceneBasic("RenderPictures/Cube_Y_G_Face.png", [ClickZone(0, 0, 0.1, 1, "hallway_code"), ClickZone(0.9, 0, 0.1, 1, "hallway_code")]),
    "hallway_code":SceneBasic("RenderPictures/Hallway_Code.png", [ClickZone(0, 0, 0.1, 1, "cube_room"), ClickZone(0.9, 0, 0.1, 1, "cube_room"), ClickZone(0.3, 0, 0.4, 1, "code_room")]),
    "code_room":SceneBasic("RenderPictures/Code-Room.png", [ClickZone(0, 0, 0.1, 1, "hallway_cube"), ClickZone(0.9, 0, 0.1, 1, "hallway_cube")]),
    "hallway_cube":SceneBasic("RenderPictures/Hallway_Cube_Y_G_Face.png", [ClickZone(0, 0, 0.1, 1, "code_room"), ClickZone(0.9, 0, 0.1, 1, "code_room"), ClickZone(0.3, 0, 0.4, 1, "cube_room")]),
}

d = drawer()
d.BasicSelect("cube_room")

def clickHandle(e):
    scenex = (e.x - currScene.offx) / currScene.imw
    sceney = (e.y - currScene.offy) / currScene.imh
    for i in currScene.clickZones:
        if scenex > i.x and scenex < (i.x + i.w) and sceney > i.y and sceney < (i.y + i.h):
            d.BasicSelect(i.nextScene)
        
root.bind("<Button 1>", clickHandle)

root.mainloop()
