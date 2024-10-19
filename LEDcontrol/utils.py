from PIL import Image

class ImageUtils:


    def blendToRGB(img: Image.Image, background_color: tuple = (0, 0, 0)) -> Image.Image:
        """
        Converts a RGBA image to RGB by blending partially transparent pixels with a black
        background (as opposed to displaying partially transparent pixels as opaque).
        """

        # Create a background image with the same size
        background = Image.new('RGB', img.size, background_color)

        # Composite RGBA image over black background
        return Image.alpha_composite(background.convert('RGBA'), img.convert("RGBA")).convert('RGB')
    

    def limitCurrent(img: Image.Image, numberOfPanels: int) -> Image.Image:
        """
        Attempts to reduce the amount of current used by the panels by estimating the 
        current needed to display an image and dimming the entire image if necessary.
        The image passed in should be an RGB image with no transparency.
        """
        
        def getImageBrightness(img):
            brightnessLevel = 0
        
            # Sum the brightness of every pixel
            for x in range(0, img.width):
                for y in range(0, img.height):
                    brightnessLevel += img.getpixel((x, y))[0] + img.getpixel((x, y))[1] + img.getpixel((x, y))[2]
            
            return brightnessLevel

        # The amperage of one panel at full brightness
        FOUR_AMPS = 255 * 3 * 32 * 64
        # One amp ~= 391,680

        ONE_REDUCTION = 3 * 32 * 64

        newImage = img.copy()
        
        # Repeat the dimming process until the screens are dim enough
        while (brightness := getImageBrightness(newImage) * numberOfPanels) > FOUR_AMPS / 2.1:

            print("Reducing brightness: " + str(brightness))

            reductionAmmount = (brightness - int(FOUR_AMPS / 2.1)) // (ONE_REDUCTION * numberOfPanels)

            if reductionAmmount == 0:
                reductionAmmount = 1

            for x in range(0, newImage.width):
                for y in range(0, newImage.height):
                    newColor = [0, 0, 0]
                    currentColor = newImage.getpixel((x, y))
                    
                    for i in range(0, 3):
                        if currentColor[i] - reductionAmmount >= 0:
                            newColor[i] = currentColor[i] - reductionAmmount
                        else:
                            newColor[i] = 0
                    
                    newImage.putpixel((x, y), tuple(newColor))
            
        return newImage
        

# Testing code  
# img = Image.open("C:\\Users\\noahn\\Documents\\GitHub\\LED-FRC-Matrix\\LEDcontrol\\media\\png\\image.png")

# img = ImageUtils.limitCurrent(img, 2)

# img.show()
# img.close()
