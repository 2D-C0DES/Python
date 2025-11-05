import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self,type,x,y):
        super().__init__()
        self.type = type
        path = f"c:/Users/Debanjan Das/Desktop/Python/projects/first_repo/Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x,y))
        self.aliens_group = pygame.sprite.Group()


    def update(self,direction):
        self.rect.x += direction


#  mystery ship creation

class MysteryShip(pygame.sprite.Sprite):
    def __init__(self,screen_width,offset):
        super().__init__()
        self.offset = offset
        self.screen_width = screen_width
        self.image = pygame.image.load("c:/Users/Debanjan Das/Desktop/Python/projects/first_repo/Graphics/mystery.png")


        x = random.choice([self.offset/2,self.screen_width + self.offset - self.image.get_width()])

        if x == self.offset/2:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft = (x,50))

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < self.offset/2:
            self.kill()
        elif self.rect.right > self.screen_width + self.offset/2:
            self.kill()