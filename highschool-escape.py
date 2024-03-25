#!/usr/bin/env python3

import pygame
import sys
import variables, outils, menu, memory, quiz, tictactoe

start_button_rect = pygame.Rect(252, 450, 100, 100)

def start_screen():
    # Affiche la page d'accueil du jeu
    fond = pygame.image.load("./images/title.png").convert()
    fond = pygame.transform.scale(fond, (variables.WINDOW_WIDTH, variables.WINDOW_HEIGHT))

    fenetre.blit(fond, (0, 0))

    # Charger l'image du bouton  
    start_button_image = pygame.image.load('./images/bouton_play.png').convert_alpha()
    start_button_image = pygame.transform.scale(start_button_image, (start_button_rect.width, start_button_rect.height))

    # Blitter le bouton sur l'écran
    fenetre.blit(start_button_image, start_button_rect)

def gestion_events():
    for event in pygame.event.get():
        # Quitter le jeu
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gestion du clic
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # écran d'accueil
            if variables.state == variables.START_STATE and start_button_rect.collidepoint(event.pos):
                    variables.state = variables.MENU_STATE
            # écran menu
            elif variables.state == variables.MENU_STATE:
                menu.events(event.pos)
            elif variables.state == variables.MEMORY_STATE:
                memory.events(event.pos)
            elif variables.state == variables.TIC_TAC_TOE_STATE:
                tictactoe.events(event.pos)
            elif variables.state == variables.QUIZ_STATE:
                quiz.events(event.pos)

def gestion_display():
        # On affiche les différents écran du jeux en fonction de l'état de "state"
        if variables.state == variables.START_STATE:
            start_screen()
        elif variables.state == variables.MENU_STATE:
            menu.screen()
        elif variables.state == variables.MEMORY_STATE:
            memory.screen()
        elif variables.state == variables.TIC_TAC_TOE_STATE:
            tictactoe.screen()
        elif variables.state == variables.QUIZ_STATE:
            quiz.screen()
        elif variables.state == variables.END_STATE:
            pass

if __name__ == "__main__":

    # Initialise PyGame
    pygame.init()
    clock = pygame.time.Clock()

    # Initialise le mixer pour la musique et les sons
    pygame.mixer.init()

    pygame.mixer.music.load('./musics/password-infinity-123276.mp3')
    pygame.mixer.music.play()

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((variables.WINDOW_WIDTH, variables.WINDOW_HEIGHT))
    pygame.display.set_caption("High School Escape Quest")


    # Main game loop
    while True:
        gestion_events()

        gestion_display()

        outils.afficher_curseur()

        pygame.display.update()
        clock.tick(60)