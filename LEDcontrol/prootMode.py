#!/usr/bin/env python
import time
import sys
import math
from rgbmatrix import RGBMatrix
from PIL import Image, ImageFilter

import LEDmode

class prootMode(LEDmode):

    def __init__(self, matrix):
        self.matrix = matrix


    # Takes an RGBA image and returns the viewbox of the non-transparent part of the image
    def getImageCenter(img: Image):
        minX = -1
        maxX = 0
        minY = -1
        maxY = 0
        for x in range(0, img.width):
            for y in range(0, img.height):
                if img.getpixel((x, y))[3] != 0:
                    if minX == -1:
                        minX = x
                    maxX = max(maxX, x)
                    if minY == -1:
                        minY = y
                    else: 
                        minY = min(minY, y)
                    maxY = max(maxY, y)
        return (minX, minY, maxX, maxY)


    def rotatoLarge(img, regionBox, angle, y, x):
        # Crop the region from the original image
        list = []
        for i in regionBox:
            list.append(i)

        list[3] = list[3]+50

        regionBox = list

        croppedRegion = img.crop(regionBox)
        
        # Rotate the cropped region
        rotatedRegion = croppedRegion.rotate(angle, resample=Image.BICUBIC)
        
        # Create a new blank image with the same size as the original image
        blankImage = Image.new('RGBA', img.size, (0, 0, 0, 0))
        
        # Calculate the new position, allowing for fractional movement
        newPosition = (regionBox[0] + int(y), regionBox[1] + int(x))
        
        # Paste rotated region with antialiasing
        blankImage.paste(rotatedRegion, newPosition, rotatedRegion.filter(ImageFilter.SMOOTH))
        
        return blankImage


    def rotato(img, regionBox, angle, y, x): 

        croppedRegion = img.crop(regionBox)
        croppedRegion.thumbnail(croppedRegion.size, Image.Resampling.LANCZOS)
        rotatedRegion = croppedRegion.rotate(angle, resample=Image.BICUBIC)
        newPostion = (regionBox[0] + int(y), regionBox[1] + int(x))

        blankImage = Image.new('RGBA', img.size)
        blankImage.getpixel((0, 0))
        blankImage.paste(rotatedRegion, newPostion, rotatedRegion)


        return blankImage


    def sigma(x):
        return abs(x)==x


    def steepSin(x):
        x = prootMode.sigma(math.sin(x))*math.sqrt(abs(math.sin(x)))
        return x
    

    def setImg(self, parts):
        # Background
        composite_image = Image.new("RGBA", (self.matrix.width, self.matrix.height))
        for part in parts:
            part[0].thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
            img = prootMode.rotato(part[0], part[1], part[2], part[3], part[4])
            composite_image.alpha_composite(img)

        self.matrix.SetImage(composite_image.convert('RGB'))


    def startup(self):
        self.rightEye = Image.open("/home/pi/LEDcontrol/media/prootImg/rightEye.png")
        self.leftEye = Image.open("/home/pi/LEDcontrol/media/prootImg/leftEye.png")
        self.rightSmile = Image.open("/home/pi/LEDcontrol/media/prootImg/rightSmile.png")
        self.leftSmile = Image.open("/home/pi/LEDcontrol/media/prootImg/leftSmile.png")
        self.nose = Image.open("/home/pi/LEDcontrol/media/prootImg/nose.png")
        self.faceSmall = Image.open("/home/pi/LEDcontrol/media/prootImg/faceSmall.png")
        self.faceNormal = Image.open("/home/pi/LEDcontrol/media/prootImg/faceNormal.png")
        self.googleLeft = Image.open("/home/pi/LEDcontrol/media/prootImg/googleLeft.png")
        self.googleRight = Image.open("/home/pi/LEDcontrol/media/prootImg/googleRight.png")
        self.blinklyLeft = Image.open("/home/pi/LEDcontrol/media/prootImg/blinklyLeft.png")
        self.blinklyRight = Image.open("/home/pi/LEDcontrol/media/prootImg/blinklyRight.png")
        
        self.angle = 0
        self.angleWarp = 0
        self.directionFlip = False
        self.x = 0
        self.y = 0
    
        self.rightEyeBox = prootMode.getImageCenter(self.rightEye)
        self.leftEyeBox = prootMode.getImageCenter(self.leftEye)
        self.googleLeftBox = prootMode.getImageCenter(self.googleLeft)
        self.googleRightBox = prootMode.getImageCenter(self.googleRight)
        self.noseBox = prootMode.getImageCenter(self.nose)
        self.rightSmileBox = prootMode.getImageCenter(self.rightSmile)
        self.leftSmileBox = prootMode.getImageCenter(self.leftSmile)


    def periodic(self):
        self.angleWarp += .01 if self.directionFlip else -.01
        if self.angleWarp >= 2:
            self.directionFlip = True
        if self.angleWarp <= 0:
            self.directionFlip = False
        self.angle += .5
        self.x += 0
        self.y += 0
        
        self.setImg([ 
                #[googleLeft, googleLeftBox, angleWarp*20, math.sin(x)*2, steepSin(y)*2], 
                #[googleRight, googleRightBox, -angleWarp*20, math.sin(x)*2, steepSin(y)*2], 
                [self.leftEye, self.leftEyeBox, -self.angleWarp*2, math.sin(self.x)*2, prootMode.steepSin(self.y)*2], 
                [self.rightEye, self.rightEyeBox, self.angleWarp*2, math.sin(self.x)*2, prootMode.steepSin(self.y)*2], 
                [self.nose, self.noseBox, 0, 0, 0], 
                [self.rightSmile, self.rightSmileBox, self.angleWarp, 0, 0], 
                [self.leftSmile, self.leftSmileBox, -self.angleWarp, 0,0]
            ])
    

    def onEnd(self):
        self.rightEye.close() 
        self.leftEye.close() 
        self.rightSmile.close()
        self.leftSmile.close()
        self.nose.close()
        self.faceSmall.close()
        self.faceNormal.close() 
        self.googleLeft.close()
        self.googleRight.close() 
        self.blinklyLeft.close() 
        self.blinklyRight.close()
    