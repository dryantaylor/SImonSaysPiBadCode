import pygame
from random import randint
from math import floor
from time import sleep

from led import LedController,NamedLedController
from input import Keypad12

class Board:
    def __init__(self,D_WIDTH,D_HEIGHT,X_OFFSET,Y_OFFSET,SQUARE_SIZE,time_between_squares,keypad_flipped):
        self.display = pygame.display.set_mode((D_WIDTH,D_HEIGHT))
        self.X_OFFSET = X_OFFSET
        self.Y_OFFSET = Y_OFFSET
        self.SQUARE_SIZE = SQUARE_SIZE
        self.input_squares = []
        self.__generate_input_squares()
        self.pos_squares = []
        self.__generate_pos_squares()

        self.TIME_BETWEEN_SQUARES = time_between_squares

        print(self.input_squares)
        self.Led_controller = LedController(26,19,21,6,5)
        self.Named_controller = NamedLedController(("YELLOW","RED"),(16,20))
        self.Led_controller.deactivate_all(0.0)
        if not keypad_flipped:
            self.keypad = Keypad12(17,25,23,22, 27,4,18,
                                     [[0,1,2],
                                      [3,4,5],
                                      [6,7,8],
                                      [9,10,11]])
        else:
            self.keypad = Keypad12(17,25,23,22, 27,4,18,
                                     [[11,10,9],
                                      [8,7,6],
                                      [5,4,3],
                                      [2,1,0]])
    def reset(self):
        self.input_squares = []
        self.__generate_input_squares()
        self.pos_squares = []
        self.__generate_pos_squares()

    def run(self):
        round = 0
        active_square = 0
        time_remaining = self.TIME_BETWEEN_SQUARES
        clock = pygame.time.Clock()
        running = True
        recall = 0; #square currently being tested
        while running:
            delta_time = max(0, clock.tick())
            key_input = self.keypad.get_input()
            if active_square == -1:
                if key_input is not None:
                    if key_input == self.input_squares[recall]:
                        if recall < round-1:
                            recall+=1
                        else:
                            active_square = 0
                            time_remaining = self.TIME_BETWEEN_SQUARES
                            self.Led_controller.activate_next()
                            if round == 5:
                                active_square = -1
                                running = False
                                self.Named_controller.activate_led("YELLOW")
                                self.Led_controller.flash_all(0.5,4)
                                sleep(0.5)
                                self.Named_controller.deactivate_led("YELLOW")
                                sleep(0.1)
                                self.Led_controller.deactivate_all(0.5)
                                return "win"
                                
                                continue
                    else:
                        print("failed")
                        running = False
                        self.Named_controller.activate_led("RED")
                        self.Led_controller.deactivate_all(0.5)
                        self.Named_controller.deactivate_led("RED")                    
                        continue
                        return "lose"
                        
                    
            self.display.fill((0,0,0))
            if active_square != -1:
                time_remaining -= delta_time
                #print(time_remaining)
                if time_remaining <= 0:
                    if active_square < round:
                        active_square+=1
                        time_remaining = self.TIME_BETWEEN_SQUARES
                    else:
                        active_square = -1 #-1 means that no square is being considered
                        if round < 5:
                            round+= 1
                            recall = 0;
                            #rint(round)
                        
                            
                #print(active_square)
                pygame.draw.rect(self.display,(0,0,255),(self.pos_squares[active_square][0],self.pos_squares[active_square][1],100,100))
            pygame.display.flip()

        print("over")
        
    
    def __generate_input_squares(self):
        #generating the squares to be used as 4 integers between 0 and 12
        mem_squares = []
        while True:
            n = randint(0,11)
            if n not in self.input_squares:
                self.input_squares.append(n)
            if len(self.input_squares) == 5:
                break
    
    def __generate_pos_squares(self):
        #calc x,y pixel positions of the squares based off
        for i in self.input_squares:
            self.pos_squares.append(((i%3) * self.SQUARE_SIZE + self.X_OFFSET, # x co-ord
                                 floor(i/3)  * self.SQUARE_SIZE + self.Y_OFFSET)) #y co-ord
        
def main():
    pygame.init()
    board = Board(300,450,0,50,100,1000,True)
    font = pygame.font.SysFont(None, 50)
    imgOne = font.render('Press any', True, (255,255,255))
    imgTwo = font.render("key to begin", True, (255,255,255))
    #have the game be on repeat
    while True:
        board.display.blit(imgOne, (60, 150))
        board.display.blit(imgTwo, (45, 190))
        while board.keypad.get_input() == None:
            pygame.display.flip()
        state = board.run()
        if state == "win":
            pass
        else:
            pass
        board.reset()
    
    
#TODO: ADD IN WIN/LOSE SCREEN
if __name__ == "__main__":
    main()
    