#!/usr/bin/python

import Tkinter as tk
from PIL import Image, ImageTk
import time




class Page(tk.Frame):
        def __init__(self, *args, **kwargs):
                tk.Frame.__init__(self, *args, **kwargs)
        #Bissi hacky aber gut fuer Debug
        def lift(self):
            print "Lifted a frame"
            tk.Frame.lift(self)
        def show(self):
                self.lift()

class Page1(Page):
     def __init__(self, *args, **kwargs):
            Page.__init__(self, *args, **kwargs)
                               
            pathStart="./assets/Startbild.jpg"          
            img = ImageTk.PhotoImage(Image.open(pathStart))
            label = tk.Label(self,image=img,takefocus="True")
            label.image=img
            label.pack(side="left", fill="both", expand=True)
            

             

class Page2(Page):
     def __init__(self, *args, **kwargs):
          Page.__init__(self, *args, **kwargs)
          
          pathStart = "./assets/count_0.jpg"
          img = ImageTk.PhotoImage(Image.open(pathStart))
          label = tk.Label(self,image=img) 
          label.image = img
          label.pack(side="left", fill="both", expand=True)
          
          def Page2callback(self):
        
              for i in range(4):
                  time.sleep(1)
                  img2 = ImageTk.PhotoImage(Image.open("./assets/count_"+str(i+1)+".jpg"))
                  self.label.configure(image=img2)
                  self.label.image = img2          
          
          self.bind("<Button-1>",Page2callback)


class Page3(Page):
     def __init__(self, *args, **kwargs):
            Page.__init__(self, *args, **kwargs)
            pathStart="./assets/cheese.jpg"
            img = ImageTk.PhotoImage(Image.open(pathStart))
            label = tk.Label(self,image=img) 
            label.image = img
            label.pack(side="left", fill="both", expand=True)
  
  
class Page4(Page):
     def __init__(self, *args, **kwargs):
            Page.__init__(self, *args, **kwargs)
            pathStart="./assets/all_done.jpg"
            img = ImageTk.PhotoImage(Image.open(pathStart))
            label = tk.Label(self,image=img) 
            label.image = img
            label.pack(side="left", fill="both", expand=True)   
   
   
class MainView(tk.Frame):
    index = 1
    pages = []
   
    
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)    
        self.geometry = args[0].geometry  
        
        
       
        
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=lambda: self.buttonCallback())
          
        b1.pack(side="left")

        p1.show()
        self.pages.append(p1)
        self.pages.append(p2)
        self.pages.append(p3)
        self.pages.append(p2)
        self.pages.append(p3)
        self.pages.append(p4)
        
      # self.after(1,lambda:self.focus_force())
      # self.bind("<Button-1>", self.buttonCallback)

        
        #f1.master.place(in_=objectframe,x=200,y=0,relwidth=1,relheight=1)
        #b1.pack(side='left')
        #p1.show()
    def buttonCallback(self):
        
        print "Lifting a frame"
        self.pages[self.index].lift()
        self.index = (self.index+1) % len(self.pages)

"""        
        while (self.index-1) !=1 :              
            for i in range(4):
              time.sleep(1)
              img2 = ImageTk.PhotoImage(Image.open("./assets/count_"+str(i+1)+".jpg"))
              self.label.configure(image=img2)
              self.label.image = img2
"""              
    
        


  

              

if __name__== "__main__":        


    root=tk.Toplevel(takefocus="True")
    root.attributes('-fullscreen',True)
  
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    main.bind("<Button-1>", lambda: main.buttonCallback())
    #root.wm_geometry("800x800")
    
    main.focus
    

    
    root.mainloop()
    
    
    print('loop and sleep over')