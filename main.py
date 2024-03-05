import pygame
pygame.init()

pygame.display.set_caption("High School Escape Quest")
fenetre = pygame.display.set_mode((600, 600))

fond = pygame.image.load("screen1.PNG").convert()
fenetre.blit(fond,(0,0))

play = pygame.image.load("jouer.png").convert_alpha()
play = pygame.transform.scale(play, (100,100))
mask_play = pygame.mask.from_surface(play)
rect_play = play.get_rect()
rect_play.move_ip(250,450)
fenetre.blit(play, rect_play)


main = pygame.image.load("hand.png").convert_alpha()
main = pygame.transform.scale(main, (50,50))
mask_main = pygame.mask.from_surface(main)
rect_play.move_ip(10,10)
rect_main = main.get_rect()

rect_surf = pygame.Surface(rect_play.size).set_alpha(0) #zone cliquable du play acceuil

clock = pygame.time.Clock()
continuer = True


while continuer :
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
            
        elif event.type == pygame.MOUSEMOTION:
            fenetre.blit(fond, rect_main, rect_main)
            fenetre.blit(play, (250,450))
            rect_main.center = event.pos
            fenetre.blit(main, rect_main)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #lorsque le clique de la souris est appuyé sur la surface rectangulaire du play, alors le fond change et le play disparait
            if event.button == 1: # 1= clique gauche
                if rect_play.collidepoint(event.pos):
                    fond = pygame.image.load("plan_lycee.png").convert()
                    fenetre.blit(fond,(0,0))                    
                    play = pygame.Surface(rect_play.size) #rend le play transparent
                    play.set_alpha(0) #rend le carré noir du rect_play transparent
                    
                                
                        
    
    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(40)

pygame.quit()