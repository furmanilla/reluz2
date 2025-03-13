import random
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (40, 40))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.velocity = 0  
        self.gravity = 0.3  
        self.jump_power = -5  

    def update(self):
        keys = key.get_pressed()

        if keys[K_SPACE] and self.rect.y > 5:  
            self.velocity = self.jump_power  

       
        self.velocity += self.gravity
        self.rect.y += self.velocity

       
        if self.rect.y > win_height - 40:  
            self.rect.y = win_height - 40
            self.velocity = 0  

        if self.rect.y < 0:  
            self.rect.y = 0
            self.velocity = 0  

class Wall(sprite.Sprite):
    def __init__(self, wall_x, hole_height, top_image, bottom_image):
        super().__init__()
        self.hole_height = hole_height
        self.top_wall = transform.scale(image.load(top_image), (50, random.randint(100, win_height - hole_height)))
        self.bottom_wall = transform.scale(image.load(bottom_image), (50, win_height - hole_height - self.top_wall.get_height()))
        self.top_rect = self.top_wall.get_rect(topleft=(wall_x, 0))
        self.bottom_rect = self.bottom_wall.get_rect(topleft=(wall_x, self.top_rect.height + hole_height))

    def update(self):
 
        self.top_rect.x -= 2
        self.bottom_rect.x -= 2
      
        if self.top_rect.x < -50:
            self.top_rect.x = win_width
            self.bottom_rect.x = win_width
            self.top_wall = transform.scale(image.load("pipedown.png"), (50, random.randint(100, win_height - self.hole_height)))
            self.bottom_wall = transform.scale(image.load("pipeup.png"), (50, win_height - self.hole_height - self.top_wall.get_height()))
            self.bottom_rect.y = self.top_rect.height + self.hole_height

    def draw_wall(self, window):
        window.blit(self.top_wall, self.top_rect)
        window.blit(self.bottom_wall, self.bottom_rect)

def check_collisions(player, walls):
    for wall in walls:
        if player.rect.colliderect(wall.top_rect) or player.rect.colliderect(wall.bottom_rect):
            return True
    return False

def restart_game():
    global player, walls

    player.rect.x = 50
    player.rect.y = win_height // 5
    player.velocity = 0  
    walls = []
    hole_height = 150
    for i in range(5):
        wall = Wall(win_width + i * 300, hole_height, "pipedown.png", "pipeup.png")
        walls.append(wall)

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Flappy Bird')
background = transform.scale(image.load("bg.png"), (win_width, win_height))


player = Player('birdup.png', 50, win_height // 5, 5)


walls = []
hole_height = 150
for i in range(5):
    wall = Wall(win_width + i * 300, hole_height, "pipedown.png", "pipeup.png")
    walls.append(wall)


game = True
game_over = False

while game: 
    for e in event.get():
        if e.type == QUIT:
            game = False
       
    window.blit(background, (0, 0))
    
    if not game_over:
        player.update()  # Оновлюємо позицію птаха
        if check_collisions(player, walls):  
            game_over = True  
        player.reset(window)

        for wall in walls:
            wall.update()  
            wall.draw_wall(window)

    display.update()

quit()
