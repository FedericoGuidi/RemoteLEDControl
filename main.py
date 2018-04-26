from wireless import wifi
from espressif.esp8266wifi import esp8266wifi as wifi_driver
import streams
import threading

# Import the Zerynth APP library
from zerynthapp import zerynthapp

streams.serial()

sleep(1000)
print("STARTING...")

# save the index.html in the board flash
new_resource("template/index.html")

# set the LED pins as outputs
pinMode(D0,OUTPUT) # red
pinMode(D1,OUTPUT) # green
pinMode(D2,OUTPUT) # blue

# variables for the current status of the LED
current_r = LOW
current_g = LOW
current_b = LOW

# global variables
on = False
stopped = False

# RPC functions to manage the LED
def turn_on():
    global on
    on = True
    digitalWrite(D0,current_r)
    digitalWrite(D1,current_g)
    digitalWrite(D2,current_b)

def turn_off():
    global on
    on = False
    digitalWrite(D0,LOW)
    digitalWrite(D1,LOW)
    digitalWrite(D2,LOW)
    
def red_led():
    if (current_r == LOW):
        current_r = HIGH
    else:
        current_r = LOW
    global on
    if on:
        digitalWrite(D0,current_r)
    
def green_led():
    if (current_g == LOW):
        current_g = HIGH
    else:
        current_g = LOW
    global on
    if on:
        digitalWrite(D1,current_g)

def blue_led():
    if (current_b == LOW):
        current_b = HIGH
    else:
        current_b = LOW
    global on
    if on:
        digitalWrite(D2,current_b)
        
def rainbow():
    global stopped
    stopped = False
    def run():
        while not stopped:
            # purple
            digitalWrite(D0,HIGH)
            digitalWrite(D2,HIGH)
            sleep(200)
            # blue
            digitalWrite(D0,LOW)
            sleep(200)
            # sky blue
            digitalWrite(D1,HIGH)
            sleep(200)
            # green
            digitalWrite(D2,LOW)
            sleep(200)
            # yellow
            digitalWrite(D0,HIGH)
            sleep(200)
            # red
            digitalWrite(D1,LOW)
            sleep(200)
            if stopped:
                global on
                if on:
                    digitalWrite(D0,current_r)
                    digitalWrite(D1,current_g)
                    digitalWrite(D2,current_b)
                else:
                    digitalWrite(D0,LOW)
                    digitalWrite(D1,LOW)
                    digitalWrite(D2,LOW)
                break
    thread = threading.Thread(target=run)  
    thread.start()

def rainbow_stop():
    global stopped
    stopped = True

# Device UID and TOKEN can be created in the ADM panel
zapp = zerynthapp.ZerynthApp("UID", "TOKEN", log=True)

# link Python functions to Javascript
zapp.on("turn_on", turn_on)
zapp.on("turn_off",turn_off)
zapp.on("RED", red_led)
zapp.on("GREEN", green_led)
zapp.on("BLUE", blue_led)
zapp.on("RAINBOW", rainbow)
zapp.on("STOP", rainbow_stop)

try:
    # connect to the wifi network (Set your SSID and password below)
    wifi_driver.auto_init()
    for i in range(0,5):
        try:
            wifi.link("SSID",wifi.WIFI_WPA2,"PASSWORD")
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
    