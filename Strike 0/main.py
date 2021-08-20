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
bg_Title_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'Title.png')).convert()
bg_Starting_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'Starting.png')).convert()
bg_Credits_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'Credits.png')).convert()
bg_HowToPlay_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Backdrops', 'HowToPlay.png')).convert()

Hero_Left_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Left.png')).convert_alpha()]
Hero_Right_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Right.png')).convert_alpha()]
Blocks_Set_1_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Blocks', 'Map_NoScrollY.png')).convert_alpha()
Bullet_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Game_Other', 'Bullet.png')).convert_alpha()

#IMAGE SCALINGS
bg_Gameplay = pygame.transform.scale(bg_Gameplay_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))
bg_Title = pygame.transform.scale(bg_Title_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))
bg_Starting = pygame.transform.scale(bg_Starting_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))
bg_Credits = pygame.transform.scale(bg_Credits_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))
bg_HowToPlay = pygame.transform.scale(bg_HowToPlay_UNSCALED, (round(1920*DivisorX), round(1080*DivisorY)))

Blocks_Set_1 = pygame.transform.scale(Blocks_Set_1_UNSCALED, (round(5115*DivisorX), round(700*DivisorY)))
Bullet = pygame.transform.scale(Bullet_UNSCALED, (round(21*DivisorX), round(31*DivisorY)))
Hero_Left = []
Hero_Right = []

for i in range(1000):
    if i < 4:
        #0.191
        Hero_Left.append(pygame.transform.scale(Hero_Left_UNSCALED[i], (round(367*DivisorX), round(611*DivisorY))))
        Hero_Right.append(pygame.transform.scale(Hero_Right_UNSCALED[i], (round(367*DivisorX), round(611*DivisorY))))
    else:
        break

del(bg_Gameplay_UNSCALED, bg_Title_UNSCALED, Hero_Left_UNSCALED, Hero_Right_UNSCALED, Blocks_Set_1_UNSCALED, Bullet_UNSCALED, bg_Starting_UNSCALED, bg_Credits_UNSCALED, bg_HowToPlay_UNSCALED)

#VARIABLES
Backdrop = 'Title'
Unlocked = False
scrollX = 0
scrollY = 0
run = True
clock = pygame.time.Clock()
BulletCount = -5
BulletY = 0

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
        self.BulletX = 0
        self.BulletCount = -5
        self.BulletY = 0
        self.BulletDirection = 'Left'
        self.Bullet_Shooing = False
        self.Bullet_Speed = 0
        self.SaveScrollX = 0

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

    def Bullet(self, scrolling):
        if self.BulletCount == 150:
            self.SaveScrollX = scrollX
            if Hero.Right == True:
                self.BulletDirection = 'Right'
            else:
                self.BulletDirection = 'Left'

        self.SaveScrollX = scrollX

        if self.Bullet_Shooing == True:
            if self.BulletDirection == 'Right':
                if self.BulletCount == 150:
                    self.BulletY = self.y + 310
                    self.BulletX = 570
                    self.BulletCount -= 1
                
                self.BulletX = Hero.BulletX + scrollX - scrolling + 15

                if self.BulletX > (1920*DivisorX):
                    self.Bullet_Shooing = False
                else:
                    self.Bullet_Shooing = True
            else:
                if self.BulletCount == 150:
                    self.BulletY = self.y + 310
                    self.BulletX = 380
                    self.BulletCount -= 1

                self.BulletX -= 10

                if self.BulletX < (-30*DivisorX):
                    self.Bullet_Shooing = False
                else:
                    self.Bullet_Shooing = True            
        else:
            self.BulletX = -50
            self.BulletY = -50
            self.BulletCount = -5

        
        

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
StartGame = Button(round(1582*DivisorX), round(938*DivisorY), round(312*DivisorX), round(113*DivisorY), win)
BackTitle = Button(round(32*DivisorX), round(938*DivisorY), round(288*DivisorX), round(113*DivisorY), win)

#FUNCTIONS
def Gameplay():
    #Time to make a bunch of GLOBAL variables!
    #HOORAY!

    global Hero
    global scrollX
    global scrollY
    global run
    global BulletCount
    global BulletY
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
        Hero.Bullet_Speed = 20
        Hero.Right = False
    elif KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
        scrollX -= 10
        Hero.Bullet_Speed = 5
        Hero.Right = True
    else:
        Hero.Bullet_Speed = 10
    if KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
        if Hero.UpCount == 100 and Hero.UpAble == True:
            Hero.UpCount = 27
    
    if Hero.UpCount <= 27 and Hero.UpCount > 0:
        Hero.y -= 15
        Hero.UpCount -= 1
    else:
        Hero.UpCount = 100
    
    if KEYS[pygame.K_SPACE] and Hero.Shooting == False:
        Hero.ShootCount = 23

    if Hero.y > 480:
        Hero.Checkpoints(0)
    
    if Hero.ShootCount > 0:
        if Hero.ShootCount > 21:
            pos = 1
        elif Hero.ShootCount > 19:
            pos = 2
            if Hero.Bullet_Shooing == False:
                Hero.Bullet_Shooing = True
                Hero.BulletCount = 150
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
        Hero.ShootCount = -8
        Hero.pos = 0

    
    Hero.Bullet(Hero.SaveScrollX)
    
    #DRAWING
    Rendering(bg_Gameplay, 'N', 0, 0, win)
    Rendering(Blocks_Set_1, 'N', scrollX - 700, scrollY + 390, win)
    if Hero.Right == True:
        Rendering(Hero_Right, pos, Hero.x, Hero.y, win)
        Rendering(Bullet, 'N', Hero.BulletX, Hero.BulletY, win)
    else:
        Rendering(Hero_Left, pos, Hero.x + 60, Hero.y, win)
        Rendering(Bullet, 'N', Hero.BulletX, Hero.BulletY, win)

    pygame.display.update()

def TitleScreen():
    global Start
    global UpdateLog
    global Credits
    global HowToPlay

    Rendering(bg_Title, 'N', 0, 0, win)
    Start.Detect_Event()
    UpdateLog.Detect_Event()
    Credits.Detect_Event()
    HowToPlay.Detect_Event()

    pygame.display.update()

    global Backdrop
    if Start.EventAble == True:
        pygame.time.delay(200)
        Backdrop = 'PreStart'
        Start.EventAble = False

    elif UpdateLog.EventAble == True:
        UpdateLog.EventAble = False
    
    elif Credits.EventAble == True:
        Backdrop = 'Credits'
        Credits.EventAble = False
    
    elif HowToPlay.EventAble == True:
        Backdrop = 'HowToPlay'
        HowToPlay.EventAble = False



def Starting():
    global StartGame
    global BackTitle

    Rendering(bg_Starting, 'N', 0, 0, win)
    StartGame.Detect_Event()
    BackTitle.Detect_Event()
    pygame.display.update()

    global Backdrop
    if StartGame.EventAble == True:
        Backdrop = 'Game'
        StartGame.EventAble = False
    
    if BackTitle.EventAble == True:
        Backdrop = 'Title'
        BackTitle.EventAble = False

def Credits_Game():
    global BackTitle

    Rendering(bg_Credits, 'N', 0, 0, win)
    BackTitle.Detect_Event()
    pygame.display.update()

    global Backdrop    
    if BackTitle.EventAble == True:
        Backdrop = 'Title'
        BackTitle.EventAble = False

def HowToPlaySCREEN():
    global BackTitle

    Rendering(bg_HowToPlay, 'N', 0, 0, win)
    BackTitle.Detect_Event()
    pygame.display.update()

    global Backdrop    
    if BackTitle.EventAble == True:
        Backdrop = 'Title'
        BackTitle.EventAble = False

#MAIN GAME LOOP
while run:
    clock.tick(27)
    KEYS = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if KEYS[pygame.K_ESCAPE]:
        run = False

    if Backdrop == 'Game':
        Gameplay()
    elif Backdrop == 'PreStart':
        Starting()
    elif Backdrop == 'Title':
        TitleScreen()
    elif Backdrop == 'Credits':
        Credits_Game()
    elif Backdrop == 'HowToPlay':
        HowToPlaySCREEN()
    else:
        print('Error 002: BadValue[Scene_NumberState-Invalid]')

pygame.quit()