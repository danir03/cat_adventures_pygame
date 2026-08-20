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
        self.jump = 100
        self.is_on_floor = False
        self.against_platform = False
        self.is_animating = False
        self.gravity = 0.8
        self.final_velocity = 16
        self.velocity_y = 0
        self.current_frame_index = 0
        self.animation_timer = 100
        self.animation_speed = 0.4
        self.health = 5

    def update(self):
        self.move()
        if not self.is_animating:
            self.image = default_cat

    def move(self):
        self.velocity_y += self.gravity * dt
        if self.velocity_y >= self.final_velocity:
            self.velocity_y = self.final_velocity
        
        old_rect_y = self.rect.y
        old_rect_x = self.rect.x

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
        if keys[pygame.K_UP]:
            self.rect.y -= self.jump * dt

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

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('sprites', 'box.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0

    def crumble(self, dt):
        self.timer += dt

        if self.timer >= 0.3:
            self.image = pygame.image.load(os.path.join('sprites', 'box break 1.png')).convert_alpha()
        if self.timer >= 0.6:
            self.image = pygame.image.load(os.path.join('sprites', 'box break 2.png')).convert_alpha()
        if self.timer >= 0.9:
            self.kill()

platform0 = Platform(0, 400)
platform1 = Platform(64, 400)
platform2 = Platform(128, 400)
platform3 = Platform(300, 500)
platform4 = Platform(372, 500)
platform5 = Platform(444, 500)
platform6 = Platform(520, 580)
box0 = Box(400, 468)
cat = Cat()

platforms = pygame.sprite.Group()
boxes = pygame.sprite.Group()
player = pygame.sprite.Group()
platforms.add(platform0)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)
platforms.add(platform4)
platforms.add(platform5)
platforms.add(platform6)
boxes.add(box0)
player.add(cat)

first_screen = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                cat.is_animating = False

    for heart in range(0, cat.health):
        heart_image = pygame.image.load(os.path.join('sprites', 'heart.png'))
        heart_rect = heart_image.get_rect()
        heart_rect.y = 50
        heart_rect.x = heart * 20
        screen.blit(heart_image, heart_rect)

    if pygame.sprite.spritecollideany(cat, platforms):
        elements = pygame.sprite.spritecollide(cat, platforms, False)
        for platform in elements:
            # checking for collisions with floor
            if cat.rect.bottom <= platform.rect.top + 10:
                cat.rect.bottom = platform.rect.top             
                cat.is_on_floor = True
            if cat.rect.top >= platform.rect.bottom - 10:
                cat.rect.top = platform.rect.bottom
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
    for object in platforms:
        object.rect.x -= x_scroll
    platforms.draw(screen)
    boxes.draw(screen)
    window.flip()
    dt = clock.tick(60) / 1000.0

pygame.quit()


