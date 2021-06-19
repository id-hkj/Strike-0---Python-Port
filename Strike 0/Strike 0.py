# ©id-hkj 2021

import pygame
import numpy as np #To make the mathematics faster
from PackageStrike0.Maths import ScreenYMath, ScreenXMath
import os

from pygame.constants import WINDOWHIDDEN
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.display.set_icon(pygame.image.load(os.path.join('Sprites', 'favicon.png')))
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Strike 0")

#VARIABLES
SCREENX, SCREENY = win.get_size()
BLOCK_SET_1_WIDTH, BLOCK_SET_1_HEIGHT = ScreenXMath(5115, SCREENX), ScreenYMath(700, SCREENY)

Backdrop = 0
Unlocked = False
scrollX = 0
scrollY = 0
Scroll_Speed = 10
run = True

print(SCREENX)
print(SCREENY)

#IMAGE LOADS/ANIMATION VARS
bg_Gameplay_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'Gameplay.png')).convert()
bg_StartScreen_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'START_SCREEN.png')).convert()

Hero_Left_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Left.png')).convert_alpha()]
Hero_Right_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Right.png')).convert_alpha()]
Blocks_Set_1_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Blocks', 'Map_NoScrollY.png')).convert_alpha()

#IMAGE SCALINGS
Blocks_Set_1 = pygame.transform.scale(Blocks_Set_1_UNSCALED, (BLOCK_SET_1_WIDTH, BLOCK_SET_1_HEIGHT))
bg_Gameplay = pygame.transform.scale(bg_Gameplay_UNSCALED, (SCREENX, SCREENY))
bg_StartScreen = pygame.transform.scale(bg_StartScreen_UNSCALED, (SCREENX, SCREENY))
Hero_Left = []
Hero_Right = []

for i in range(1000):
    if i < 4:
        #0.191
        Hero_Left.append(pygame.transform.scale(Hero_Left_UNSCALED[i], (ScreenXMath(367, SCREENX), ScreenYMath(611, SCREENY))))
        Hero_Right.append(pygame.transform.scale(Hero_Right_UNSCALED[i], (ScreenXMath(367, SCREENX), ScreenYMath(611, SCREENY))))
    else:
        break

clock = pygame.time.Clock()

#OBJECTS
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Right = True
        self.ShootCount = 0
        self.Shooting = False
        self.UpCount = 100
        self.UpAble = False

    def Drawing(self, win, pos):
        self.win = win
        self.pos = pos
        if (Hero.Right == True):
            self.win.blit(Hero_Right[self.pos], (self.x, self.y))
        if (Hero.Right == False):
            self.win.blit(Hero_Left[self.pos], (self.x, self.y))

    def No_Go_Through(self, rectx, recty, rectwidth, rectheight):
        self.rectx = rectx
        self.recty = recty
        self.rectwidth = rectwidth
        self.rectheight = rectheight
        global scrollX

        #PREVENT DOWN
        if (scrollX < self.rectx) and (scrollX > np.subtract(self.rectx, np.subtract(self.rectwidth, 22))):
            if ((self.y < np.add(self.recty, self.rectheight)) and (self.y > self.recty)):
                if self.UpCount == 100:
                    self.y += 15
                    self.UpAble = False
                    self.UpCount = 100
            else:
                self.UpAble = True
        #PREVENT LEFT
        if (scrollX > self.rectx) and (scrollX < np.add(self.rectx, 22)):
            scrollX -= 10
        #PREVENT RIGHT
        else:
            if (scrollX < np.subtract(self.rectx, self.rectwidth)) and (scrollX > np.subtract(np.subtract(self.rectx, self.rectwidth), 22)):
                scrollX += 10
        

class Blocks(object):
    def __init__(self, IMAGE):
        self.IMAGE = IMAGE
    
    def Drawing(self, win, X, Y):
        self.win = win
        self.X = X
        self.Y = Y

        self.win.blit(self.IMAGE, (self.X, self.Y))

class Button(object):
    def __init__(self, x, y, width, height, win):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.EventAble = False
        self.win = win
    
    def Detect_Event(self):
        MouseX, MouseY = pygame.mouse.get_pos()
        
        pygame.draw.rect(self.win, (0, 0, 0), (self.x, self.y, self.width, self.height), width = 4)

        if pygame.mouse.get_pressed()[0] and MouseX >= self.x and MouseX <= (self.width + self.x) and MouseY >= self.y and MouseY <= (self.height + self.y):
            pygame.time.delay(50)
            self.EventAble = True

#SPRITES
Hero = Player(ScreenXMath(303, SCREENX), ScreenYMath(5, SCREENY))
Blocks_1 = Blocks(Blocks_Set_1)
Start = Button(ScreenXMath(74, SCREENX), ScreenYMath(819, SCREENY), ScreenXMath(342, SCREENX), ScreenYMath(104, SCREENY), win)
UpdateLog = Button(ScreenXMath(71, SCREENX), ScreenYMath(931, SCREENY), ScreenXMath(747, SCREENX), ScreenYMath(103, SCREENY), win)
Credits = Button(ScreenXMath(1361, SCREENX), ScreenYMath(818, SCREENY), ScreenXMath(469, SCREENX), ScreenYMath(105, SCREENY), win)
HowToPlay = Button(ScreenXMath(1113, SCREENX), ScreenYMath(933, SCREENY), ScreenXMath(722, SCREENX), ScreenYMath(101, SCREENY), win)

#FUNCTIONS
def Gameplay():
    #Time to make a bunch of GLOBAL variables!
    #HOORAY!

    global Hero
    global scrollX
    global scrollY
    pos = 0
    #Ok, It wasn't that many.

    #BOUNDARIES
    Hero.No_Go_Through(100, 95, 1430, 195)
    Hero.No_Go_Through(100, 95, 1430, 195)
    print(Hero.y)

    #KEY PRESSED EVENTS
    if KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]:
        scrollX += Scroll_Speed
        Hero.Right = False
    if KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
        scrollX -= Scroll_Speed
        Hero.Right = True
    if KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
        if Hero.UpCount == 100 and Hero.UpAble == True:
            Hero.UpCount = 27
    
    if Hero.UpCount <= 27 and Hero.UpCount > 0:
        Hero.y -= 20
        Hero.UpCount -= 1
    else:
        Hero.UpCount = 100
    
    if KEYS[pygame.K_SPACE] and Hero.Shooting == False:
        Hero.Shooting = True
        Hero.ShootCount = 23
    
    if Hero.ShootCount > 0 and Hero.Shooting == True:
        if Hero.ShootCount > 21:
            pos = 1
        elif Hero.ShootCount > 19:
            pos = 2
        elif Hero.ShootCount > 3:
            pos = 3
        elif Hero.ShootCount > 1:
            pos = 2
        elif Hero.ShootCount > 0:
            pos = 1
        else:
            print('ERROR')
        Hero.ShootCount -= 1
    else:
        Hero.Shooting = False
        Hero.ShootCount = 25
        Hero.pos = 0
    
    #DRAWING
    win.blit(bg_Gameplay, (0, 0))

    Blocks_1.Drawing(win, scrollX - int(np.round(np.multiply(BLOCK_SET_1_WIDTH, 0.137))), scrollY + int(np.round(np.multiply(SCREENY, 0.361))))
    Hero.Drawing(win, pos)
    
    pygame.display.update()

def TitleScreen():
    win.blit(bg_StartScreen, (0, 0))
    
    Start.Detect_Event()
    UpdateLog.Detect_Event()
    Credits.Detect_Event()
    HowToPlay.Detect_Event()

    pygame.display.update()
    global Backdrop
    if Start.EventAble == True:
        pygame.time.delay(200)
        Backdrop = 1

#MAIN GAME LOOP
while run:
    clock.tick(27)
    KEYS = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if KEYS[pygame.K_ESCAPE]:
        run = False

    if Backdrop == 1:
        Gameplay()
    elif Backdrop == 0:
        TitleScreen()
    else:
        print('Error 002: BadValue[Scene_NumberState-Invalid]')

pygame.quit()