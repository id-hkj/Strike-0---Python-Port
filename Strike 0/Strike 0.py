# ©id-hkj 2021

import pygame
pygame.init()

pygame.display.set_icon(pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\favicon.png"))
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Strike 0")

#VARIABLES
ScreenX, ScreenY = win.get_size()
scrollX = 0
scrollY = 0
Block_A_Width = 200
Block_A_Height = 100
Scroll_Speed = 10
Shooting = False
run = True

print(ScreenX)
print(ScreenY)

#IMAGE LOADS/ANIMATION VARS
bg_UNSCALED = pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\Bg.png").convert ()
#Shoot_Animation_Left_UNSCALED = [pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\Hero\ReadyPos_Left.png"), pygame.image.load(r"C:\Program Files\Strike 0\Sprites\Hero\ShootingLift1_Left.png"), pygame.image.load(r"C:\Program Files\Strike 0\Sprites\Hero\ShootingLift2_Left.png"), pygame.image.load(r"C:\Program Files\Strike 0\Sprites\Hero\Lifted_Left.png")]
#Shoot_Animation_Right_UNSCALED = [pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\Hero\ReadyPos_Right.png"), pygame.image.load(r"C:\Program Files\Strike 0\Sprites\Hero\ShootingLift1_Right.png"), pygame.image.load(r"C:\Program Files\Strike 0\Sprites\Hero\ShootingLift2_Right.png"), pygame.image.load(r"C:\Program Files\Strike 0\Sprites\Hero\Lifted_Right.png")]
#Walking_Left_UNSCALED = pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\Hero\ReadyPos_Left.png")
#Walking_Right_UNSCALED = pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\Hero\ReadyPos_Right.png")
Blocks_Set_1_UNSCALED = pygame.image.load(r"C:\Program Files (x86)\Strike 0\Sprites\Blocks\Map_NoScrollY.png").convert_alpha()

#IMAGE SCALINGS
Blocks_Set_1 = pygame.transform.scale(Blocks_Set_1_UNSCALED, (int(ScreenX-((ScreenX//2.663)-ScreenX)), int(ScreenY-((ScreenY//0.648)-ScreenY))))
bg = pygame.transform.scale(bg_UNSCALED, (ScreenX, ScreenY))

Left = False
Right = True
ShootCount = 0
clock = pygame.time.Clock()

#FUNCTIONS
def Drawing():
    #Blocks
    win.blit(bg, (0, 0))
    win.blit(Blocks_Set_1, (scrollX - 30, scrollY + 100))

    pygame.display.update()
    

#MAIN GAME LOOP
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    #KEY PRESSED EVENTS
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_LEFT]:
        scrollX -= Scroll_Speed
    if keys[pygame.K_RIGHT]:
        scrollX += Scroll_Speed
    if keys[pygame.K_UP]:
        scrollY -= Scroll_Speed
    if keys[pygame.K_SPACE]:
        Shooting = True
    Drawing()    
pygame.quit()
