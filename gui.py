#!/usr/bin/python

import Tkinter 	as tk
from PIL import Image, ImageTk


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
#       label = tk.Label(self, text="This is page 1")
       
       pathStart="/home/fotobox/gitfiles/assets/Startbild.jpg"
       img = ImageTk.PhotoImage(Image.open(pathStart))
       label = tk.Label(self,image=img)  
       label.image = img
       label.pack(side="top", fill="both", expand=True)
##
##initialize fullscreen main window
##

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)  

          
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
       
       

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        p1 = Page1(self)
        f1 = FullScreenApp(self)
        
        objectframe = tk.Frame(self)
        pageframe   = tk.Frame(self)
        objectframe.pack(side="top", fill="both", expand=False)
        pageframe.pack(side="top", fill="both", expand=False)
        
        p1.place(in_=pageframe, x=0,y=0,relwidth=1,relheight=1)
        f1.place(in_=objectframe,x=0,y=0,relwidth=1,relheight=1)
        
        b1= tk.Button(objectframe, text="BUTTON IS HERE")
        b1.pack(side='left')
        
        p1.show()
    
    


root=tk.Tk()
#app=FullScreenApp(root)
main = MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("800x00")
root.mainloop()


print('loop and sleep over')