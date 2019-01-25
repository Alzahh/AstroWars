import pygame, random, sys

pygame.init()
pygame.mixer.init()
size = (1000, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(("Astro Wars v3.1"))
bg = pygame.image.load("images/bg.jpg")
menu_bg = pygame.image.load("images/menu_bg.jpg")
im = pygame.image.load("images/im.jpg")
im1 = pygame.image.load("images/im1.jpg")
im2 = pygame.image.load("images/im2.jpg")
im3 = pygame.image.load("images/im3.jpg")
im4 = pygame.image.load("images/im4.jpg")
IMAGE = [im,im1,im2,im3,im4]
text = pygame.Surface((size[0], 30))
i = 0


pygame.mixer.music.load("bg_music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

#Fonts
pygame.font.init()
score_font = pygame.font.SysFont("Comic Sans MS", 24)
inf_font = pygame.font.SysFont("Comic Sans MS", 24, 0, 1)
# Lists
all_sprites_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

punkts = [(70, 140, u"Play", (250, 250, 30), (250, 30, 250), 1),
          (70, 210, u"Exit", (250, 250, 30), (250, 30, 250), 2),
          (70, 280, u"Credits", (250, 250, 30), (250, 30, 250), 3),
          (70, 350, u"Sound", (250, 250, 30), (250, 30, 250), 7)]


def Main():
    player = Player()
    all_sprites_list.add(player)
    clock = pygame.time.Clock()    #fps options
    health = 3
    score = 0
    player.rect.y = 370
    player.rect.x = 15
    n = 0
    r = -1


    gameover_punkts = [(70, 140, u"Play again", (250, 250, 30), (250, 30, 250), 4),
                       (70, 210, u"Menu", (250, 250, 30), (250, 30, 250), 5),
                       (70, 280, u"Exit", (250, 250, 30), (250, 30, 250), 2)]


    gameover = Menu(gameover_punkts)

    pause_punkts = [(70, 140, u"Back to game", (250, 250, 30), (250, 30, 250), 6),
                    (70, 210, u"Menu", (250, 250, 30), (250, 30, 250), 5),
                    (70, 280, u"Sound", (250, 250, 30), (250, 30, 250), 7)]

    pause = Menu(pause_punkts)


    done = False
    # Main loop
    while not done:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                bullet = Bullet()
                bullet.rect.x = player.rect.x + 10
                bullet.rect.y = player.rect.y + 47
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause.menu()

        for enemy in enemy_list.sprites():
            if enemy.rect.x <= 5:
                enemy.rect.x += 1000
                health -= 1
                if health == 0:
                    clean()
                    gameover_punkts.append((750, 550, u"Score: " + str(score), (250, 250, 30), (250, 30, 250), 0))
                    gameover.menu()





        enemy_list.sprites()[0].rect.x -= 10
        enemy_list.sprites()[1].rect.x -= 10
        enemy_list.sprites()[2].rect.x -= 10

        all_sprites_list.update()
        for bullet in bullet_list:
            for enemy in enemy_list.sprites():
                if pygame.sprite.collide_rect(enemy, bullet):

                    enemy.rect.x = random.randrange(size[0], size[0] + 200)
                    enemy.rect.y = random.randrange(30, size[1] - 90)
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)
                    score += 1



            if bullet.rect.x >= size[0]-30:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        text.fill((82, 125, 197))

        #   font render
        text.blit(score_font.render("Score: " + str(score), 1, (255, 0, 0)), (850, 0))
        text.blit(score_font.render("Speed: " + str(round((60 + score / 4) / 60, 2)), 1, (0, 0, 0)), (650, 0))
        text.blit(inf_font.render("Stop all asteroids!", 1, (0, 0, 0)), (0, -6))
        text.blit(inf_font.render("HP: " + str(health), 1, (0, 0, 0)), (500, 0))

        screen.blit(bg, (0, 0))
        screen.blit(text, (0, 0))

        all_sprites_list.draw(screen)
        pygame.display.flip()

        clock.tick(60 + score / 4)

    pygame.quit()
    sys.exit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Hero.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.y = pos[1]


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 25

class Menu:
    def __init__(self, punkts =[120, 140, u"Punkt", (250, 250, 30), (250, 30, 250), 0]):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        paused = True
        done = True
        font_menu = pygame.font.SysFont("Comic Sans MS", 50)

        punkt = 0
        while done:
            screen.blit(menu_bg, (0, 0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 255 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
                    self.render(screen, font_menu, punkt)
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif e.key == pygame.K_p:
                        done = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 1:
                        clean()
                        Main()
                    if punkt == 2:
                        sys.exit()
                    if punkt == 3:
                        game1 = Extra()
                        game1.extra()
                    if punkt == 4:
                        Main()
                    if punkt == 5:
                        game = Menu(punkts)
                        game.menu()
                    if punkt == 6:
                        done = False
                    if punkt == 7:
                        if paused == False:
                            pygame.mixer.music.pause()
                            paused = True
                        else:
                            pygame.mixer.music.unpause()
                            paused = False
            pygame.display.flip()

class Extra:
    def extra(self):
        foto = 0
        done = True
        while done:
            screen.fill((100, 100, 200))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_KP_ENTER or e.key == pygame.K_SPACE :
                        done = False
                    elif e.key == pygame.K_RIGHT:
                        foto += 1
                    elif e.key == pygame.K_LEFT:
                        foto -= 1
                    if foto <= 0:
                        foto = 0
                    elif foto >= 4:
                        foto = 4

            screen.blit(IMAGE[foto], (0, 0))
            screen.blit(screen, (0, 0))
            pygame.display.flip()

def enemy_pack(ammount):
    for i in range(ammount):
        enemy = Enemy("images/Asteroid.png")
        enemy.rect.x = random.randrange(size[0], size[0] + 200)
        enemy.rect.y = random.randrange(30, size[1] - 90)
        enemy_list.add(enemy)
        all_sprites_list.add(enemy)


def clean():
    enemy_list.sprites()[0].rect.x += 1000
    enemy_list.sprites()[1].rect.x += 1000
    enemy_list.sprites()[2].rect.x += 1000

enemy_pack(3)
game = Menu(punkts)
game.menu()


Main()