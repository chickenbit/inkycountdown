import os
import countdown

if __name__ == "__main__":
    this_dir = os.getcwd()
    events = os.path.join(this_dir, "resources", "example_events.csv")
    events = os.path.join(this_dir, "resources", "pi_releases.csv")
    background_image = os.path.join(this_dir, "resources", "InkyPhat-Birthday-Countdown.png")
    countdown.main(events_csv=events, font_size=15, base_image=background_image)
