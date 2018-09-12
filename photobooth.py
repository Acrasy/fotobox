#!bin/env python3

###############################################################################
#               imports                                                       #
###############################################################################

from PIL import Image, ImageTk
from time import sleep
from sys import exit

import os
import cups
import subprocess as sub
import picamera as picam


###############################################################################
#               global defines                                                #
###############################################################################

#preset = "4zu6"
preset = "streifen"


IMG1 = "picture1.jpg"
IMG2 = "picture2.jpg"
IMG3 = "picture3.jpg"

IMAGE_WIDTH      = 640
IMAGE_HEIGHT     = 480

SCREEN_DELAY     = 3
COUNTDOWN        = 3

SCREEN_W         = 1280
SCREEN_H         = 800

TOTAL_PICS       = 3

#cameraResolution = (1800,1200)                  # resolution DSLR
cameraResolution = (1920,1152)                  #set resolution PiCam

# =============================================================================
#                 setup camera
# =============================================================================

CAM = picamera.PiCamera()
CAM.annotate_text_size   = 80
CAM.resolution           =cameraResolution


###############################################################################
#               helper functions                                              #
###############################################################################
#
#       parked
#
# =============================================================================
# take picture (dslr)
# =============================================================================

# =============================================================================
# def takePicture(picName):
#     pictureOptions = "gphoto2 --capture-and-download --filename " + picName + " --force-overwrite"
#     p = sub.Popen(pictureOptions,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
# =============================================================================


# =============================================================================
#       testroutine without gui
# =============================================================================

# =============================================================================
# def picRoutine(filename):
#     for i in range(3):
#         takePicture("picture"+str(i+1)+".jpg")
#     scalePictures(filename)
#     printPic(filename)
#     deleteImages(filename)
# =============================================================================


# =============================================================================
# print the image
# =============================================================================
def printPic(fileName):
    conn = cups.Connection()
    printers = conn.getPrinters()
    default_printer = printers.keys()[0]
    cups.setUser('pi')
    conn.printFile (default_printer, fileName, "boothy", {'fit-to-page':'True'})


# =============================================================================
# Merge Pictures in grid
# =============================================================================

def scalePictures(fileName):
    xSize, ySize = cameraResolution                   #resolution Picam

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


# =============================================================================
# delete pictures (after print)
# =============================================================================

def deleteImages(fileName):
    if os.path.isfile(IMG1):
        os.remove(IMG1)
    if os.path.isfile(IMG2):
        os.remove(IMG2)
    if os.path.isfile(IMG3):
        os.remove(IMG3)
    if os.path.isfile(fileName):
        os.remove(fileName);


# =============================================================================
# prep pictures
# =============================================================================

def overlayImage(imagePath, duration = 0, layer = 3, mode = 'RGB'):
    """
    Add an overlay (and sleep for optional duration).
    If sleep duration ios not supplied then overlay will need to be removed later.
    This functions returns an overlay ID, which can be used to removeOverlay(id)
    """

    img = Image.open(imagePath)

    if( img.size[0]> SCREEN_W):
        basewidth = SCREEN_W
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize),Image.ANTIALIAS)

    # "
    #   The camera`s block size is 32x16 so any image data
    #   provided to a renderer must have a width which is a
    #   multiple of 32, and a height which is a multiple of
    #   16.
    # "
    # Refer:
    # http://picamera.readthedocs.io/en/release-1.10/recipes1.html#overlaying-images-on-the-preview

    pad = Image.new(mode, (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))

    # Paste the original image into the padded one
    pad.paste(img, (0, 0))

    #Get the padded image data
    try:
        padded_img_data = pad.tobytes()
    except AttributeError:
        padded_img_data = pad.tostring() # Note: tostring() is deprecated in PIL v3.x

    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    o_id = CAM.add_overlay(padded_img_data, size=img.size)
    o_id.layer = layer

    if duration > 0:
        sleep(duration)
        CAM.remove_overlay(o_id)
        o_id = -1 # '-1' indicates there is no overlay

    return o_id # if we have an overlay (o_id > 0), we will need to remove it later

# =============================================================================
# above function courtesy of jibbius
# =============================================================================


def printOverlay(stringToPrint):
    CAM.annotate_text = stringToPrint

def getReady(photoNumber):
    overlayImage('/assets/2.jpg', 2, 'RGBA')


def prepImage(photoNumber):
    overlayImage('/assets/'+photoNumber+'.jpg', SCREEN_DELAY, 3, 'RGBA')


def takingPhoto(photoNumber, filename):
    for counter in range(COUNTDOWN,0,-1):                   #Countdown and print countdown on screen
        printOverlay("             ..." + str(counter))
        sleep(1)

    CAM.annotate_text=""
    CAM.capture(filename)
    return filename


def removeOverlay(id):
    if id != -1:
        CAM.removeOverlay(id)


def thanksScreen(filenamePrefix):
    thanksImage = '/assets/8.jpg'
    overlayImage(thanksImage,2)

    #Playback
    prevOverlay = False
    for photoNumber in range(1, TOTAL_PICS+1):
        filename = filenamePrefix + '_' + str(photoNumber) + 'of ' + str(TOTAL_PICS)+'.jpg'
        thisOverlay = overlayImage(filename, False, (3 + TOTAL_PICS))
        # The idea here, is only remove the previous overlay after a new overlay is added.
        if prevOverlay:
            removeOverlay(prevOverlay)
        sleep(2)
        prevOverlay = thisOverlay

    removeOverlay(prevOverlay)

    finishedImage = '/assets/all_done_delayed_upload.png'
    overlayImage(finishedImage, 5)

###############################################################################
#               main function + actual main                                   #
###############################################################################

def main():
    #start cam preview
    CAM.startPreview(resolution = (SCREEN_W, SCREEN_H))

    filename = "bild"

    #Display intro screen
    greetingImage1 = 'assets/1.jpg'
    greetingImage2 = 'assets/2.jpg'
    overlay1 = overlayImage(greetingImage1, 0, 3)
    overlay2 = overlayImage(greetingImage2, 0, 4)


    #funktion zum connecten mit bluetooth und empfangen der message


    while True:
        starting = None
        #funktion zum auslesen der bluetooth message und schreibt wert in variable
        if starting == 'starting':
           removeOverlay(overlay2)
           sleep(3)
           removeOverlay(overlay1)

           for photoNumber in range(1, TOTAL_PICS+1):
               prepImage(photoNumber)
               takingPhoto(photoNumber, filename)
               

           thanksScreen(filename)
           sleep(10) #delay for printer

           overlay1 = overlayImage(greetingImage1, 0, 3)
           overlay2 = overlayImage(greetingImage2, 0, 4)


if __name__== "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("na daun ned")

    finally:
        CAM.stop_preview()
        CAM.close()
        exit()

