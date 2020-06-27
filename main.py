import argparse
import os
import countdown

_this_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Update countdown on the inkyPhat eInk display.',
				usage="""

  # Scenario 1: use included resources\pi_releases.csv as events
  %(prog)s


  # Scenario 2: Specify csv to use as events
  %(prog)s --events resources/example_events.csv

  # Scenario 3: Specify font to use
  %(prog)s --font_path /usr/share/fonts/truetype/freefont/FreeMonoBold.ttf

""")
parser.add_argument('--events', 
                    default=os.path.join(_this_dir, "resources", "pi_releases.csv"))
parser.add_argument('--bg_image', 
                    default=os.path.join(_this_dir, 
                                         "resources", 
                                         "InkyPhat-Birthday-Countdown.png"))
parser.add_argument('--font_size', default=15, type=int)
parser.add_argument('--font_path', default=None, type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    image = countdown.main(events_csv=args.events,
                           font_size=args.font_size,
                           base_image=args.bg_image,
                           font_path=args.font_path)
    if os.path.isfile(r'/proc/device-tree/model'):
        # non full proof way to conditionally set image on when on a rpi
        # https://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
        from inky import InkyPHAT
        inkyphat = InkyPHAT('yellow')
        inkyphat.set_image(image)
        inkyphat.set_border(InkyPHAT.BLACK)
        inkyphat.show()
