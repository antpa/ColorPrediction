from itertools import cycle
import random
import sys

from nn import *

import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH  = 512
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
MIDDLEHEIGHT = SCREENHEIGHT * 0.5
FIRSTQUARTER = SCREENWIDTH * 0.25
LASTQUARTER = SCREENWIDTH * 0.75

try:
    xrange
except NameError:
    xrange = range

def main():
    global SCREEN, FPSCLOCK, myfont
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Color Prediction')
    myfont = pygame.font.SysFont("Roboto", 30)
    fill = getRandomColor()
    
    brain = NeuralNetwork(3,3,2)
    
    # Intialize a bit the network
    for i in range(0, 10000) :
        sum = fill[0] + fill[1] + fill[2]
        if sum > 300:
            target = array([0,1]) # black
        else :
            target = array([1,0]) # white
        
        brain.train(array(fill), target)
        fill = getRandomColor()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                if pos_x > SCREENWIDTH / 2 :
                    target = array([0,1]) # black
                else :
                    target = array([1,0]) # white
                
                brain.train(array(fill), target)
                fill = getRandomColor()

        # draw sprites
        SCREEN.fill(fill)
        h, o = brain.feedforward(array(fill))
        if o[0] > o [1] : # black
            pygame.draw.ellipse(SCREEN, (0,0,0), (FIRSTQUARTER - 10, MIDDLEHEIGHT + 20, 20, 20), 0)
            label_prob = myfont.render(str(o[0]), 1, (0,0,0))
            SCREEN.blit(label_prob, (SCREENWIDTH / 2 - label_prob.get_width() / 2, MIDDLEHEIGHT + 40))
        else: # white
            pygame.draw.ellipse(SCREEN, (255,255,255), (LASTQUARTER - 10, MIDDLEHEIGHT + 20, 20, 20), 0)
            label_prob = myfont.render(str(o[1]), 1, (255,255,255))
            SCREEN.blit(label_prob, (SCREENWIDTH / 2- label_prob.get_width() / 2, MIDDLEHEIGHT + 40))

        sum = fill[0] + fill[1] + fill[2]
        if sum > 255*3/2:
            color = (0,0,0)
        else : 
            color = (255,255,255)
        label_sum = myfont.render(str(sum), 1, color)

        SCREEN.blit(label_sum, (SCREENWIDTH / 2, 40))
        label_black = myfont.render("BLACK", 1, (0,0,0))
        SCREEN.blit(label_black, (FIRSTQUARTER - label_black.get_width() / 2, MIDDLEHEIGHT - 20))
        label_white = myfont.render("WHITE", 1, (255,255,255))
        SCREEN.blit(label_white, (LASTQUARTER - label_white.get_width() / 2, MIDDLEHEIGHT - 20))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomColor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

if __name__ == '__main__':
    main()
