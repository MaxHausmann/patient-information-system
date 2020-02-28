from microbit import *
import radio

radio.on()
radio.config(address=0x75626974)

data = radio.receive()