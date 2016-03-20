import mraa, time, pickle

GPIO = [13,12,11,10] 
pump_running = False

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
    time.sleep(time_interval)
    x.write(0)
    pump_running = False
