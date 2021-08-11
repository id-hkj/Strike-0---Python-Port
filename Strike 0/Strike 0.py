# ©id-hkj 2021

import pygame
import numpy as np #To make the mathematics faster
import os

pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.display.set_icon(pygame.image.load(os.path.join('Sprites', 'favicon.png')))
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Strike 0")

SCREENX, SCREENY = win.get_size()
DivisorX = SCREENX/1920
DivisorY = SCREENY/1080
print(SCREENX)
print(SCREENY)

#IMAGE LOADS/ANIMATION VARS
bg_Gameplay_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'Gameplay.png')).convert()
bg_StartScreen_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'START_SCREEN.png')).convert()

Hero_Left_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Left.png')).convert_alpha()]
Hero_Right_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Right.png')).convert_alpha()]
Blocks_Set_1_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Blocks', 'Map_NoScrollY.png')).convert_alpha()

#IMAGE SCALINGS
Blocks_Set_1 = pygame.transform.scale(Blocks_Set_1_UNSCALED, (round(5115*DivisorX), round(700*DivisorY)))
bg_Gameplay = pygame.transform.scale(bg_Gameplay_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))
bg_StartScreen = pygame.transform.scale(bg_StartScreen_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))
Hero_Left = []
Hero_Right = []

for i in range(1000):
    if i < 4:
        #0.191
        Hero_Left.append(pygame.transform.scale(Hero_Left_UNSCALED[i], (round(367*DivisorX), round(611*DivisorY))))
        Hero_Right.append(pygame.transform.scale(Hero_Right_UNSCALED[i], (round(367*DivisorX), round(611*DivisorY))))
    else:
        break

#VARIABLES
Backdrop = 0
Unlocked = False
scrollX = 0
scrollY = 0
run = True
clock = pygame.time.Clock()

#OBJECTS
def Rendering(Sprite, Pos, X1920, Y1080, win):
    NewX = X1920*DivisorX
    NewY = Y1080*DivisorY
    
    if Pos == 'N':
        win.blit(Sprite, (NewX, NewY))
    else:
        win.blit(Sprite[Pos], (NewX, NewY))

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
            self.win.blit(Hero_Left[self.pos], (self.x + 60, self.y))


    def No_Go_Through(self, rectx, recty, rectwidth, rectheight, Type):
        self.rectx = rectx
        self.recty = recty
        self.rectwidth = rectwidth
        self.rectheight = rectheight
        global scrollX

        #PREVENT DOWN
        if Type == 'Vertical':
            if (scrollX < self.rectx) and (scrollX > np.subtract(self.rectx, np.subtract(self.rectwidth, -17))):
                if ((self.y < np.add(self.recty, self.rectheight)) and (self.y > self.recty)):
                    if self.UpCount == 100:
                        self.y += 15
                        self.UpAble = False
                        self.UpCount = 100
                else:
                    self.UpAble = True
                global win
                pygame.draw.rect(win, (0, 0, 0), (self.rectx, self.recty, self.rectwidth, self.rectheight), width = 4)
        elif Type == 'Horizontal':
            #PREVENT LEFT
            if (scrollX > self.rectx) and (scrollX < np.add(self.rectx, 22)) and ((self.y > np.subtract(self.recty, 5)) and (self.y < np.add(np.add(self.recty, self.rectheight), 5))):
                scrollX -= 10
            #PREVENT RIGHT
            else:
                if (scrollX < np.subtract(self.rectx, self.rectwidth)) and (scrollX > np.subtract(np.subtract(self.rectx, self.rectwidth), 22)) and ((self.y > np.subtract(self.recty, 5)) and (self.y < np.add(np.add(self.recty, self.rectheight), 5))):
                    scrollX += 10
        else:
            print('Error 400: Bad Input')
    def Checkpoints(self, Checkpoint):
        self.Checkpoint = Checkpoint

        global scrollX
        global scrollY

        if self.Checkpoint == 0:
            scrollX = 0
            self.y = 5
        

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
Hero = Player(303, 5)
Blocks_1 = Blocks(Blocks_Set_1)
Start = Button(round(74*DivisorX), round(819*DivisorY), round(342*DivisorX), round(104*DivisorY), win)
UpdateLog = Button(round(71*DivisorX), round(931*DivisorY), round(747*DivisorX), round(103*DivisorY), win)
Credits = Button(round(1361*DivisorX), round(818*DivisorY), round(469*DivisorX), round(105*DivisorY), win)
HowToPlay = Button(round(1113*DivisorX), round(933*DivisorY), round(722*DivisorX), round(101*DivisorY), win)

#FUNCTIONS
def Gameplay():
    #Time to make a bunch of GLOBAL variables!
    #HOORAY!

    global Hero
    global scrollX
    global scrollY
    global run
    pos = 0
    #Ok, It wasn't that many.
    
    #FOr Y Scaling, it is JumpChange*(NumberThere/20)
    #BOUNDARIES
    
    #Vertical is done LEFT to RIGHT
    Hero.No_Go_Through(10_000_000, -10_000_000, 9_998_700, 10_002_000, 'Vertical')
    Hero.No_Go_Through(1290, -10_000_000, 2350, 10_000_290, 'Vertical')
    Hero.No_Go_Through(-1075, -10_000_000, 105, 10_002_000, 'Vertical')
    Hero.No_Go_Through(-1190, -10_000_000, 150, 10_000_290, 'Vertical')
    Hero.No_Go_Through(-1355, -10_000_000, 400, 10_000_095, 'Vertical')
    Hero.No_Go_Through(-1740, -10_000_000, 365, 9_999_790, 'Vertical')
    Hero.No_Go_Through(-2115, -10_000_000, 445, 10_000_290, 'Vertical')
    Hero.No_Go_Through(-2575, -10_000_000, 125, 10_002_000, 'Vertical')
    Hero.No_Go_Through(-2715, -10_000_000, 1245, 10_000_290, 'Vertical')
    Hero.No_Go_Through(-3975, -10_000_000, 10_000_000, 10_002_000, 'Vertical')

    #Horizontal is done Top To Bottom, then Left to Right

    Hero.No_Go_Through(10_000_000, -205, 10_001_750, 300, 'Horizontal')
    Hero.No_Go_Through(-2110, -205, 10_000_000, 495, 'Horizontal')
    Hero.No_Go_Through(10_000_000, 95, 10_001_340, 200, 'Horizontal')
    Hero.No_Go_Through(10_000_000, 290, 9_998_700, 200, 'Horizontal')
    Hero.No_Go_Through(-1085, 290, 90, 200, 'Horizontal')
    Hero.No_Go_Through(-2585, 290, 120, 200, 'Horizontal')
    Hero.No_Go_Through(-3985, 290, 10_000_000, 200, 'Horizontal')

    #KEY PRESSED EVENTS
    if KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]:
        scrollX += 10
        Hero.Right = False
    if KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
        scrollX -= 10
        Hero.Right = True
    if KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
        if Hero.UpCount == 100 and Hero.UpAble == True:
            Hero.UpCount = 27
    
    if Hero.UpCount <= 27 and Hero.UpCount > 0:
        Hero.y -= 15
        Hero.UpCount -= 1
    else:
        Hero.UpCount = 100
    
    if KEYS[pygame.K_SPACE] and Hero.Shooting == False:
        Hero.Shooting = True
        Hero.ShootCount = 23

    if Hero.y > 480:
        Hero.Checkpoints(0)
    
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
    Rendering(bg_Gameplay, 'N', 0, 0, win)
    Rendering(Blocks_Set_1, 'N', scrollX - 700, scrollY + 390, win)
    if Hero.Right == False:
        Rendering(Hero_Right, pos, Hero.x, Hero.y, win)
    else:
        Rendering(Hero_Left, pos, Hero.x + 60, Hero.y, win)
    #win.blit(bg_Gameplay, (0, 0))
    #Blocks_1.Drawing(win, scrollX - 700, scrollY + 390)
    #Hero.Drawing(win, pos)
    
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
