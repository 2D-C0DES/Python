# setting up the game Lookup
# create the space ship
# lasers of spaceship abd aliens
# create obstacles
# create aliens
# create mystery ship
# check for collisions
# game OverflowErroradd scoring
# add high score
# add sounds and bgm



import pygame
import sys
import random
from game import Game

# this code block is neede before creating the game class
# {
# from spaceship import Spaceship

# this code block is needed before integrating the laser class into the spaceship class
# {
# from laser import Laser
# } 

# from obstacle import Obstacle
# }

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

OFFSET = 50

GREY = (29,29,27)
YELLOW = (243,216,63)


font = pygame.font.Font("c:/Users/Debanjan Das/Desktop/Python/projects/first_repo/font/monogram.ttf", 30)
level_surface = font.render("LEVEL 01",False,YELLOW)
game_over_surface = font.render("GAME OVER" , False,YELLOW)
score_text_surface = font.render("SCORE:",False,YELLOW)
hiscore_text_surface = font.render("HISCORE:",False,YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET,SCREEN_HEIGHT + OFFSET))
pygame.display.set_caption("SPACE INVADERS")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH,SCREEN_HEIGHT,OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER,300)

MYSTERY_SHIP = pygame.USEREVENT +1
pygame.time.set_timer(MYSTERY_SHIP,random.randint(4000,8000))



# this code block is neede before creating the game class
# {
# spaceship = Spaceship(SCREEN_WIDTH,SCREEN_HEIGHT)
# spaceship_group = pygame.sprite.GroupSingle()
# spaceship_group.add(spaceship) 


# this code block is needed before integrating the laser class into the spaceship class
# {
# laser = Laser((100,100),6 , SCREEN_HEIGHT)
# laser2 = Laser((100,200),-6 , SCREEN_HEIGHT)
# lasers_group = pygame.sprite.Group()
# lasers_group.add(laser, laser2)
# }

# obstacle = Obstacle(100,100)
# blocks_group = pygame.sprite.Group()
# }

while True:
    # checking for the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MYSTERY_SHIP and game.run:
            game.create_mysteryship()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()
    

            

        

    # updating
    # spaceship_group.update()
    # blocks_group.update()
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collision()
    

    # drawing screen
    screen.fill(GREY)


    # UI
    pygame.draw.rect(screen, YELLOW, (10, 10, 730,630),2,40)
    pygame.draw.line(screen,YELLOW,(20,605),(730,605),3)

    if game.run:
        screen.blit(level_surface,(610,610,50,50))

    else:
        screen.blit(game_over_surface,(610,610,50,50))
    x = 50
    for  life in range (game.lives):
        screen.blit(game.spaceship_group.sprite.image ,(x,610))
        x += 50


    screen.blit(score_text_surface,(40,15,50,50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score,False,YELLOW)
    screen.blit(score_surface,(110,15,50,50))

    screen.blit(hiscore_text_surface,(550,15,50,50))
    formatted_hiscore = str(game.highscore).zfill(5)
    hiscore_surface = font.render(formatted_hiscore,False,YELLOW)
    screen.blit(hiscore_surface,(640,15,50,50))
    # spaceship_group.draw(screen)
    # spaceship_group.sprite.lasers_group.draw(screen)

    # this code block is needed before integrating the laser class into the spaceship class
    # {
    # lasers_group.draw(screen)
    #  }
    # obstacle.blocks_group.draw(screen)

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)

    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    pygame.display.update()
    clock.tick(60)




