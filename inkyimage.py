from PIL import Image, ImageFont, ImageDraw

WHITE = 0
BLACK = 1
RED = 2
YELLOW = 2

WIDTH = 212
HEIGHT = 104

_image = Image.new('P', (WIDTH, HEIGHT))

_draw = ImageDraw.Draw(_image)


def create_mask(source, mask=(WHITE, BLACK, RED)):
    """Create a transparency mask.

    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.

    :param mask: Optional list of Inky pHAT colours to allow.

    """

    # Create a new 1bpp (on/off) mask image
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            # Mask out just the inkyphat colours we want to show
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image

def set_image(image, colswap=None):
    """Replace buffer with an image.

    The colswap argument can be either a dictionary of source (keys) and target (values),
    or a simple list where the target colour (0 = White, 1 = Black, 2 = Red) is the index.

    A colswap of [0, 1, 2], for example, will have no effect on a properly prepared image.
    A colswap of [1, 0, 2] would swap Black and White.
    This is equivalent to {0:1, 1:0, 2:2}

    :param image: A valid PIL image, or an image filename
    :param colswap: (optional) determine how colours should be swapped/mapped

    """

    if isinstance(image, str):
        image = Image.open(image)

    if hasattr(image, 'getpixel'):

        if isinstance(colswap,list):
            w, h = image.size
            for x in range(w):
                for y in range(h):
                    p = image.getpixel((x, y))
                    try:
                        p = colswap.index(p)
                        image.putpixel((x, y), p)
                    except ValueError:
                        continue

        if isinstance(colswap,dict):
            w, h = image.size
            for x in range(w):
                for y in range(h):
                    p = image.getpixel((x, y))
                    if p in colswap.keys():
                        p = colswap[p]
                        image.putpixel((x, y), p)

        _image.paste(image)
        return _image

def get_image():
    """Get the image buffer."""

    _image.save("test.bmp")
    return _image
