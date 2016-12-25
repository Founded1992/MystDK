from Tkinter import Tk
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
root.mainloop()
