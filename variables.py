# Variables pour maintenir l'état de la navigation dans le jeu
START_STATE = 'start'
MENU_STATE = 'menu'
MEMORY_STATE = 'memory'
TIC_TAC_TOE_STATE = 'tic_tac_toe'
QUIZ_STATE = 'quiz'
END_STATE = 'game_over'

state = START_STATE

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Backgrounds
MENU_BACKGROUND_IMAGE = "./images/plan_lycee.png"
MEMORY_BACKGROUND_IMAGE = "./images/salle_memo.png"
TICTACTOE_BACKGROUND_IMAGE = "./images/salle_morpion.png"
QUIZ_BACKGROUND_IMAGE = "./images/salle_quiz.png"

# Fonts
GAME_FONTS = "./fonts/retro-gaming-fonts.ttf"

# Hauteur de la score-barre
SCORE_BARRE_HEIGHT = 50

MAX_LIVES = 3
livesCount = MAX_LIVES