import mraa, time, pickle
#import pyupm_grove as grove

GPIO = [10,12,14,16,18]
pump_running = False
GPIO_BTN1 = 5
GPIO_BTN2 = 6
RELAY_FACTOR = 0

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
    if num == 1  :
        previous_pressed()
    elif num == 2  :
        next_pressed()

def previous_presssed() :
    print "previous pressed"

def next_pressed() :
    print "next pressed"
