# inkycountdown

Python Script for displaying event countdown information to an [InkyPhat](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat) display on a raspberry pi.

## Example / Preview

Example image using Raspberry Pi version release days as birthdays.

```
Column 1: Pi Version
Column 2: Days till birthday!
Column 3: How old the Pi Version will be!
```

![Example inkycountdown as image][logo]

_ran on November 9, 2019_

# Usage

`main.py` is bootstrapped for command-line usage

  ## Scenario 1: use included resources\pi_releases.csv as events
  ```python
  main.py
  ```
  ## Scenario 2: Specify csv to use as events
  ```python
  main.py --events resources/example_events.csv
  ```
  ## Scenario 3: Specify font to use
  ```python
  main.py --font_path /usr/share/fonts/truetype/freefont/FreeMonoBold.ttf
  ```
  
# Resources

## Fonts

* https://pythonbytes.fm/episodes/show/154/code-frozen-in-carbon-on-display-for-all
* https://github.com/tonsky/FiraCode
* https://www.kutilek.de/sudo-font/

[logo]: ./resources/example.bmp "Example Countdown"

## TODO

* display the date last ran 
* optional column headers
* Auto font-size picker
