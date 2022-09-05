import pygame 
import math
import random
from pygame.locals import *

pygame.init()

#Fenetre pour écran
screen = pygame.display.set_mode((800,600)) 

#Background
background = pygame.image.load('misc/background.png')

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
enemyImg = pygame.image.load('misc/spaceinvaders.png')
enemyX = random.randint(0,736)#Appel de la fonction random
enemyY = random.randint(50,150)
enemyX_change = 4
enemyY_change = 40

#Bullet
bulletImg = pygame.image.load('misc/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10 #Vitesse balle
bullet_state = "ready" #"Ready" -> Invisible // "Fire" -> Mouvement

score = 0
def player(x,y): #Image sera aux coordonnées x et y, x en abscisse
    screen.blit(playerImg, (x,y)) #Dessiner à appeler dans la loop pour toujours apparaitre
    
def enemy(x,y):
    screen.blit(enemyImg, (x,y))
    
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
        
    #mouvements ennemis
    enemyX += enemyX_change  #Ajouter ou enleve valeur a position       
    #Bordures
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change
        
    #Mouvement Bullet ( rester visible a l'écran)
    #Tir multiple
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
        
        #Collision
        if (((bulletX>=enemyX)and(bulletX<=enemyX+50))and((bulletY>=enemyY)and(bulletY<=enemyY+50))):
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            #Respawn ennemi
            enemyX = random.randint(0,736)
            enemyY = random.randint(50,150)
            
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update() #Update pour changements