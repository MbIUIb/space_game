from pygame.image import load
from pygame.transform import scale
from pygame import image


def load_image(filename, with_alpha=True):
    path = 'assets/images/' + filename
    image = load(path)

    if with_alpha:
        return image.convert_alpha()
    else:
        return image.convert()

def unscale_image(image, n):
    return scale(image, (image.get_width() // n, image.get_height() // n)).convert_alpha()
