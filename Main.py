__author__ = 'fillan'
from Calculation import *
import pygame
import time


def convert2d(p):  # One point
    z = p.z
    if z <= 0:
        z = 1
    return xScreenSize * p.x/(2 * z) + (xScreenSize / 2), yScreenSize * p.y/(2 * z) + (yScreenSize / 2)


def draw(w, engine, time):
    pygame.draw.rect(window, (0, 0, 0), (0, 0, xScreenSize, yScreenSize), 0)
    for i in viewSpace:
        for j in i.modelSpace:
            Go = 0
            for k in j.indexList:
                p = i.pointList[k]
                if p.z <= 0:
                    Go += 1
            if Go <= 1:
                p1 = convert2d(i.pointList[j.indexList[0]])
                p2 = convert2d(i.pointList[j.indexList[1]])
                p3 = convert2d(i.pointList[j.indexList[2]])
                pygame.draw.polygon(w, j.Color, [p1, p2, p3], 0)
    velocity = myPhysics.calculate_velocity()
    print_text('Speed = ' + str(velocity), 10, 10)
    print_text('Engine', 10, 80)
    print_text('Score', 10, 130)
    print_text(str(time), 10, 140)
    pygame.draw.rect(window, (0, 255, 0), (10, 100, 100 * engine, 20), 0)
    pygame.draw.rect(window, (255, 0, 0), (10, 100, 100, 20), 1)
    pygame.draw.circle(window, (0, 0, 255), (30, 50), 20, 1)
    pygame.draw.circle(window, (255, 0, 0), (xScreenSize // 2, yScreenSize // 2), 20, 1)
    angle = -3 * math.pi / 4 + math.pi * velocity / 20
    pygame.draw.line(window, (255, 0, 0), (30, 70), (30 + 30 * math.cos(angle), 70 + 30 * math.sin(angle)), 3)
    pygame.display.flip()


def print_text(text, x, y):
    myfont = pygame.font.SysFont(None, 17)
    label = myfont.render(text, True, (255, 255, 255), (10, 10, 10))
    window.blit(label, (x, y))
pygame.init()
try:
    f = open("Score.txt")
    highScore = 0
    for line in f:
        highScore = int(line)
    f.close()
except IOError:
    highScore = 0
print("Use arrow keys to move.  Use 1 and 2 to control the engine")
Running = True
xScreenSize = 700
yScreenSize = 700
Clock = pygame.time.Clock()
window = pygame.display.set_mode((xScreenSize, yScreenSize))
pygame.display.set_caption("Fillan's Graphics Engine")
viewSpace = []
lightSource = Point(0, 0, -1000)
viewSpace.append(Ground(lightSource))  # Ground must always be first
viewSpace.append(Cube(Point(-50, 0, 500), Point(50, 100, 50), (200, 100, 100), lightSource))
viewSpace.append(Cube(Point(0, 0, 300), Point(50, 100, 50), (100, 200, 100), lightSource))
viewSpace.append(Cube(Point(-25, 0, 400), Point(50, 100, 50), (100, 100, 200), lightSource))
myPhysics = Physics(Point(0, 0, 1))
myCalculation = Calculation(viewSpace, myPhysics)
myKeyboard = Keyboard()
Engine = 0
Time = 0
while Running:
    Time += 1
    Clock.tick(20)
    if False:  # Crash logic
        if Time > highScore:
            highScore = Time
        pygame.draw.rect(window, (0,0,0), (0, 0, xScreenSize, yScreenSize), 0)
        print_text("CRASH", xScreenSize / 2 - 10, yScreenSize / 2)
        print_text("Score = " + str(Time), xScreenSize / 2 - 20, yScreenSize / 2 + 30)
        print_text("High Score = " + str(highScore), xScreenSize / 2 - 30, yScreenSize / 2 + 60)
        pygame.display.flip()
        f = open("Score.txt", 'w+')
        f.write(str(highScore))
        f.close()
        time.sleep(2)
        Running = False
    draw(window, Engine, Time)
    myCalculation.reset()
    if myKeyboard.uDown:
        myCalculation.create_total(1, 0, 0, .01)
    if myKeyboard.dDown:
        myCalculation.create_total(1, 0, 0, -.01)
    if myKeyboard.rDown:
        myCalculation.create_total(0, 0, 1, .01)
    if myKeyboard.lDown:
        myCalculation.create_total(0, 0, 1, -.01)
    if myKeyboard.twoDown:
        Engine += .1
    if myKeyboard.oneDown:
        Engine -= .1
    if Engine < 0:
        Engine = 0
    if Engine > 1:
        Engine = 1
    myPhysics.update_engine(Engine)
    viewSpace = myCalculation.rotate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                myKeyboard.uDown = True
            if event.key == pygame.K_DOWN:
                myKeyboard.dDown = True
            if event.key == pygame.K_RIGHT:
                myKeyboard.rDown = True
            if event.key == pygame.K_LEFT:
                myKeyboard.lDown = True
            if event.key == pygame.K_1:
                myKeyboard.oneDown = True
            if event.key == pygame.K_2:
                myKeyboard.twoDown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                myKeyboard.uDown = False
            if event.key == pygame.K_DOWN:
                myKeyboard.dDown = False
            if event.key == pygame.K_RIGHT:
                myKeyboard.rDown = False
            if event.key == pygame.K_LEFT:
                myKeyboard.lDown = False
            if event.key == pygame.K_1:
                myKeyboard.oneDown = False
            if event.key == pygame.K_2:
                myKeyboard.twoDown = False