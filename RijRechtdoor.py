## @package RijRechtdoor
#  Dit package bevat de implementatie van het 'rij rechtdoor en draai'-algoritme.

import pygame
import random
import math
import numpy
import pandas as pd

## Deze klasse bevat alle parameters van de robot: zijn positie, welke plant hij vast heeft, zijn geheugen,... Onze robot die wij gebruiken is een object van deze klasse.
class Robot(object):

    ## Constructor: hiermee wordt de robot aangemaakt. Wanneer de robot wordt aangemaakt worden verschillende parameters geïnitialiseerd.
    #@param[in] x De x-waarde van de positie waarop de robot moet staan.
    #@param[in] y De y-waarde van de positie waarop de robot moet staan.


    def __init__(self, x, y):
        ## De x-positie van de robot.
        self.x = x
        ## De y-positie van de robot
        self.y = y
        ## Het nummer van de plant die de robot zal negeren wanneer het scant voor planten.
        self.ignorePlant = 0
        ## De orientatie waarin de robot momenteel staat (in graden). Dit start op 180°.
        self.orientation = 180
        ## Het plant-object dat de robot momenteel vast heeft. Dit is gelijk aan 'None' als de robot geen plant vast heeft.
        self.plant = None
        ## De lijst met gevonden planten door de robot.
        self.gevondenPlanten = []

## Deze klasse bevat alle parameters van de plant: zijn positie, of hij is opgepakt of niet,...
class Plant(object):

    ## Constructor: hiermee wordt de plant aangemaakt. Wanneer de plant wordt aangemaakt worden verschillende parameters geïnitialiseerd.
    # @param[in] x De x-waarde van de positie waarop de plant moet staan.
    # @param[in] y De y-waarde van de positie waarop de plant moet staan.
    def __init__(self, x, y, nr):
        ## De x-positie van de plant
        self.x = x
        ## De y-positie van de plant
        self.y = y
        ## Dit attribuut geeft weer of de plant is opgepakt. Als het op TRUE staat is de plant momenteel opgepakt door de robot. Indien niet, staat het op FALSE.
        self.opgepakt = False
        ## Het nummer van de plant, het id.
        self.nr = nr


## Tekent de huidige situatie op het scherm.
# @param[in]  robot  De robot
# @param[in]  Plant1  De eerste plantenpot
# @param[in]  Plant2  De tweede plantenpot
# @param[in]  Plant3  De derde plantenpot
# @param[in]  Plant4  De vierde plantenpot
#
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

## Door het oproepen van deze functie kan je de robot voor een bepaalde tijd. De duur dat de robot zal rondlopen hangt af van de parameter 'snelheid'
def loopRandomRond():

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

## De robot checkt of er plantenpotten in de buurt staan, en kiest vervolgens de dichtste plant.
# @param[in]  ignorePlant  Dit is het NUMMER van de plant die genegeerd zal worden. Dit is wellicht de plant die de robot net verzet heeft. Door deze nu te negeren zal de robot niet 2 keer op rij dezelfde plant detecteren.
# @param[out]  goToPlant  De robot geeft de dichtstbijzijnde plant terug als argument.
def checkVoorPlanten(ignorePlant):
    minDistance = 1000000
    goToPlant = None

    for plant in bloempottenLijst:
        dist = math.sqrt((robot.x - plant.x) ** 2 + (robot.y - plant.y) ** 2)

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

## Dit laat de robot de plant die hij vast heeft neerzetten.
def placePlant():
    robot.plant.opgepakt = False
    robot.plant = None

## Dit laat de robot de meegegeven plant oppakken.
# @param[in]  plant De plant die opgepakt moet worden.
def pickUpPlant(plant):
    if robot.plant is None or robot.plant is 0:
        robot.plant = plant
        plant.opgepakt =True

## Dit laat de robot de plant die hij vast heeft naar een veilige plaats brengen om neer te zetten. De robot blijft hiervoor willekeurig rond lopen tot de kust veilig is.
def movePlantToSafePlace():
    safe = False
    while not safe:
        loopRandomRond()
        if checkVoorPlanten(robot.plant.nr) is None:
            safe = True
            robot.ignorePlant = robot.plant.nr
        #pygame.time.delay(snelheid)
    placePlant()

## Deze functie zal nagaan of de huidige opstelling van de planten in orde is. Dit door te kijken hoever alle planten van elkaar staan. Als ze allemaal ver genoeg van elkaar staan zal de functie TRUE terugsturen. Anders stuurt het FALSE terug.
# @param[out]  goed  Goed is TRUE als de opstelling in orde is, en FALSE als dit niet het geval is.
def checkPlantenOpstelling():
    goed = True
    for plant1 in bloempottenLijst:
        for plant2 in bloempottenLijst:
            if plant1 is not plant2:
                #Als 2 plantenpotten nog te dicht bij elkaar staan (<250) dan is de opstelling nog niet goed
                if math.sqrt((plant1.x - plant2.x) ** 2 + (plant1.y - plant2.y) ** 2) < 250:
                    goed = False
    return goed

## Deze functie laat de robot naar een bepaalde plant toe rijden.
# @param[in]  plant De plant waar de robot naartoe moet rijden.
def rijdRobotNaarPlant(plant):
    aantalX = abs(robot.x - plant.x)/snelheid
    aantalY = abs(robot.y - plant.y)/snelheid
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

## Deze functie laat de robot een cirkel rijden. Tijdens het rijden van deze cirkel houdt de robot bij welke planten het allemaal gedecteerd heeft. De robot houdt deze planten bij in zijn lijst 'gevondenplanten'.
# @param[in] straal De straal van de cirkel die de robot moet rijden.
def rijCirkelEnMap(straal):
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

## Deze functie laat de robot 90 graden draaien.
def draai90Graden():
    robot.orientation = (robot.orientation + 90)%360
    draw_situation(robot, Plant1, Plant2, Plant3, Plant4)

## Deze functie laat de robot rechtdoor rijden voor een aantal meter. Het aantal meter dat deze robot zal doorrijden hangt af van wat meegegeven is. Welke richting de robot precies vooruit rijdt hangt af van de richting waarin de robot is georienteerd.
# @param[in] meter Het aantal meter dat de robot vooruit dient te rijden.
def rijRechtdoor(meter):
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

## Deze functie wordt enkel opgeroepen als de opstelling in orde is. Ze zorgt voor een correcte afsluiting van de simulatie.
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

pygame.font.init()
font = pygame.font.SysFont('arial', 30)
label = font.render('Druk op enter om de simulatie te starten', 1, (0, 0, 0))
win.blit(label, (200, width/2))
pygame.display.update()

robotImg = pygame.image.load('HA.png')

#Random kiest telkens of de robot een stap achteruit zet, vooruit, of niets doet via deze lijst van operations
operationList = [-1, 0, 1]

#Initialising plantenbakken: voor elke scenario is er een excel voorzien. De excel bevat de info van waar
# de verschillende potten moeten staan
df = pd.read_excel("Scenario3.xlsx")
df_nr = df["Nummer"]
df_x = df["X"]
df_y = df["Y"]


Plant1 = Plant(df_x[0], df_y[0], df_nr[0])
Plant2 = Plant(df_x[1], df_y[1], df_nr[1])
Plant3 = Plant(df_x[2], df_y[2], df_nr[2])
Plant4 = Plant(df_x[3], df_y[3], df_nr[3])
bloempottenLijst = [Plant1,Plant2,Plant3,Plant4]
bloempotImg = pygame.image.load('bloempot.png')

#Startpositie robot
x = height*0.5
y = width*0.5
robot = Robot(x, y)

#Bepaald hoe snel de simulatie verloopt
snelheid = 10

ignorePlant = None
start = False

while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = True

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #TODO: Ingevulde implementatie van het rij rechtdoor-algoritme.
    rijRechtdoor(700)

    gevondenPlant = checkVoorPlanten(robot.plant)
    if gevondenPlant is not None:
        if robot.plant is None:
            rijdRobotNaarPlant(gevondenPlant)
            pickUpPlant(gevondenPlant)
    else:
        if robot.plant is not None:
            placePlant()
    draai90Graden()







    pygame.time.delay(snelheid)
    if checkPlantenOpstelling():
        done = True
        beeindigSpel()