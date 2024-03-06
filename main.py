import pygame
pygame.init()

mouse_position = pygame.mouse.get_pos()

pygame.display.set_caption("High School Escape Quest")
fenetre = pygame.display.set_mode((600, 600))

fond = pygame.image.load("screen1.PNG").convert()
fenetre.blit(fond,(0,0))

plan_lycee = pygame.image.load("plan_lycee.png").convert()

play = pygame.image.load("jouer.png").convert_alpha()
play = pygame.transform.scale(play, (100,100)) #modifie la taille de l'image
mask_play = pygame.mask.from_surface(play)
rect_play = play.get_rect()
rect_play.move_ip(250,450)
fenetre.blit(play, rect_play)


main = pygame.image.load("hand.png").convert_alpha()
main = pygame.transform.scale(main, (50,50))
mask_main = pygame.mask.from_surface(main)
rect_play.move_ip(10,10)
rect_main = main.get_rect()

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
            if rect_play.collidepoint(event.pos):
                play = pygame.Surface(rect_play.size) #rend le play transparent
                play.set_alpha(0) #rend le carré noir du rect_play transparent
                    
                fond = plan_lycee
                fenetre.blit(fond,(0,0))
                
                memo = pygame.image.load("zone.png").convert_alpha()
                mask_memo = pygame.mask.from_surface(memo)
                rect_memo = memo.get_rect()
                rect_memo.move_ip(0,50)
                
                morpion = pygame.image.load("zone.png").convert_alpha()
                play = pygame.transform.scale(play, (193,289))
                mask_morpion = pygame.mask.from_surface(morpion)
                rect_morpion = morpion.get_rect()
                rect_morpion.move_ip(0,311)


                quiz = pygame.image.load("zone.png").convert_alpha()
                play = pygame.transform.scale(play, (235,350))
                mask_quiz = pygame.mask.from_surface(quiz)
                rect_quiz = quiz.get_rect()
                rect_quiz.move_ip(365,250)
                
            elif fond == plan_lycee and rect_memo.collidepoint(event.pos):
                    
                fond = pygame.image.load("plan_classe.jpg").convert()
                fenetre.blit(fond,(0,0))
            
            elif fond == plan_lycee and rect_morpion.collidepoint(event.pos):
                    
                fond = pygame.image.load("plan_classe.jpg").convert()
                fenetre.blit(fond,(0,0))
            
            elif fond == plan_lycee and rect_quiz.collidepoint(event.pos):
                    
                fond = pygame.image.load("plan_classe.jpg").convert()
                fenetre.blit(fond,(0,0))
                    
                        
        
    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(40)

pygame.quit()
