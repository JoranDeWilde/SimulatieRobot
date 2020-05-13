import pygame
import random
import math
import numpy

class Robot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #Plantenpot die de robot mag negeren. Dit zodat de robot niet steeds dezelfde plant oppakt en neezet
        self.ignorePlant = 0
        self.orientation = 180
        self.plant = None
        self.gevondenPlanten = []

class Plant(object):
    def __init__(self, x, y, nr):
        self.x = x
        self.y = y
        self.opgepakt = False
        self.nr = nr

#Tekent situatie op het scherm
def draw_situation(robot,Plant1,Plant2,Plant3,Plant4):
    win.fill((255,255,255))
    if(robot.orientation == 90):
        orientation = 270
    elif(robot.orientation == 270):
        orientation = 90
    else:
        orientation = robot.orientation
    img = pygame.transform.rotate(robotImg,orientation)
    win.blit(img, (robot.x, robot.y))

    win.blit(bloempotImg, (Plant1.x, Plant1.y))
    win.blit(bloempotImg, (Plant2.x, Plant2.y))
    win.blit(bloempotImg, (Plant3.x, Plant3.y))
    win.blit(bloempotImg, (Plant4.x, Plant4.y))

#Laat robot in een willekeurige richting even lopen. Er is gekozen om een richting voor 8 keer na elkaar te kiezen, zodat hij niet om de cm
#opnieuw moet kiezen.
def loopRandomRond(robot):

    add_x = random.choice(operationList) * 15
    add_y = random.choice(operationList) * 15

    while add_x == 0 and add_y == 0:
        add_x = random.choice(operationList) * 15
        add_y = random.choice(operationList) * 15

    for i in range(8):
        if robot.x + add_x > 100 and robot.x + add_x < 700:
            robot.x = robot.x + add_x
            if robot.plant is not None:
                robot.plant.x = robot.x

        if robot.y + add_y > 100 and robot.y + add_y < 700:
            robot.y = robot.y + add_y
            if robot.plant is not None:
                robot.plant.y = robot.y

        draw_situation(robot,Plant1,Plant2,Plant3,Plant4)
        pygame.draw.rect(win, (0, 0, 0), (100, 100, height - 230, width - 150), 4)
        pygame.time.delay(snelheid)
        pygame.display.update()
    return robot.x, robot.y

def checkVoorPlanten(x,y,ignorePlant):
    # Check of er plantenpotten in de buurt staan, kies de dichtste plant
    minDistance = 1000000
    goToPlant = None

    for plant in bloempottenLijst:
        dist = math.sqrt((x - plant.x) ** 2 + (y - plant.y) ** 2)

        # Indien ignorePlant niet None is, wil dit zeggen dat de robot deze plant vast heeft en dus niet moet checken of deze dichtbij is
        if ignorePlant is not None:
            if plant.nr == ignorePlant:
                dist = 100000
        if robot.plant is not None:
            if plant.nr == robot.plant.nr:
                dist = 100000

        if dist < minDistance:
            goToPlant = plant
            minDistance = dist

    #Kijk of de dichtste plant in de buurt ligt van het bereik van de sensor. Zo niet kan de robot deze eigenlijk niet zien
    if minDistance < 250:
        return goToPlant
    else:
        return None

def placePlant(robot,plant):
    robot.plant = None
    plant.opgepakt = False

def pickUpPlant(robot,plant):
    if robot.plant is None or robot.plant is 0:
        robot.plant = plant
        plant.opgepakt =True

def movePlantToSafePlace(robot,plant):
    safe = False
    while not safe:
        robot.x, robot.y = loopRandomRond(robot.x, robot.y, plant)
        if checkVoorPlanten(robot.x,robot.y,plant.nr) is None:
            safe = True
            robot.ignorePlant = plant.nr
        #pygame.time.delay(snelheid)
    plant.opgepakt = False

def checkPlantenOpstelling():
    goed = True
    for plant1 in bloempottenLijst:
        for plant2 in bloempottenLijst:
            if plant1 is not plant2:
                #Als 2 plantenpotten nog te dicht bij elkaar staan (<250) dan is de opstelling nog niet goed
                if math.sqrt((plant1.x - plant2.x) ** 2 + (plant1.y - plant2.y) ** 2) < 250:
                    goed = False
    return goed

#De robot rijdt in een bepaalt aantal stappen naar de plant toe
def rijdRobotNaarPlant(x,y,plant):
    aantalX = abs(x - plant.x)/snelheid
    aantalY = abs(y - plant.y)/snelheid
    aantalStappen = math.ceil(max(aantalX, aantalY))

    for i in range(aantalStappen):
        if abs(robot.x-plant.x) >= 15:
            robot.x = robot.x + 15*numpy.sign(plant.x - x)
        else:
            robot.x = plant.x
        if abs(robot.y - plant.y) >= 15:
            robot.y = robot.y + 15*numpy.sign(plant.y - y)
        else:
            robot.y = plant.y

        draw_situation(robot, Plant1, Plant2, Plant3, Plant4)
        pygame.draw.rect(win, (0, 0, 0), (100, 100, height - 230, width - 150), 4)
        pygame.display.update()
        pygame.time.delay(snelheid)
    robot.x = plant.x
    robot.y = plant.y

def rijCirkelEnMap(robot,straal):
    stappen = math.ceil(2*math.pi*straal/15)
    hoek = 0
    center_x = robot.x
    center_y = robot.y - straal

    while(hoek < 2*math.pi):
        x = straal * math.sin(hoek) + center_x
        if 100 < x < 700:
            robot.x = x

        y = straal * math.cos(hoek) + center_y
        if 100 < y < 700:
            robot.y = y

        # Increase the angle in prep for the next round.
        hoek += (360/stappen)*math.pi/180

        for plant in bloempottenLijst:
            if math.sqrt((plant.x - center_x) ** 2 + (plant.y - center_y) ** 2) < straal+250:
                if plant.nr is not robot.ignorePlant:

                    robot.gevondenPlanten.append(plant)


        draw_situation(robot, Plant1, Plant2, Plant3, Plant4)
        pygame.draw.rect(win, (0, 0, 0), (100, 100, height - 230, width - 150), 4)
        pygame.display.update()
        pygame.time.delay(snelheid)

def draai90Graden(robot):
    robot.orientation = (robot.orientation + 90)%360
    draw_situation(robot, Plant1, Plant2, Plant3, Plant4)

def rijRechtdoor(robot,meter):
    if meter is 0:
        draw_situation(robot, Plant1, Plant2, Plant3, Plant4)
        pygame.draw.rect(win, (0, 0, 0), (100, 100, height - 230, width - 150), 4)
        pygame.display.update()
        pygame.time.delay(snelheid)
        return

    if robot.orientation == 0:
        x =  robot.x
        y = max(robot.y - meter, 700)
    elif robot.orientation == 90:
        x = min(robot.x + meter, 100)
        y= robot.y
    elif robot.orientation == 180:
        x = robot.x
        y = min(robot.y + meter, 100)
    else:
        x = max(robot.x - meter, 700)
        y = robot.y

    aantalstappen = math.ceil(meter/15)
    for i in range(aantalstappen):
        if abs(robot.x-x) >= 15:
            robot.x = robot.x + 15*numpy.sign(x - robot.x)
            if robot.plant is not None:
                robot.plant.x = robot.x
        else:
            robot.x = x
            if robot.plant is not None:
                robot.plant.x = robot.x
        if abs(robot.y - y) >= 15:
            robot.y = robot.y + 15*numpy.sign(y - robot.y)
            if robot.plant is not None:
                robot.plant.y = robot.y
        else:
            robot.y = y
            if robot.plant is not None:
                robot.plant.y = robot.y
        draw_situation(robot, Plant1, Plant2, Plant3, Plant4)
        pygame.draw.rect(win, (0, 0, 0), (100, 100, height - 230, width - 150), 4)
        pygame.display.update()
        pygame.time.delay(snelheid)

def beeindigSpel():
    pygame.font.init()
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Potten staan ver genoeg van elkaar', 1, (0, 0, 0))

    win.blit(label, (300, 300))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

#Settings van display instellen
height = 950
width = 850
win =pygame.display.set_mode((height , width))
win.fill((255,255,255))
pygame.display.set_caption('Simulatie van robot')

robotImg = pygame.image.load('HA.png')

#Random kiest telkens of de robot een stap achteruit zet, vooruit, of niets doet via deze lijst van operations
operationList = [-1, 0, 1]

#Initialising plantenbakken
Plant1 = Plant(100, 100, 1)
Plant2 = Plant(230, 230, 2)
Plant3 = Plant(100, 230, 3)
Plant4 = Plant(230, 100, 4)
bloempottenLijst = [Plant1,Plant2,Plant3,Plant4]
bloempotImg = pygame.image.load('bloempot.png')

#Startpositie robot
x = height*0.5
y = width*0.5
robot = Robot(x, y)

#Bepaald hoe snel de simulatie verloopt
snelheid = 5

start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                start = True

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #TODO: In te vullen door de leerlingen
    rijRechtdoor(robot,700)

    gevondenPlant = checkVoorPlanten(robot.x,robot.y,robot.plant)
    if gevondenPlant is not None:
        if robot.plant is None:
            rijdRobotNaarPlant(robot.x,robot.y,gevondenPlant)
            pickUpPlant(robot,gevondenPlant)
    else:
        if robot.plant is not None:
            placePlant(robot,robot.plant)
    draai90Graden(robot)

    pygame.time.delay(snelheid)
    if checkPlantenOpstelling():
        done = True
        beeindigSpel()