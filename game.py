import pygame
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

pygame.init()
window = pygame.Window(size =(WINDOW_WIDTH, WINDOW_HEIGHT), title = "First Game", position = (50, 50))
screen = window.get_surface()
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
running = True
dt = 0
x_scroll = 0
default_cat = pygame.image.load(os.path.join('sprites', 'cat.png')).convert_alpha()
walking_left_frames = [pygame.image.load(os.path.join('sprites', 'cat.png')),
                       pygame.image.load(os.path.join('sprites', 'cat-first step left.png')),
                       pygame.image.load(os.path.join('sprites', 'cat-second step left.png')),
                       pygame.image.load(os.path.join('sprites', 'cat-third step left.png'))]
walking_right_frames = [pygame.image.load(os.path.join('sprites', 'cat.png')),
                        pygame.image.load(os.path.join('sprites', 'cat-first step right.png')),
                        pygame.image.load(os.path.join('sprites', 'cat-second step right.png')),
                        pygame.image.load(os.path.join('sprites', 'cat-third step right.png'))]

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('sprites', 'cat.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = 300
        self.speed = 400
        self.jump = 70
        self.is_on_floor = False
        self.against_platform = False
        self.is_animating = False
        self.gravity = 0.8
        self.final_velocity = 16
        self.velocity_y = 0
        self.current_frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.4
        self.health = 5

    def update(self):
        self.move()
        if not self.is_animating:
            self.image = default_cat

    def move(self):
        old_rect_y = self.rect.y
        old_rect_x = self.rect.x
        
        self.velocity_y += self.gravity * dt

        if self.velocity_y >= self.final_velocity:
            self.velocity_y = self.final_velocity

        if self.is_on_floor:
            self.velocity_y = 0
            self.rect.y = old_rect_y

        self.rect.y += self.velocity_y

        keys = pygame.key.get_pressed()  
        if keys[pygame.K_LEFT]: 
            self.is_animating = True
            self.rect.x -= self.speed * dt
            self.animation_timer += dt       
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0  
                self.current_frame_index += 1  
                if self.current_frame_index >= len(walking_left_frames):
                    self.current_frame_index = 0
                self.image = walking_left_frames[self.current_frame_index] 
        if keys[pygame.K_RIGHT]:
            self.is_animating = True
            self.rect.x += self.speed * dt
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0  
                self.current_frame_index += 1  
                if self.current_frame_index >= len(walking_right_frames):
                    self.current_frame_index = 0
                self.image = walking_right_frames[self.current_frame_index]
        if keys[pygame.K_UP] and self.is_on_floor:
            self.rect.y -= 4000 * dt

        if self.against_platform:
            self.rect.x = old_rect_x

    def check_in_bounds(self):
        if self.rect.y > 1300:
            return False
        else:
            return True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('sprites', 'floor.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.originalx = x
        self.originaly = y

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('sprites', 'box.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.originalx = x
        self.originaly = y
        self.timer = 0

    def crumble(self, dt):
        self.timer += dt

        if self.timer >= 0.3:
            self.image = pygame.image.load(os.path.join('sprites', 'box break 1.png')).convert_alpha()
        if self.timer >= 0.6:
            self.image = pygame.image.load(os.path.join('sprites', 'box break 2.png')).convert_alpha()
        if self.timer >= 0.9:
            self.kill()

class Pond(pygame.sprite.Sprite):
    def __init__(self, x, y):
            super().__init__()
            self.image = pygame.image.load(os.path.join('sprites', 'pond.png')).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

platform0 = Platform(0, 400)
platform1 = Platform(platform0.rect.x + platform0.rect.width, 400)
platform2 = Platform(platform1.rect.x + platform1.rect.width, 400)
platform3 = Platform(300, 500)
platform4 = Platform(platform3.rect.x + platform3.rect.width, 500)
box0 = Box(400, 500 - platform4.rect.height)
platform5 = Platform(platform4.rect.x + platform4.rect.width, 500)
platform6 = Platform(550, 580)
platform7 = Platform(platform6.rect.x + platform6.rect.width, 580)
box1 = Box(platform7.rect.x + platform7.rect.width, 580)
platform8 = Platform(850, 500)
pond0 = Platform(platform8.rect.x + platform8.rect.width, 500)
cat = Cat()

platforms = pygame.sprite.Group()
boxes = pygame.sprite.Group()
ponds = pygame.sprite.Group()
player = pygame.sprite.Group()
platforms.add(platform0)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)
platforms.add(platform4)
platforms.add(platform5)
platforms.add(platform6)
platforms.add(platform7)
platforms.add(platform8)
boxes.add(box0)
boxes.add(box1)
player.add(cat)

first_screen = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    previous_x_scroll = x_scroll

    if cat.rect.x >= (WINDOW_WIDTH / 2):
        x_scroll = cat.rect.x - (WINDOW_WIDTH / 2)
        
    heart_image = pygame.image.load(os.path.join('sprites', 'heart.png'))
    heart_rect = heart_image.get_rect()
    for heart in range(0, cat.health):
        width = heart_rect.width
        height = heart_rect.height
        y = 50
        x = heart * 20
        screen.blit(heart_image, pygame.Rect(x, y, width, height))

    if pygame.sprite.spritecollideany(cat, platforms):
        cat.is_on_floor = True
    else:
        cat.is_on_floor = False

    if pygame.sprite.spritecollideany(cat, boxes):
        collided_boxes = pygame.sprite.spritecollide(cat, boxes, False)
        for box in collided_boxes:
            cat.is_on_floor = True
            box.crumble(dt)

    if not cat.check_in_bounds():
        running = False
        
    screen.fill((153, 219, 232))
    player.update()
    player.draw(screen)
    if previous_x_scroll != x_scroll:
        for object in platforms:
            object.rect.x = object.originalx - x_scroll
        for box in boxes:
            box.rect.x = box.originalx - x_scroll
    platforms.draw(screen)
    boxes.draw(screen)
    window.flip()
    dt = clock.tick(60) / 1000.0

pygame.quit()


