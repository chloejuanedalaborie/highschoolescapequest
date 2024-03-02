import pygame

pygame.init()
fenetre = pygame.display.set_mode((640, 480))

fond = pygame.image.load("plan_lycee.jpg").convert()
fenetre.blit(fond,(0,0))

check = pygame.image.load("check.png").convert_alpha()
mask_check = pygame.mask.from_surface(check)
rect_check = check.get_rect()
rect_check.move_ip(400,300)
fenetre.blit(check, rect_check)

bicheck = pygame.image.load("check.png").convert_alpha()
mask_bicheck = pygame.mask.from_surface(bicheck)
rect_bicheck = bicheck.get_rect()
rect_bicheck.move_ip(400,140)
fenetre.blit(bicheck, rect_bicheck)

main = pygame.image.load("hand.png").convert_alpha()
mask_main = pygame.mask.from_surface(main)
rect_check.move_ip(10,10)
rect_bicheck.move_ip(10,10)
rect_main = main.get_rect()

clock = pygame.time.Clock()
continuer = True


while continuer :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.MOUSEMOTION:
            fenetre.blit(fond, rect_main, rect_main)
            fenetre.blit(check, (400,300))
            fenetre.blit(bicheck, (400, 140))
            rect_main.center = event.pos
            fenetre.blit(main, rect_main)
    
    offset_x = rect_check.x - rect_main.x
    offset_y = rect_check.y - rect_main.y
    if mask_main.overlap(mask_check, (offset_x, offset_y)):
        print("Touché")
    
    else:
        print("")
    
    pygame.display.update()
    clock.tick(40)

pygame.quit()
