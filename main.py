import pygame 
import math
import random
from pygame import mixer # Pour musiques

pygame.init()

#Fenetre pour écran
screen = pygame.display.set_mode((800,600)) 

#Background
background = pygame.image.load('misc/background.png')

#Background sound
mixer.music.load("misc/background.wav")
mixer.music.play(-1) # -1 pour avoir une loop

#Fenetre titre avec icône
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('misc/probe.png')
pygame.display.set_icon(icon)

#Joueur
playerImg = pygame.image.load('misc/player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Space Invaders
enemyImg = [] # Liste vide pour plusieurs ennemis
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies): ##Loop selon le nombre d'ennemis
    enemyImg.append(pygame.image.load('misc/spaceinvaders.png')) #On remplace A = B par A.append(B)
    enemyX.append(random.randint(0,736)) #Appel de la fonction random
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4) 
    enemyY_change.append(40) 

#Bullet
bulletImg = pygame.image.load('misc/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10 #Vitesse balle
bullet_state = "ready" #"Ready" -> Invisible // "Fire" -> Mouvement

#Score
score_value=0
font = pygame.font.Font('freesansbold.ttf', 32) ##Police d'écriture (nom police, taille)
textX=10
textY=10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y): ##Afficher score en haut a gauche
    score = font.render("Score : "+ str(score_value), True, (215, 110, 100)) # Couleur du texte
    screen.blit(score, (x,y))
    
def game_over_text(x,y): ##Afficher game_over
    over_text = over_font.render("GAME OVER", True, (215, 110, 100)) # Couleur du texte
    screen.blit(over_text, (200,250))

def player(x,y): #Image sera aux coordonnées x et y, x en abscisse
    screen.blit(playerImg, (x,y))
    
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10)) #Apparaitre au milieu avant du vaisseau
    

# Boucle lancement 
running = True
while running:
    #Remplir page avec RGB ( 0, 0, 0)
    screen.fill((215, 110, 100))
    #background Image
    screen.blit(background, (0,0)) #Va ralentir le programme -> augmenter vitesse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
         # si touche pressée, check direction
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_LEFT:
                playerX_change = -5
             if event.key == pygame.K_RIGHT:
                playerX_change = 5
             if event.key == pygame.K_SPACE:
                 if bullet_state is "ready": #Eviter trop de tirs qui provoquent un bug bullet
                    bullet_sound = mixer.Sound('misc/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX #On sauvegarde position X pour eviter décalage
                    fire_bullet(playerX,bulletY)
                
        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0 #Vitesse retour a position de depart, ici ne bouge pas
                  
    playerX += playerX_change  #Ajouter ou enleve valeur a position       
    #Bordures
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:#Prendre en compte que player est une image de 64x64pixels pour les bordures
        playerX = 736
        
    #mouvements ennemis, avec for in range pour multiples ennemis
    for i in range(num_of_enemies):
        
        #GameOver
        if enemyY[i] > 200: #Game Over si les ennemis atteignent le vaisseau
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200,250)
            break
        
        enemyX[i] += enemyX_change[i]  #Ajouter ou enleve valeur a position       
     #Bordures
        if enemyX[i] <= 0:
          enemyX_change[i] = 4
          enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
          enemyX_change[i] = -4
          enemyY[i] += enemyY_change[i]
          
        #Collision, ici il faut que la balle entre dans la hitbox de l'alien
        if ((((bulletX>=enemyX[i])and(bulletX<=(enemyX[i])+60))and((bulletY>=enemyY[i])and(bulletY<=(enemyY[i])+60)))and(((bulletX+30>=enemyX[i])and(bulletX+30<=(enemyX[i])+60))and((bulletY+30>=enemyY[i])and(bulletY+30<=(enemyY[i])+60)))):
            explosion_sound = mixer.Sound('misc/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            #Respawn ennemi
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
            
        enemy(enemyX[i], enemyY[i], i)
            
    #Mouvement Bullet ( rester visible a l'écran)
    #Tir multiple
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
        
        
    player(playerX, playerY)
    show_score(textX,textY)
    
    pygame.display.update() #Update pour changements