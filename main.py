from wireless import wifi
# this example is based on Particle Photon
# change the following line to use a different wifi driver
from espressif.esp8266wifi import esp8266wifi as wifi_driver
import streams

# Import the Zerynth APP library
from zerynthapp import zerynthapp

streams.serial()

sleep(1000)
print("STARTING...")

pinMode(D0,OUTPUT) # red
pinMode(D1,OUTPUT) # green
pinMode(D2,OUTPUT) # blue

# variables for the current status of the LED
current_r = LOW
current_g = LOW
current_b = LOW

# define a RPC function: generate a random number
def turn_on():
    digitalWrite(D0,current_r)
    digitalWrite(D1,current_g)
    digitalWrite(D2,current_b)

def turn_off():
    digitalWrite(D0,LOW)
    digitalWrite(D1,LOW)
    digitalWrite(D2,LOW)
    
def red_led():
    if (current_r == LOW):
        digitalWrite(D0, HIGH)
        current_r = HIGH
    else:
        digitalWrite(D0, LOW)
        current_r = LOW
    
def green_led():
    if (current_g == LOW):
        digitalWrite(D1, HIGH)
        current_g = HIGH
    else:
        digitalWrite(D1, LOW)
        current_g = LOW

def blue_led():
    if (current_b == LOW):
        digitalWrite(D2, HIGH)
        current_b = HIGH
    else:
        digitalWrite(D2, LOW)
        current_b = LOW


# send events on button pressed
def on_btn():
    zapp.event({"my_button":"pressed"})

onPinFall(BTN0,on_btn,debounce=1000)


# Device UID and TOKEN can be created in the ADM panel
zapp = zerynthapp.ZerynthApp("_vb0ElDHQy-cfNsXUORK0Q", "h9aIzQJ3QsiQIPrSLQy4pA", log=True)

# link "random" to do_random
zapp.on("turn_on", turn_on)
zapp.on("turn_off",turn_off)
zapp.on("RED", red_led)
zapp.on("GREEN", green_led)
zapp.on("BLUE", blue_led)

try:
    # connect to the wifi network (Set your SSID and password below)
    wifi_driver.auto_init()
    for i in range(0,5):
        try:
            wifi.link("NETGEAR_EXT",wifi.WIFI_WPA2,"7349886F52")
            break
        except Exception as e:
            print("Can't link",e)
    else:
        print("Impossible to link!")
        while True:
            sleep(1000)

    # Start the Zerynth app instance!
    # Remember to create a template with the files under the "template" folder you just cloned
    # upload it to the ADM and associate it with the connected device
    zapp.run()
    
    # Do whatever you need here
    while True:
        print(".")
        sleep(5000)
        
except Exception as e:
    print(e)
