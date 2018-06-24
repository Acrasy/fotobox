import Tkinter  as tk
from PIL import Image, ImageTk
import time

import os
import cups
import logging
import subprocess as sub

#preset = "4zu6"
preset = "streifen"
#preset = "test"

IMG1 = "picture1.jpg"
IMG2 = "picture2.jpg"
IMG3 = "picture3.jpg"


#########################################################################
#               Logic                                                   #
#########################################################################


IMAGE_WIDTH      = 640
IMAGE_HEIGHT     = 480

#print the image
def printPic(fileName):
    conn = cups.Connection()
    printers = conn.getPrinters()
    default_printer = printers.keys()[0]
    cups.setUser('pi')
    conn.printFile (default_printer, fileName, "boothy", {'fit-to-page':'True'})
    logging.info("Print job successfully created.");

#
#Merge Pictures in grid
#    
def scalePictures(fileName):
    xSize, ySize = (1800,1200)
   
    
    if preset == "4zu6":  
        xSnip, ySnip = (int(xSize/2.5),int(ySize/2.5))
        #xSnip, ySnip = (600,400)   
        xOffset, yOffset = (200,134)
        basePhoto = Image.new('RGB',(xSize,ySize),"white")
        
        first = Image.open(IMG1)
        second = Image.open(IMG2)
        third = Image.open(IMG3)
        
        re1 = first.resize((xSnip, ySnip))
        re2 = second.resize((xSnip, ySnip))
        re3 = third.resize((xSnip, ySnip))
        
        basePhoto.paste(re3,(xSize-xSnip,ySize-ySnip))
        basePhoto.paste(re2,(xSize-2*xSnip+xOffset,ySize-2*ySnip+yOffset)) 
        basePhoto.paste(re1,(0,0))
        basePhoto.save(fileName)
        
    elif preset == "streifen":
        xSnip, ySnip = (int(xSize/3),int(ySize/3))   
        xOffset, yOffset = (0,80)
        basePhoto = Image.new('RGB',(xSize,ySize),"white")
        
        first = Image.open(IMG1)
        second = Image.open(IMG2)
        third = Image.open(IMG3)
        
        re1 = first.resize((xSnip, ySnip))
        re2 = second.resize((xSnip, ySnip))
        re3 = third.resize((xSnip, ySnip))
        
        basePhoto.paste(re3,(xSize-xSnip,yOffset))
        basePhoto.paste(re2,(xSize-2*xSnip+xOffset,yOffset)) 
        basePhoto.paste(re1,(0,yOffset))
        
        basePhoto.paste(re3,(xSize-xSnip,ySize/2+yOffset))
        basePhoto.paste(re2,(xSize-2*xSnip+xOffset,ySize/2+yOffset)) 
        basePhoto.paste(re1,(0,ySize/2+yOffset))
        basePhoto.save(fileName)
        
    else:
       print('set preset correctly')



   
def deleteImages(fileName):
    logging.info("Deleting any old images.")
    if os.path.isfile(IMG1):
        os.remove(IMG1)
    if os.path.isfile(IMG2):
        os.remove(IMG2)
    if os.path.isfile(IMG3):
        os.remove(IMG3)
    if os.path.isfile(fileName):
        os.remove(fileName);

def takePicture(picName):
    pictureOptions = "gphoto2 --capture-and-download --filename " + picName + " --force-overwrite"
    p = sub.Popen(pictureOptions,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)

def picRoutine(filename):
    for i in range(3):    
        takePicture("picture"+str(i+1)+".jpg")
    scalePictures(filename)
    printPic(filename)
    deleteImages(filename)
    
#########################################################################
#               GUI                                                     #
#########################################################################

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
            label = tk.Label(self,image=img)
            label.image=img
            label.pack(side="left", fill="both", expand=True)


class Page2(Page):
     def __init__(self, *args, **kwargs):
          Page.__init__(self, *args, **kwargs)
          pathStart = "./assets/count_1.jpg"
          img = ImageTk.PhotoImage(Image.open(pathStart))
          label = tk.Label(self,image=img) 
          label.image = img
          label.pack(side="left", fill="both", expand=True)
          
        
          
          def Page2callback(self):
              for i in range(4,-1,-1):
                  time.sleep(1)
                  img2 = ImageTk.PhotoImage(Image.open("./assets/count_"+str(i)+".jpg"))
                  label.configure(image=img2)
                  label.image = img2
                  
          Page2callback(self)

                  
        


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

        b1 = tk.Button(buttonframe, text="Next", command=self.buttonCallback)
          
        b1.pack(side="left")

        p1.show()
        self.pages.append(p1)
        self.pages.append(p2)
        self.pages.append(p3)
        self.pages.append(p2)
        self.pages.append(p3)
        self.pages.append(p2)
        self.pages.append(p3)
        self.pages.append(p4)

        
        #f1.master.place(in_=objectframe,x=200,y=0,relwidth=1,relheight=1)
        #b1.pack(side='left')
        #p1.show()
    def buttonCallback(self):
        print "Lifting a frame"
        self.pages[self.index].lift()
        self.index = (self.index+1) % len(self.pages)


  

              

if __name__== "__main__":        


    root=tk.Toplevel()
    #Damit sparst dir die FullscreenApp Klasse
    root.attributes('-fullscreen',True)
    #app=FullScreenApp(root)
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    main.bind()
    #root.wm_geometry("800x800")
    
    root.mainloop()
    

