import random
from math import *

base_speed = 10
base_size = 10
base_sense = base_size*3
base_movement = 5
base_energy = 1000
base_cost = 10
speed_adj_factor = 0.141421356237
size_adj_factor = 0.158740105197
sense_adj_factor = 0.2
eating_dist = 2*base_size
reproReq = 2

INF = 10000000

WIDTH = 1000
HEIGHT = 1000

counter = 1

def mutate(unit, parent):
    unit.x = parent.x
    unit.y = parent.y
    unit.angle = parent.angle
    
    chance = [-1, 0, 1]
    rand = random.choice(chance)
    red = parent.color[0]
    green = parent.color[1]
    blue = parent.color[2]
    if rand == 0:
        unit.speed = parent.speed
    else:
        green = 0
        unit.speed = max(0, parent.speed + rand*random.uniform(0.1, 1))
        if unit.speed > base_speed:
            red = 255
            green = 0
            blue = 0
        else:
            red = 0
            green = 0
            blue = 255
        
    rand2 = random.choice(chance)
    if rand2 == 0:
        unit.sense = parent.sense
    else:
        unit.sense = max(0, parent.sense + rand*random.uniform(0.1, 1))

    rand3 = random.choice(chance)
    if rand3 == 0:
        unit.size = parent.size
    else:
        unit.size = max(0, parent.size + rand*random.uniform(0.1, 1))
    
    unit.color = (red, green, blue)
    unit.cost = calculateCost(unit)
    return 

def distance(p1x, p1y, p2x, p2y):
    return ((p1x - p2x)**2 + (p1y - p2y)**2)**0.5

def randomizeStart(unit):
    global HEIGHT, WIDTH
    lineSegment = random.choice([0, 1, 2, 3])
    x, y, angle = 0, 0, 0
    if lineSegment == 0: # ---
        x = random.randint(1, WIDTH)
        y = 0
        angle = 90
    elif lineSegment == 1: # <- |
        x = WIDTH - 1
        y = random.randint(1, HEIGHT)
        angle = 180
    elif lineSegment == 2: # __
        x = random.randint(1, WIDTH)
        y = HEIGHT - 1
        angle = 270
    else:  # | ->
        x = 0
        y = random.randint(1, HEIGHT)
        angle = 0
    unit.x = x
    unit.y = y
    unit.angle = angle

def moveTowards(unit, food, dist):
    if dist < eating_dist:
        unit.x = food[0]
        unit.y = food[1]
    else:
        unit.x = unit.x + (base_movement*unit.speed/base_speed)*(food[0] - unit.x)/dist
        unit.y = unit.y + (base_movement*unit.speed/base_speed)*(food[1] - unit.y)/dist

def calculateCost(unit):
    return (4/3*pi*(unit.size*size_adj_factor)**3)*((unit.speed*speed_adj_factor)**2)/2 + (unit.sense*sense_adj_factor)

class Unit:
    def __init__(self, parent = None, currTime = 0):
        global counter
        self.id = counter
        self.speed = base_speed
        self.size = base_size
        self.sense = base_sense
        self.x = -1
        self.y = -1
        self.angle = -1
        self.energy = base_energy
        self.foodCount = 0
        self.cost = base_cost
        self.color = (0, 255, 0)
        self.birth = currTime
        self.death = INF
        counter+=1

        randomizeStart(self)
        if parent:
            mutate(self, parent)
            # print("Speed :", self.speed, " Sense: ", self.sense)
        pass

    def move(self, Foods, units):
        global WIDTH, HEIGHT
        if self.cost > self.energy:
            return (False, -1)
        
        foodCaught = -1
        moved = False
        minDist = 100000
        closestFood = None
        minIdx = -1
        for idx, food in enumerate(Foods):
            dist = distance(self.x, self.y, food[0], food[1])
            if dist < self.sense and dist < minDist:
                minDist = dist
                closestFood = food
                minIdx = idx
        
        if closestFood:
            moveTowards(self, closestFood, minDist)
            newDist = distance(self.x, self.y, closestFood[0], closestFood[1])
            if newDist < eating_dist:
                foodCaught = minIdx
            moved = True

        if not moved:
            self.x = self.x + (base_movement*self.speed/base_speed)*cos(self.angle*pi/180)
            self.y = self.y + (base_movement*self.speed/base_speed)*sin(self.angle*pi/180)
            deviate = random.randint(0, 20);
            sign = random.choice([-1, 1])
            angle = self.angle + deviate*sign

            x = self.x + (base_movement*self.speed/base_speed)*cos(self.angle*pi/180)
            y = self.y + (base_movement*self.speed/base_speed)*sin(self.angle*pi/180)
            if x >= WIDTH - 2 or x <= 0 or y >= HEIGHT - 2 or y <= 0:
                angle+=180
            self.angle = angle

        self.energy-=self.cost
        return (True, foodCaught)
        pass
