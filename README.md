# LEDmatrix

A 20 * 10 Pixel LED Matrix

Run the server:
	`python3 server/driver.py`

Run the client:
	`python3 -m client`

The serial paths are hardcoded for now.
So remember to boot the orange pi with the arduino plugged in,
wait a minute and only then plug in the HES controller (it all Just Works™)

The server driver is expecting `NUM_BYTES` (600) bytes to be written to a TCP socket (port 53777) per frame. Each three bytes represent a LED, and each of those three bytes are the color in standard RGB order. The first LED is the upper left corner, going right, then down, like so:
```
[
[00 01 02 03 04 05 06 07 08 09],
[10 11 12 13 14 15 16 17 18 19]
...
]
```

For arduino:
```
[
[09 08 07 06 05 03 03 02 01 00],
[10 11 12 13 14 15 16 17 18 19]
...
]
```

### Running the simulator
1.  - On Windows, get python 3 from [here]( https://www.python.org/downloads/) and **mark the option to add python 3 to PATH, on the installer**.
    - On GNU/Linux, run `sudo apt install python3 python3-pip`.
2. For either system, after installing python run `sudo pip3 install pygame`.
3. Run `python3 simulator.py` from the "server" folder, connect your program to port 53777 and go!
