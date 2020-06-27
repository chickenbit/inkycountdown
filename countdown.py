from datetime import date
from datetime import datetime
import csv
import event
from math import floor
import logging
from PIL import Image, ImageFont, ImageDraw
MODE = "RGBA" # ValueError: cannot reshape array of size 88192 into shape (104,212)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
_logger.addHandler(ch)


def get_font(font_size=19, font_path=None):
    """Just using the one from inkyphat site...
    want more options: https://pythonbytes.fm/episodes/show/154/code-frozen-in-carbon-on-display-for-all
    https://www.kutilek.de/sudo-font/

    :param font_size:
    :return:
    """
    if font_path is None:
      from font_fredoka_one import FredokaOne
      font = ImageFont.truetype(FredokaOne, font_size)
    else:
      font = ImageFont.truetype(font_path, font_size)
#    font = ImageFont.truetype("FiraCode-Light.ttf", font_size)
#    font = ImageFont.truetype(r'/home/pi/Source/sudo-font/sudo/Sudo-Thin.ttf', font_size)
#    font = ImageFont.truetype(r'/home/pi/Source/sudo-font/sudo/Sudo-Medium.ttf', font_size)
# FreeMonoBold kinda works
#    font = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', font_size)
#    font = ImageFont.truetype(r'/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf', font_size)
#    font = ImageFont.truetype("Sudo-Thin.ttf", font_size)
#    font = ImageFont.truetype("Sudo-Regular.ttf", font_size)
#    font = ImageFont.truetype("Sudo-Medium.ttf", font_size)
    return font


def get_events(font, max_height, max_width, event_file):
    """

    :param font:
    :param max_height:
    :param event_file:
    :return:
    """
    events = []
    with open(event_file, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            dt = datetime.strptime(row[1], r'%m/%d/%Y')
            d = date(dt.year, dt.month, dt.day)
            events.append(event.Event(row[0], d))

    sorted_events = sorted(events, key=lambda e: e.days_til_event())
    # Get Max events to list
    max_events = 0
    events_height = 0
    spacing = 3
    for row in sorted_events:
        w, h = font.getsize(row.name)
#        print("h {}".format(h))
        new_height = events_height + h + spacing
        if new_height > max_height:
            break
        else:
            events_height = new_height
            max_events = max_events + 1
#    print("max_events {}".format(max_events))
    return sorted_events[0:max_events]


def draw_logo(font, height, width):
    """

    :param font:
    :param height:
    :param width:
    :return:
    """
    img = Image.new(MODE, (width, height), 1)
    draw = ImageDraw.Draw(img)
    text = "[Graphic]"
    text_w, text_h = font.getsize(text)
    x = (width / 2) - (text_w / 2)
    y = (height / 2)

    draw.text((x, y), text, fill=222, font=font)
#    img.save(r'countdown_right.bmp')
    return img


def draw_events(events, font, height, width):
    """

    :param events:
    :param font:
    :param height:
    :param width:
    :return:
    """
    img = Image.new(MODE, (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    x_current = 0
    y_current = 0
    padding = 1
    RED = 2
    WHITE = 0
    max_name = 0
    max_days_til = 0
    max_will_be = 0
    max_width_name = 0
    max_width_days_til = 0
    max_width_will_be = 0
    space = r' '
    width_space = font.getsize(space)
    for e in events:
        if len(e.name) > max_name:
            max_name = len(e.name)
            max_width_name = font.getsize(e.name)
        if len(str(e.days_til_event())) > max_days_til:
            max_days_til = len(str(e.days_til_event()))
            max_width_days_til = font.getsize(str(e.days_til_event()))
        if len(str(e.will_be())) > max_will_be:
            max_will_be = len(str(e.will_be()))
            max_width_will_be = font.getsize(str(e.will_be()))

#    _logger.debug(f"{width}")
#    _logger.debug(f"{max_width_name[0]} {max_width_days_til[0]} {max_width_will_be[0]}")
#    _logger.debug(f"{max_name} {max_days_til} {max_will_be}")
    extra_width = width - max_width_name[0] - max_width_days_til[0] - max_width_will_be[0] - width_space[0]*2
    if extra_width < 0:
#        _logger.warning(f"extra width {extra_width} is less than zero!")
#        _logger.warning(f"Choose a smaller font (current size is {font.size})")
        # TODO should truncate the name
        max_name = max_name + extra_width
        extra_width = 0
    num_spaces = floor((extra_width / width_space[0]) / 3)
#    _logger.debug(f"num_spaces: {num_spaces}")
    f = '{0:<%d} {1:>%d} {2:>%d}' % (max_name + num_spaces+1, max_days_til + num_spaces, max_will_be + num_spaces)
    _logger.debug(f)
    import textwrap 
    for e in events:
        # draw name
#        message = f.format(e.name, e.days_til_event(), e.will_be())
        message = f.format(textwrap.shorten(e.name, width=max_name + num_spaces, placeholder=""), e.days_til_event(), e.will_be())
#        _logger.debug(message)
        draw.text((x_current, y_current), message, fill=(0, 0, 0), font=font)
        name_w, name_h = font.getsize(message)
        y_current = y_current + name_h + padding + padding

    y_current = 0
    name_w, name_h = font.getsize(events[0].name)
    y_current = y_current + name_h + padding

    for e in events[1:]:
        # draw horizontal line after event with padding
        for x in range(0, width):
            img.putpixel((x, y_current), (255, 255, 0))
        name_w, name_h = font.getsize(e.name)
        y_current = y_current + name_h + padding + padding

    return img


class InkyPhat(object):
    WIDTH = 212
    HEIGHT = 104


def main(events_csv, base_image, max_height=InkyPhat.HEIGHT,
         max_width=InkyPhat.WIDTH, font_size=14, font_path=None):

    width_events = 125
    width_logo = InkyPhat.WIDTH - width_events
    img = Image.new(MODE, (InkyPhat.WIDTH, InkyPhat.HEIGHT), 1)
#    draw = ImageDraw.Draw(img)

    # get font
    font = get_font(font_size, font_path)

    # set background image
    background_image = Image.open(base_image)
    img.paste(background_image)
#    image_right = draw_logo(font, InkyPhat.HEIGHT, width_logo)

    # get events
#    event_source = events_csv
    events = get_events(font, max_height=max_height, max_width=max_width, event_file=events_csv)

    # draw events
    image_left = draw_events(events, font, max_height, width_events)

    img.paste(image_left, (0, 0))
#    img.paste(image_right, (width_events,0))
#    draw.bitmap((width_events,0), image_right)
#    draw.bitmap((0,0), image_left)
    img.save(r'countdown.bmp')
#    image_left.save(r'countdown_left.bmp')
#    image_right.save(r'countdown_right.bmp')

    img = img.convert("P")
   
    img.save(r'countdown_p.bmp')
    # draw graphic

    # draw legend
    return img
