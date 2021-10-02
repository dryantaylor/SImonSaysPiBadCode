import RPi.GPIO as gpio

import pygame
def convert_pygame_key_to_value(key):
    keys = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
            pygame.K_q: 3, pygame.K_w: 4, pygame.K_e: 5,
            pygame.K_a: 6, pygame.K_s: 7, pygame.K_d: 8,
            pygame.K_z: 9, pygame.K_x:10, pygame.K_c:11}
    if key in keys.keys():
        return keys[key]
    else: return 12
    
    
class Keypad12:
    
    def __init__(self,row_one,row_two,row_three,row_four,col_one,col_two,col_three,outputMatrix):
        self.prev_input = None
        self.ROWS = [row_one,row_two,row_three,row_four]
        self.COLS = [col_one,col_two,col_three]
        self.MATRIX = outputMatrix
        
        """SETUP"""
        gpio.setmode(gpio.BCM)

        for i in self.COLS:
            gpio.setup(i,gpio.OUT)
            gpio.output(i,1)
    
        for i in self.ROWS:
            gpio.setup(i,gpio.IN, pull_up_down= gpio.PUD_UP)
        
    def get_input(self):
        has_button_pressed = False
        for j in range(len(self.COLS)):
            gpio.output(self.COLS[j],0)
            for i in range(len(self.ROWS)):
                output = self.MATRIX[i][j]
                if gpio.input(self.ROWS[i]) == 0:
                    has_button_pressed = True
                    if self.prev_input != output:
                        gpio.output(self.COLS[j],1)
                        self.prev_input = output
                        return output
            gpio.output(self.COLS[j],1)
        if not has_button_pressed:
            self.prev_input = None
        return None
