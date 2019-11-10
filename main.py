import os
import countdown

if __name__ == "__main__":
    this_dir = os.getcwd()
    events = os.path.join(this_dir, "resources", "pi_releases.csv")
    background_image = os.path.join(this_dir, "resources", "InkyPhat-Birthday-Countdown.png")
    image = countdown.main(events_csv=events, font_size=15, base_image=background_image)
    if os.path.isfile(r'/proc/device-tree/model'):
        # non full proof way to conditionally set image on when on a rpi
        # https://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
        from inky import InkyPHAT
        inkyphat = InkyPHAT('yellow')
        inkyphat.set_image(image)
        inkyphat.set_border(inky.BLACK)
        inkyphat.show()
