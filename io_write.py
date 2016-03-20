import mraa, time, pickle
import pyupm_grove as grove

GPIO = [13,12,11,10]
pump_running = False
GPIO_BTN1 = 5
GPIO_BTN2 = 6
LEDOn = False
RELAY_FACTOR = 0.6

"""
Enable pump_no for time_interval seconds
"""
def enable_pump(pump_no, time_interval) :
    print " pump " + str(pump_no) + " time " + str(time_interval)
    global pump_running
    if pump_running :
        return
    pump_running = True
    x = mraa.Gpio(GPIO[pump_no])
    x.dir(mraa.DIR_OUT)
    x.write(1)
    time.sleep(time_interval + RELAY_FACTOR)
    x.write(0)
    pump_running = False

def button_press(num) :
    if(num == 1)
        previous_pressed()
    else if(num ==2)
        next_pressed()

def previous_presssed() :
    print "previous pressed"

def next_pressed() :
    print "next pressed"

class BtnWatchThread (threading.Thread):

    def __init__(self, threadID, pin, num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.pin = pin
        self.num = num

    def run(self):
        button = grove.GroveButton(self.pin)
        while True :
            #print button.name(), ' value is ', button.value()
            value = button.value()
            time.sleep(1)
            button_press(num)
            #print "Exiting " + self.name
        del button

class LEDWatchThread (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # Create the Grove LED object using GPIO pin 2
        led = grove.GroveLed(5)
        # Print the name
        print led.name()
        while LEDOn :
            # Turn the LED on and off 10 times, pausing one second
            # between transitions
            for i in range (0,10):
                led.on()
                time.sleep(1)
                led.off()
                time.sleep(1)
            # Delete the Grove LED object
        del led
