
from microbit import *
import utime
import radio


radio.on()
radio.config(address=0x75626974)

# Pulszähler
pulsecounter = 0

# Timerstart
timerT = int(utime.ticks_ms() / 1000)

###########################################################

# Timing settings
sekunden_in_milli = 1000

SAMPLE_RATE = 25  # zwischen 25-100
SAMPLE_INTERVAL = int(sekunden_in_milli / SAMPLE_RATE)

# Pulsdetektion
threshold_on = 550
threshold_off = 500
beat = False

sample_zw_schlaegen = 0

while True:

    if button_a.is_pressed():
        # Sampling loop:
        while True:

            # read signal from input in pin 2 (currently PulseSensor.com)
            # Signal: Original = 0-1000.
            Signal = pin2.read_analog()

            sample_zw_schlaegen += 1

            # indicate pulse on microbit
            # in pulse wave peak ?
            if beat is False and (Signal > threshold_on):
                beat = True
                display.show(Image.HEART)
                display.set_pixel(2, 2, 9)  # LED pixel on

            # not in pulse wave peak ?
            if beat is True and (Signal < threshold_off):
                beat = False
                display.show(Image.HEART_SMALL)
                display.set_pixel(2, 2, 0)  # LED pixel off
                pulsecounter = pulsecounter+1
                # reset counter of samples_between_beats
                sample_zw_schlaegen = 0

            # Signal anpassen, damit voller Plot ausgenutzt wird
            Signal = 2*Signal - 1000
            # print("({})".format(Signal))
            print("({}, {})".format(Signal, sample_zw_schlaegen*10))

            # pause between samples
            sleep(SAMPLE_INTERVAL)

            if timerT >= 10:
                break

######################################################

pulserate = pulsecounter * 6

radio.send("Messdauer: 10 Sekunden", pulserate)

radio.off()