import gpiozero as gpio
from time import sleep
"""
EXIT WITH CTRL+C TO TRIGGER THE EXCEPT 
"""

class LedController:
    def __init__(self,*led_locations):
            self.leds = []
            for loc in led_locations:
                self.leds.append(gpio.LED(loc))
            self.current_active = 0
            
    def activate_next(self):
                                  #get the final item index
        if self.current_active <= len(self.leds) - 1:
            self.leds[self.current_active].on()
            self.current_active+=1
    
    def activate_all(self,step):
        for active in range(self.current_active,len(self.leds),1):
            self.leds[active].on()
            self.current_active+=1
            sleep(step)
            
    def deactivate_all(self,step):
        for active in range(self.current_active-1,-1,-1):
            self.leds[active].off()
            sleep(step)
        self.current_active = 0
    
    def flash_all(self,time_per_flash,num_flashes):
        is_led_on = self.leds[0].value > 0 #true if the light is on
        sleep(time_per_flash)
        for i in range(num_flashes):
            is_led_on = not is_led_on
            for led in self.leds:
                if is_led_on:
                    led.on()
                else:
                    led.off()
            sleep(time_per_flash)
        if is_led_on:
            self.current_active = len(self.leds)
        else:
            self.current_active = 0
        
class NamedLedController:
    def __init__(self,keys,values):
        self.leds = {}
        for i,key in enumerate(keys):
            self.leds[key] = gpio.LED(values[i])
    def activate_led(self,name):

        self.leds[name].on()
    
    def deactivate_led(self,name):
        self.leds[name].off()
    

"""
EXAMPLE SCRIPT
""" 
def mainaaa():
    led_controller = LedController(26,19,21,6,5)
    try:
        print("aaaa")
        led_controller.activate_all(0.1)
        led_controller.flash_all(0.3,4)
        led_controller.deactivate_all(0.1)
        while True:
            input("press enter to activate next led")
            led_controller.activate_next()
    except KeyboardInterrupt:
        pass
    finally:
        led_controller.deactivate_all(0.5)

def main():
    named_control = NamedLedController(("RED","YELLOW"),(21,20))
    named_control.activate_led("YELLOW")
    sleep(2)
    named_control.deactivate_led("YELLOW")
if __name__ == "__main__":
    mainaaa()