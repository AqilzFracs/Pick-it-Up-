import pygame
import sys
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()

width, height = 600, 400
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Pick it Up!")

#sound
bgsound = pygame.mixer.Sound("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/sound/Soundtrack PickItUp.mp3")
ball_s = pygame.mixer.Sound("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/sound/ball.mp3")

# images
mainmenu_pict = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/PickItUpBG.png")
bg = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/BGPlay.png")
ground = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/Ground.png")
basket = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/Basket.png")
bola = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/ballOri.png")
voli = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/VolleyBall.png")
bomb = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/bomb.png")
pause = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/pause.png")
RingBasket = pygame.image.load("C:/Aqil/Kuliah/Sem 3/Grafkom/Project_Grafkom/img/Ring.png")

# Inisialisasi OpenGL
# glOrtho(0, width, height, 0, -1, 1)         
glOrtho(0, width, height, 0, -1, 1)


# Karakter
ring_size = 70
ring_x = width // 2 - ring_size // 2
ring_y = height - ring_size
ring_speed = 10


# ball
ball_types = [
    {'image': basket, 'size': 30, 'speed': 5, 'is_bomb': False},
    {'image': voli, 'size': 30, 'speed': 5, 'is_bomb': False},
    {'image': bola, 'size': 30, 'speed': 5, 'is_bomb': False},
    {'image': bomb, 'size': 30, 'speed': 5, 'is_bomb': True}
]
num_ball = 5
num_bombs = 2

ball_list = [
    { 
        'type': random.choice(ball_types),
        'x': random.randint(0, width - 30),
        'y': random.randint(-50, 0),  # Koordinat awal di luar layar
        'reset_ball': {'x': random.randint(0, width - 30), 'y': random.randint(-50, 0)}
    } for _ in range(num_ball - num_bombs)
]

for _ in range(num_bombs):
    ball_list.append({
        'type': random.choice(ball_types),
        'x': random.randint(0, width - 30),
        'y': random.randint(-50, 0),
        'reset_ball': {'x': random.randint(0, width - 30), 'y': random.randint(-50, 0)}
    })
# basketBall_size = 30
# basketBall_x = random.randint(0, width - basketBall_size)
# basketBall_y = 400
# basketBall_speed = 5

# footBall_size = 30
# footBall_x = random.randint(0, width - footBall_size)
# footBall_y = 400
# footBall_speed = 5

# volleyBall_size = 30
# volleyBall_x = random.randint(0, width - volleyBall_size)
# volleyBall_y = 400
# volleyBall_speed = 5

# bomb_size = 30
# bomb_x = random.randint(0, width - bomb_size)
# bomb_y = 400
# bomb_speed = 5

# Skor
score = 0
font = pygame.font.SysFont(None, 30)

# nyawa
lives = 5



# ground_scroll = 0
# ground_scroll_x2 = 600
# scroll_speed = 3

def button_MM():
    glPushMatrix()
    glBegin(GL_QUADS)
    glVertex2f(240, 205)
    glVertex2f(240, 255)
    glVertex2f(360, 255)
    glVertex2f(360, 205)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(240, 135)
    glVertex2f(240, 180)
    glVertex2f(360, 180)
    glVertex2f(360, 135)
    glEnd()
    glPopMatrix()
    

def is_button_clicked(x, y, button_x, button_y, button_width, button_height):
    return (
        x >= button_x and
        x <= button_width and
        y >= button_y and
        y <= button_height
    )


def draw_background():
    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex2f(0, 0)

    glTexCoord(1 , 0)
    glVertex2f(width, 0)

    glTexCoord(1, 1)
    glVertex2f(width, height)

    glTexCoord(0, 1)
    glVertex2f(0, height)
    glEnd()

def draw_ground():
    glBegin(GL_QUADS)
    glTexCoord(0, 1)  # Sudut kiri bawah
    glVertex2f(0, 0)

    glTexCoord(1, 1)  # Sudut kiri atas
    glVertex2f(0, 120)

    glTexCoord(1, 0)  # Sudut kanan atas
    glVertex2f(600, 120)

    glTexCoord(0, 0)  # Sudut kanan bawah
    glVertex2f(600, 0)
    glEnd()


def draw_Ball():
    for ball in ball_list:
      image = ball['type']['image']
      size = ball['type']['size']
      glBegin(GL_QUADS)
      glTexCoord(0, 1)
      glVertex2f(ball['x'], ball['y'])

      glTexCoord(1, 1)
      glVertex2f(ball['x'] + size, ball['y'])

      glTexCoord(1, 0)
      glVertex2f(ball['x'] + size, ball['y'] + size)

      glTexCoord(0, 0)
      glVertex2f(ball['x'], ball['y'] +  size)             
      glEnd()


def draw_ring():
    glBegin(GL_QUADS)
    glVertex2f(ring_x, ring_y)
    glVertex2f(ring_x + ring_size, ring_y)
    glVertex2f(ring_x + ring_size, ring_y + ring_size)
    glVertex2f(ring_x, ring_size + ring_size)
    glEnd()


def draw_text(text, x, y): 
    render_text = font.render(text, True, (255, 255, 255))
    pygame.display.get_surface().blit(render_text, (x, y))

def resetgame():
    global ring_x, ball_list, ring_speed, lives
    ring_x = width // 2 - ring_size // 2
    # Tambahan: Atur ulang posisi makanan jika ada
    ball_list = [
      { 
          'type': random.choice(ball_types),
          'x': random.randint(0, width - 30),
          'y': random.randint(400, 450),  # Koordinat awal di luar layar
          'reset_ball': {'x': random.randint(0, width - 30), 'y': random.randint(400, 450)}
      } for _ in range(num_ball - num_bombs)
    ]

    for _ in range(num_bombs):
        ball_list.append({
            'type': random.choice(ball_types),
            'x': random.randint(0, width - 30),
            'y': random.randint(400, 450),
            'reset_ball': {'x': random.randint(0, width - 30), 'y': random.randint(400, 450)}
      })
    if lives == 0:
      lives = 5

clock = pygame.time.Clock()

# bgsound.play()
run = True
show_menu = True
paused = False
start = False

while run:
    # Set frame rate
    clock.tick(60)

    if show_menu:
        menu = True
        screen.blit(mainmenu_pict,(0,0))

    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN and show_menu == True:
            if is_button_clicked(event.pos[0], event.pos[1], 240, 135, 360, 180):
                show_menu = False  # Klik tombol "Start", jadi sembunyikan menu
                volume = 0.2  # Ini akan mengatur volume ke 50%
                bgsound.set_volume(volume)
                bgsound.play()
                start = True
            
            elif is_button_clicked(event.pos[0], event.pos[1], 240, 205, 360, 255):
                pygame.quit()
                quit()
            
    
    if start:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.pause()
                    screen.blit(pause,(0,0))
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and pause == True:
                        if is_button_clicked(event.pos[0], event.pos[1], 240, 135, 360, 180):
                            show_menu = False  # Klik tombol "Start", jadi sembunyikan menu 
                            volume = 0.2  # Ini akan mengatur volume ke 50%
                            bgsound.set_volume(volume)
                            bgsound.play()
                            start = True

                        if is_button_clicked(event.pos[0], event.pos[1], 240, 205, 360, 255):
                            pygame.quit()
                            quit()

        
        if keys[pygame.K_LEFT] and ring_x > 0 and not paused:
            ring_x -= ring_speed
        if keys[pygame.K_RIGHT] and ring_x < width - ring_size and not paused:
            ring_x += ring_speed
        

        screen.blit(bg,(0,0))
        screen.blit(ground,(0, 600))
        screen.blit(ground,(0, 600))

        pygame.time.wait(10)


            
        screen.blit(RingBasket,(ring_x,ring_y))
        # screen.blit(basket,(basketBall_x, basketBall_y))
        for ball in ball_list:
          screen.blit(ball['type']['image'], (ball['x'], ball['y']))



        # Deteksi makanan oleh burung
        for ball in ball_list:
          ball['y'] += ball['type']['speed']
          size = ball['type']['size']
          if not ball['type']['is_bomb']:
              lives -= 1
          elif (
                ball['x'] < ring_x + ring_size and
                ball['x'] + size > ring_x and
                ball['y'] > ring_y + ring_size
                ):
              
              # Burung memakan makanan
              if ball['type']['is_bomb']:
                  lives -+ 1
                  ball['x'], ball['y'] = ball['reset_ball']['x'], ball['reset_ball']['y']
              else:
                  score += 1
                  if score % 10 == 0:
                      for ball in ball_list:
                          ball['type']['speed'] += 2
                  ball['x'], ball['y'] = ball['reset_ball']['x'], ball['reset_ball']['y']

            
    glClear(GL_COLOR_BUFFER_BIT)

    if start == True:
        draw_text(f"Skor    : {score}", 10, 10)
        draw_text(f"Nyawa : {lives}", 10, 30)
        draw_text(f"Speed : {ring_speed}", 10, 50)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(pygame.display.get_surface(), 'RGBA'))
    # draw_ground()
    draw_background()

    glDisable(GL_TEXTURE_2D)

    pygame.display.flip()