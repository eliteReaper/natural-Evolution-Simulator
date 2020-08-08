import pygame
from Unit import *
from pygame.locals import *
import os
from CONSTANTS import *

pygame.init()
CLOCK = pygame.time.Clock()

surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
simOver = False



units = []
surface.fill((255, 255, 255))
for i in range(0, Population):
    u = Unit()
    pygame.draw.circle(surface, (0, 0, 0), (u.x, u.y), int(u.size))
    units.append(u)

''' Function to place food randomly on the grid'''
def placeFood(N):
    global Foods, units
    foodAt = random.sample(range(0, WIDTH*HEIGHT), N)
    for food in foodAt:
        Foods.append((food//WIDTH, food%HEIGHT)) 
        

'''This timer is to update the data in the data.txt file to update the graphs'''
pygame.time.set_timer(USEREVENT+1, 3000)

placeFood(Food_Count)
start = True


while not simOver:
    CLOCK.tick(FPS)
    surface.fill((255, 255, 255)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simOver = True
        if event.type == USEREVENT+1:
            ''' Updating data.txt file '''
            bestUnit = None
            with open("data.txt", "w") as wr:
                for unit in units:
                    wr.write(str(unit.speed) + " " + str(unit.sense) + " " + str(unit.size) + "\n")         
    
    for idx, unit in enumerate(units):
        moved, foodCaught = unit.move(Foods, units)
        if foodCaught != -1:
            unit.foodCount+=1
            del Foods[foodCaught]
            if len(units) < 2*Food_Count:
                placeFood(1)
        if not moved and unit.foodCount > 0:
            unit.foodCount-=1
            unit.energy+=base_energy
        elif not moved and unit.foodCount == 0:
            units.remove(unit)
        if unit.foodCount >= reproReq:
            units.append(Unit(unit))
            unit.foodCount-=reproReq
        
        for unit2 in units:
            if unit!=unit2:
                if distance(unit.x, unit.y, unit2.x, unit2.y) < eating_dist and unit.size >= 1.2*unit2.size:
                    unit.energy+=base_energy
                    unit.foodCount+=(max(1, unit2.foodCount))
                    units.remove(unit2)

        pygame.draw.circle(surface, (unit.color[0], unit.color[1], unit.color[2]), (int(unit.x), int(unit.y)), int(unit.sense), 2)
        pygame.draw.circle(surface, unit.color, (int(unit.x), int(unit.y)), int(unit.size))
    
    for food in Foods:
        pygame.draw.circle(surface, (0, 0, 0), (food[0], food[1]), 5)

    screen.blit(surface, (0,0))
    pygame.display.update()