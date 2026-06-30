from RF24 import *

radio = RF24(22, 0)   # o (17,0) en el receptor

radio.begin()

radio.printPrettyDetails()
