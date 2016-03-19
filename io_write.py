import mraa, time, pickle

GPIO_START = 13
pump_running = False

"""
Enable pump_no for time_interval seconds
"""
def enable_pump(pump_no, time_interval) :
    if pump_running :
        return
    pump_running = True
    x = mraa.Gpio(GPIO_START + pump_no)
    x.dir(mraa.DIR_OUT)
    x.write(1)
    time.sleep(time_interval)
    x.write(0)
    pump_running = False
