from PIL import Image

class ImageUtils:

    """
        Converts a RGBA image to RGB by blending partially transparent pixels with a black
        background (as opposed to displaying partially transparent pixels as opaque).
    """
    def blendToRGB(img: Image.Image, background_color: tuple = (0, 0, 0)) -> Image.Image:
        # Create a background image with the same size
        background = Image.new('RGB', img.size, background_color)

        # Composite RGBA image over black background
        return Image.alpha_composite(background.convert('RGBA'), img.convert("RGBA")).convert('RGB')
