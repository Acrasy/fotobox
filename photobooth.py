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


if __name__== "__main__":        


