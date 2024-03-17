#!/usr/bin/env python3

import pygame
import random
import time

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
            # lorsque le bouton gauche de la souris est appuyé sur la surface rectangulaire du play
            # alors le fond change et le play disparait
            if pygame.mouse.get_pressed()[0] and rect_play.collidepoint(event.pos):
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
            if pygame.mouse.get_pressed()[0] and zone_cliquable_mémo.collidepoint(event.pos):
                affiche_écran = jeu_mémo
            elif pygame.mouse.get_pressed()[0] and zone_cliquable_morpion.collidepoint(event.pos):
                affiche_écran = jeu_morpion
            elif pygame.mouse.get_pressed()[0] and zone_cliquable_quiz.collidepoint(event.pos):
                affiche_écran = jeu_quiz

def init_mémo():
    # Dimensions des cases du mémo
    RECT_WIDTH = 70
    RECT_HEIGHT = 90
    GAP = 30  # Espace entre les rectangles

    # Calcul total de l'espace horizontal et vertical
    total_width = 4 * (RECT_WIDTH + GAP) - GAP        
    total_height = 4 * (RECT_HEIGHT + GAP) - GAP 

    # Position du coin supérieur gauche de la zone des rectangle
    start_x = (550 - total_width) // 2
    start_y = (700 - total_height) // 2

    # Création des cases du mémo
    global rectangles
    rectangles = []
    for ligne in range(3):
        for colonne in range(4):
            rect = pygame.Rect(start_x + (RECT_WIDTH + GAP) * colonne + GAP, start_y + (RECT_HEIGHT + GAP) * ligne + GAP, RECT_WIDTH, RECT_HEIGHT)
            rectangles.append({'rectangle': rect, 'image_index': None, 'clicked': False})

    # Attribution aléatoire des images aux rectangles
    index_images_disponibles = list(range(6)) * 2
    for rect_info in rectangles:
        rect_info['image_index'] = index_images_disponibles.pop(random.randint(0, len(index_images_disponibles)-1))    
    
    global cliquées
    cliquées = []    
    global resultats
    resultats = []
                        
def jeu_mémo():
    fond = pygame.image.load("./images/salle_memo.png").convert()
    fenetre.blit(fond,(0,0))

    # par défaut, toutes les images sont cachées
    cases_blanches = [rect for rect in rectangles + resultats + cliquées if rect not in resultats]
    for rect_info in cases_blanches:
        rect_surf = pygame.Surface(rect_info['rectangle'].size)
        rect_surf.fill(WHITE)
        fenetre.blit(rect_surf, rect_info['rectangle'])    
    
    # on affiche les images déjà trouvées
    for rect_info in resultats + cliquées:
        index = rect_info['image_index'] + 1
        image = pygame.image.load(f'./images/mémo/card_{index}.jpeg')
        image = pygame.transform.scale(image, (70, 90))
        fenetre.blit(image, rect_info['rectangle'])

    if len(cliquées) == 2:
        print('compare '+str(cliquées[0])+' à '+str(cliquées[1]))
        if cliquées[0]['image_index'] != cliquées[1]['image_index']:
            # la paire cliquée est fausse
            for rect_2 in rectangles:
                if rect_2['image_index'] == rect_info['image_index']:
                    rect_2['clicked'] = False
        else:
            print('match')
            resultats.extend(cliquées)
        cliquées.clear()
       
    
    gérer_curseur()
    
    # on vérifie si toutes les cases ont été retournées
    # resultats contient les paires qui ont été validées
    if (len(resultats) != len(rectangles)) :
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect_info in rectangles:
                    # si la case est cliquée on affiche l'image et on met 'clicked' à True
                    if pygame.mouse.get_pressed()[0] and rect_info['rectangle'].collidepoint(event.pos):
                        rect_info['clicked'] = not rect_info['clicked']
                        if rect_info['clicked']:
                            if rect_info not in cliquées:
                                cliquées.append(rect_info)

    else:
        print('memo complet')                            
    

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
    pygame.mouse.set_visible(False)
    fenetre.blit(curseur, rect_curseur)

def gérer_event_quit():
    global continuer
    for event in pygame.event.get():
        
        # Quitter le jeu
        if event.type == pygame.QUIT:
            continuer = False
            
clock = pygame.time.Clock()

init_mémo()

affiche_écran = start
continuer = True
while continuer :

    gérer_event_quit()
    
    affiche_écran()
                        
    pygame.display.update()
    clock.tick(40)

pygame.quit()
