# ©id-hkj 2021

import pygame
import os
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.display.set_icon(pygame.image.load(os.path.join('Sprites', 'favicon.png')))
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Strike 0")

#VARIABLES
SCREENX, SCREENY = win.get_size()
BLOCK_SET_1_WIDTH, BLOCK_SET_1_HEIGHT = int(2.664*SCREENX), int(SCREENY * 0.648)

Backdrop = 1
Unlocked = False
scrollX = 0
scrollY = 0
Scroll_Speed = 10
Shooting = False
run = True

print(SCREENX)
print(SCREENY)


#IMAGE LOADS/ANIMATION VARS
bg_Gameplay_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Bg.png')).convert()
Hero_Left_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Left.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Left.png')).convert_alpha, pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Left.png')).convert_alpha, pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Left.png')).convert_alpha()]
Hero_Right_UNSCALED = [pygame.image.load(os.path.join('Sprites', 'Hero', 'ReadyPos_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift1_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'ShootingLift2_Right.png')).convert_alpha(), pygame.image.load(os.path.join('Sprites', 'Hero', 'Lifted_Right.png')).convert_alpha()]
Blocks_Set_1_UNSCALED = pygame.image.load(os.path.join('Sprites', 'Blocks', 'Map_NoScrollY.png')).convert_alpha()

#IMAGE SCALINGS
Blocks_Set_1 = pygame.transform.scale(Blocks_Set_1_UNSCALED, (BLOCK_SET_1_WIDTH, BLOCK_SET_1_HEIGHT))
bg_Gameplay = pygame.transform.scale(bg_Gameplay_UNSCALED, (SCREENX, SCREENY))


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
    def Drawing(self, win):
        self.win = win
        #Blocks
        self.win.blit(Blocks_Set_1, (scrollX - int(BLOCK_SET_1_WIDTH * 0.137), scrollY + int(SCREENY * 0.361)))
        #Hero
        if (Hero.Right == True):
            self.win.blit(Hero_Right_UNSCALED[0], (Hero.x, Hero.y))
        if (Hero.Right == False):
            self.win.blit(Hero_Left_UNSCALED[0], (Hero.x, Hero.y))

#SPRITES
Hero = Player(int(SCREENX*0.28038), 0)

#FUNCTIONS
def Gameplay():
    #Time to make a bunch of GLOBAL variables!
    #HOORAY!

    global Hero
    global scrollX
    global scrollY

    #Ok, It wasn't that many.

    #BOUNDARIES
    if Hero.y <= 200 and Hero.UpCount == 100:
        Hero.y += 10

    #KEY PRESSED EVENTS
    if KEYS[pygame.K_LEFT]:
        scrollX += Scroll_Speed
        Hero.Right = False
    if KEYS[pygame.K_RIGHT]:
        scrollX -= Scroll_Speed
        Hero.Right = True
    if KEYS[pygame.K_UP] and Hero.UpCount == 100:
        Hero.UpCount = 25
    
    if Hero.UpCount <= 25 and Hero.UpCount > -25:
        if Hero.UpCount <= 0:
            neg = -1
        else:
            neg = 1
        Hero.y -= (10 * neg)
        Hero.UpCount -= 1
    else:
        Hero.UpCount = 100
    
    if KEYS[pygame.K_SPACE] and Hero.Shooting == False:
        Hero.Shooting = True

    win.blit(bg_Gameplay, (0, 0))
    Hero.Drawing(win)
    pygame.display.update()

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
    else:
        print('Error 002: BadValue[Scene_NumberState-Invalid]')

pygame.quit()
