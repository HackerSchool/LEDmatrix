BAUD = 115200 # Match arduino's baud rate

WIDTH = 10
HEIGHT = 20
NUM_LEDS = WIDTH * HEIGHT
NUM_BYTES = NUM_LEDS * 3

SOCK_PATH = '/tmp/ledmatrix'

BLACK = (0, 0, 0)
WHITE = (0xff, 0xff, 0xff)
RED = (0xff, 0, 0)
GREEN = (0, 0xff, 0)
BLUE = (0, 0, 0xff)

# Minimum time to sleep in between frames to avoid dropped frames.
# Calculated by trial and error!
# TODO: ????? why is it bigger than the server's MIN_PERIOD
MIN_PERIOD = 63e-3
