from Tkinter import Tk
from tkSnack import *
import time

root = Tk()

def close(evt):
    root.destroy()

root.title("Cube Island")
root.bind("<Escape>", close)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(bg="black")

ThemeLength = 184000
initializeSnack(root)
s = Sound()
s.read('Thief in the Night.mp3')
def playTheme():
    print "loop"
    s.play()
    root.after(ThemeLength, playTheme)
playTheme()

root.mainloop()
