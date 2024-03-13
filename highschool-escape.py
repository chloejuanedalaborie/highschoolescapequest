#!/usr/bin/env python3

import pygame
import random

# Définition des couleurs
WHITE = (255, 255, 255)

# Définition de la taille de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

pygame.init()

# Titre du Jeux
pygame.display.set_caption("High School Escape Quest")

# Fenêtre principale
fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def start():
    # Variable globale qui sert à affecter les différents écrans du jeu
    global affiche_écran
    
    fond = pygame.image.load("./images/menu.png").convert()
    fenetre.blit(fond,(0,0))

    # Bouton play
    play = pygame.image.load("./images/bouton_play.png").convert_alpha()
    play = pygame.transform.scale(play, (100,100)) # Modifie la taille de l'image
    pygame.mask.from_surface(play)
    rect_play = play.get_rect() # Forme un rectangle autour du bouton play
    rect_play.move_ip(250,450)
    fenetre.blit(play, rect_play)
    
    gérer_curseur()   

    for event in pygame.event.get():
        # Le bouton play est cliqué
        if event.type == pygame.MOUSEBUTTONDOWN:
            # lorsque le clique de la souris est appuyé sur la surface rectangulaire du play
            # alors le fond change et le play disparait
            if rect_play.collidepoint(event.pos):
                play = pygame.Surface(rect_play.size) #rend le play transparent
                play.set_alpha(0) #rend le carré noir du rect_play transparent
                affiche_écran = menu    

def menu():
    global affiche_écran
    fond = pygame.image.load("./images/plan_lycee.png").convert()
    fenetre.blit(fond,(0,0))

    # zone de clic pour le jeu 'memo'
    zone_cliquable_mémo = pygame.Rect(0,50,193,256)
    surface_mémo = pygame.Surface(zone_cliquable_mémo.size)
    surface_mémo.set_alpha(0)
    fenetre.blit(surface_mémo, zone_cliquable_mémo)
    
    # zone de clic pour le jeu 'morpion'
    zone_cliquable_morpion = pygame.Rect(0,311,193,289)
    surface_morpion = pygame.Surface(zone_cliquable_morpion.size)
    surface_morpion.set_alpha(0)
    fenetre.blit(surface_morpion, zone_cliquable_morpion)
    
    # zone de clic pour le jeu 'quiz'
    zone_cliquable_quiz = pygame.Rect(365,250,235,350)
    surface_quiz = pygame.Surface(zone_cliquable_quiz.size)
    surface_quiz.set_alpha(0)
    fenetre.blit(surface_quiz, zone_cliquable_quiz)
    
    gérer_curseur()
    
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if zone_cliquable_mémo.collidepoint(event.pos):
                affiche_écran = jeu_mémo
            elif zone_cliquable_morpion.collidepoint(event.pos):
                affiche_écran = jeu_morpion
            elif zone_cliquable_quiz.collidepoint(event.pos):
                affiche_écran = jeu_quiz
                
def jeu_mémo():
    fond = pygame.image.load("./images/salle_memo.png").convert()
    fenetre.blit(fond,(0,0))
    
    # Chargement des images du mémo
    memo = []
    for i in range(1, 7):
        image = pygame.image.load(f'./images/mémo/card_{i}.jpeg')
        image = pygame.transform.scale(image, (70, 90))  # Redimensionner l'image
        image.set_alpha(0) # Rendre l'image transparente par défaut
        memo.append(image)

    # Dimensions des cases du mémo
    RECT_WIDTH = 70
    RECT_HEIGHT = 90
    GAP = 30  # Espace entre les rectangles

    #calcul total de l'espace horizontal et vertical
    total_width = 4 * (RECT_WIDTH + GAP) - GAP        
    total_height = 4 * (RECT_HEIGHT + GAP) - GAP 

    #position du coin supérieur gauche de la zone des rectangle
    start_x = (550 - total_width) // 2
    start_y = (700 - total_height) // 2

    # Création des cases du mémo
    rectangles = []
    for ligne in range(3):
        for colonne in range(4):
            rect = pygame.Rect(start_x + (RECT_WIDTH + GAP) * colonne + GAP, start_y + (RECT_HEIGHT + GAP) * ligne + GAP, RECT_WIDTH, RECT_HEIGHT)
            rect_surf = pygame.Surface(rect.size)
            rect_surf.fill(WHITE)
            fenetre.blit(rect_surf, rect)
            rectangles.append({'rectangle': rect, 'image_index': None, 'clicked': False})

    # Attribution aléatoire des images aux rectangles
    index_images_disponibles = list(range(len(memo))) * 2
    for rect_info in rectangles:
        rect_info['image_index'] = index_images_disponibles.pop(random.randint(0, len(index_images_disponibles)-1))    
        fenetre.blit(memo[rect_info['image_index']], rect_info['rectangle'])  # Afficher l'image (transparente à ce stage)  
    
    gérer_curseur()
    """ jeu_terminé = False
    while not jeu_terminé:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect_info in rectangles:
                    if rect_info['rectangle'].collidepoint(event.pos):

                        memo[rect_info['image_index']].set_alpha(None)

                        rect_info['clicked'] = not rect_info['clicked']  # Inverser l'état du clic """

def jeu_morpion():
    fond = pygame.image.load("./images/salle_morpion.png").convert()
    fenetre.blit(fond,(0,0))
    
    gérer_curseur() 
    
def jeu_quiz():
    fond = pygame.image.load("./images/salle_quiz.png").convert()
    fenetre.blit(fond,(0,0))
    
    gérer_curseur() 
                
def gérer_curseur():
    curseur = pygame.image.load("./images/curseur.png").convert_alpha()
    curseur = pygame.transform.scale(curseur, (50,50))
    rect_curseur = curseur.get_rect()
    rect_curseur.center = pygame.mouse.get_pos()
    fenetre.blit(curseur, rect_curseur)

def gérer_event_quit():
    global continuer
    for event in pygame.event.get():
        
        # Quitter le jeu
        if event.type == pygame.QUIT:
            continuer = False
            
clock = pygame.time.Clock()

affiche_écran = start
continuer = True
while continuer :

    gérer_event_quit()
    
    affiche_écran()
                        
    pygame.display.update()
    clock.tick(40)

pygame.quit()
