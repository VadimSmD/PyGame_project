import pygame
import sys
import os

FPS = 60
cost = 5
making_tower = False
making_auto = False
making_flame = False
making_health = False
spawned_ids = []
time = 0
weapons = []
dead_enemies = []
dead_ids = []
existing_enemies = []
possible_coords = []
fire = []
for i in range(195, 1281):
    possible_coords.append(i)
wining_mass = [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410,
               420, 430, 440, 450, 460, 470, 480, 490, 500]


def write_a_word(x, y, word, f_type, size):
    font = pygame.font.Font(f_type, size)
    start = font.render(word, 1, pygame.Color('white'))
    rect = start.get_rect()
    rect.top = y
    rect.x = x
    screen.blit(start, rect)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def update_damage():
    global total_health
    to_delete_weapons = []
    to_delete_enemies = []
    for e in range(len(existing_enemies)):
        if existing_enemies[e][0] <= 193:
            total_health -= existing_enemies[e][3]
            to_delete_enemies.append(e)
    for example in to_delete_enemies:
        dead_ids.append(spawned_ids[example])
        existing_enemies.remove(existing_enemies[example])
        spawned_ids.remove(spawned_ids[example])

    for w in range(len(weapons)):
        to_delete_enemies = []
        for e in range(len(existing_enemies)):
            if existing_enemies[e][3] <= 0:
                to_delete_enemies.append(e)

        for e in range(len(existing_enemies)):
            if abs(weapons[w][0] - existing_enemies[e][0]) <= weapons[w][5]:
                existing_enemies[e][3] -= (weapons[w][3] / 60)
                break
        for e in range(len(existing_enemies)):
            if existing_enemies[e][0] >= weapons[w][0] and existing_enemies[e][0] <= weapons[w][0] + 100:
                weapons[w][4] -= existing_enemies[e][3]
                if e not in to_delete_enemies:
                    to_delete_enemies.append(e)
        for example in to_delete_enemies:
            dead_ids.append(spawned_ids[example])
            existing_enemies.remove(existing_enemies[example])
            spawned_ids.remove(spawned_ids[example])
    for w in range(len(weapons)):
        if weapons[w][4] <= 0:
            to_delete_weapons.append(w)
    for example_weapon in to_delete_weapons:
        weapons.remove(weapons[example_weapon])


def mass_in_mass(mass1, mass2):
    count = 0
    for el in mass1:
        if el in mass2:
            count += 1
    if count == len(mass1):
        return True
    else:
        return False


def shoot_sometimes_or_whatever(t):
    global fire
    for w in range(len(weapons)):
        any_enemy_in_r = False
        back = False
        front = True
        cooldown = True
        for e in range(len(existing_enemies)):
            if abs(weapons[w][0] - existing_enemies[e][0]) <= weapons[w][5]:
                any_enemy_in_r = True
                if weapons[w][0] > existing_enemies[e][0]:
                    back = True
                    front = False
                break
        if any_enemy_in_r and t - weapons[w][7] >= weapons[w][6]:
            cooldown = False
            weapons[w][7] = t
        if any_enemy_in_r and not cooldown:
            if front:
                if weapons[w][2] == 'tower':
                    fire.append([(weapons[w][0] + 50, 290), 'tower_fire.png', (0, 0, 0), (20, 20), t])
                elif weapons[w][2] == 'auto':
                    fire.append([(weapons[w][0] + 55, 320), 'tower_fire.png', (0, 0, 0), (20, 20), t])
                elif weapons[w][2] == 'flame':
                    fire.append([(weapons[w][0] + 50, 322), 'flame_fire.png', (0, 0, 0), (20, 20), t])
                elif weapons[w][2] == 'health':
                    fire.append([(weapons[w][0] + 55, 330), 'health_boom.png', (255, 255, 255), (20, 20), t])
                cooldown = True
            elif back:
                if weapons[w][2] == 'tower':
                    fire.append([(weapons[w][0], 280), 'back_tower_fire.png', (0, 0, 0), (20, 20), t])
                elif weapons[w][2] == 'auto':
                    fire.append([(weapons[w][0] + 55, 320), 'back_tower_fire.png', (0, 0, 0), (20, 20), t])
                elif weapons[w][2] == 'flame':
                    fire.append([(weapons[w][0] + 50, 322), 'back_flame_fire.png', (0, 0, 0), (20, 20), t])
                elif weapons[w][2] == 'health':
                    fire.append([(weapons[w][0] + 55, 330), 'health_boom.png', (255, 255, 255), (20, 20), t])
                cooldown = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, dif, name, health, shields, armor, spawn_time, current_time, speed_coef):
        pygame.sprite.Sprite.__init__(self)
        if spawn_time not in dead_ids:
            self.id = spawn_time
            self.char = health * (armor / 400) + shields
            if dif == 'Easy':
                self.char = self.char * 0.75
            elif dif == 'Normal':
                pass
            elif dif == ' Hard':
                self.char = self.char * 1.25
            self.coordinate = 1280
            if spawn_time == int(current_time) and self.id not in spawned_ids:
                self.spawn(name)

            if spawn_time < current_time:
                self.coordinate = 1280 - speed_coef * (current_time - spawn_time)
                index = spawned_ids.index(self.id)
                existing_enemies[index][0] = int(self.coordinate)

    def spawn(self, name):
        existing_enemies.append([self.coordinate, 325, name, self.char])
        spawned_ids.append(self.id)


class Making_sniper(pygame.sprite.Sprite):
    def __init__(self, event, dif):
        global making_tower
        pygame.sprite.Sprite.__init__(self)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sniper_x = event.pos[0]
            self.sniper_y = event.pos[1]
            if self.sniper_x >= 195 and self.sniper_x <= 1280 and self.sniper_y <= 380 and self.sniper_y >= 280:
                making_tower = False
                count = 0
                for i in range(self.sniper_x, self.sniper_x + 101):
                    if i in possible_coords:
                        count += 1
                if count == 101:
                    l.amount -= 40
                    k.amount -= 50
                    m.amount -= 20
                    if dif == 'Easy':
                        damage = 100
                    elif dif == 'Normal':
                        damage = 75
                    elif dif == 'Hard':
                        damage = 50
                    weapons.append([self.sniper_x, 280, 'tower', damage, 400, 200, 1, 0])
                    for i in range(self.sniper_x, self.sniper_x + 101):
                        possible_coords.remove(i)


class Making_auto(pygame.sprite.Sprite):
    def __init__(self, event, dif):
        global making_auto
        pygame.sprite.Sprite.__init__(self)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sniper_x = event.pos[0]
            self.sniper_y = event.pos[1]
            if self.sniper_x >= 195 and self.sniper_x <= 1280 and self.sniper_y <= 380 and self.sniper_y >= 280:
                making_auto = False
                count = 0
                for i in range(self.sniper_x, self.sniper_x + 101):
                    if i in possible_coords:
                        count += 1
                if count == 101:
                    l.amount -= 20
                    k.amount -= 50
                    m.amount -= 50
                    if dif == 'Easy':
                        damage = 20
                    elif dif == 'Normal':
                        damage = 15
                    elif dif == 'Hard':
                        damage = 12
                    weapons.append([self.sniper_x, 280, 'auto', damage, 500, 170, 0.3, 0])
                    for i in range(self.sniper_x, self.sniper_x + 101):
                        possible_coords.remove(i)


class Making_flame(pygame.sprite.Sprite):
    def __init__(self, event, dif):
        global making_flame
        pygame.sprite.Sprite.__init__(self)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sniper_x = event.pos[0]
            self.sniper_y = event.pos[1]
            if self.sniper_x >= 195 and self.sniper_x <= 1280 and self.sniper_y <= 380 and self.sniper_y >= 280:
                making_flame = False
                count = 0
                for i in range(self.sniper_x, self.sniper_x + 101):
                    if i in possible_coords:
                        count += 1
                if count == 101:
                    l.amount -= 0
                    k.amount -= 50
                    m.amount -= 50
                    if dif == 'Easy':
                        damage = 10
                    elif dif == 'Normal':
                        damage = 12
                    elif dif == 'Hard':
                        damage = 15
                    weapons.append([self.sniper_x, 280, 'flame', damage, 350, 150, 0.1, 0])
                    for i in range(self.sniper_x, self.sniper_x + 101):
                        possible_coords.remove(i)


class Making_health(pygame.sprite.Sprite):
    def __init__(self, event, dif):
        global making_health
        pygame.sprite.Sprite.__init__(self)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sniper_x = event.pos[0]
            self.sniper_y = event.pos[1]
            if self.sniper_x >= 195 and self.sniper_x <= 1280 and self.sniper_y <= 380 and self.sniper_y >= 280:
                making_health = False
                count = 0
                for i in range(self.sniper_x, self.sniper_x + 101):
                    if i in possible_coords:
                        count += 1
                if count == 101:
                    l.amount -= 10
                    k.amount -= 50
                    m.amount -= 80
                    if dif == 'Easy':
                        damage = 200
                    elif dif == 'Normal':
                        damage = 175
                    elif dif == 'Hard':
                        damage = 150
                    weapons.append([self.sniper_x, 280, 'health', damage, 550, 200, 2, 0])
                    for i in range(self.sniper_x, self.sniper_x + 101):
                        possible_coords.remove(i)


class Update_button(pygame.sprite.Sprite):
    def __init__(self, event, name, location, dif):
        pygame.sprite.Sprite.__init__(self)
        self.main = load_image(name, (255, 255, 255))
        self.main = pygame.transform.scale(self.main, (100, 100))
        self.rect = self.main.get_rect()
        self.rect.left, self.rect.top = location
        screen.blit(self.main, self.rect)
        write_a_word(25, 550, 'Улучшить производство', None, 30)
        write_a_word(25, 575, 'нужно ' + str(cost) + ' всех ресурсов', None, 30)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.x = event.pos[0]
            self.y = event.pos[1]
            if self.x >= 50 and self.x <= 150 and self.y >= 600 and self.y <= 700:
                if l.amount >= cost and k.amount >= cost and m.amount >= cost:
                    l.amount -= cost
                    k.amount -= cost
                    m.amount -= cost
                    self.up(dif)

    def up(self, dif):
        global cost
        cost = cost * 3
        if dif == 'Easy':
            coeff = 1
        elif dif == 'Normal':
            coeff = 0.5
        elif dif == 'Hard':
            coeff = 0.2
        l.speed += l.speed * coeff
        k.speed += k.speed * coeff
        m.speed += m.speed * coeff


class Make_weapon(pygame.sprite.Sprite):
    def __init__(self, dif, event):
        global making_tower, making_auto, making_flame, making_health
        pygame.sprite.Sprite.__init__(self)
        self.main = load_image('tower.png')
        self.main = pygame.transform.scale(self.main, (100, 100))
        self.rect = self.main.get_rect()
        self.rect.left, self.rect.top = 350, 600
        screen.blit(self.main, self.rect)
        write_a_word(325, 550, 'Создать башню снайпера', None, 30)
        write_a_word(325, 575, '(40 л, 50 к, 20 м)', None, 30)

        self.main = load_image('auto.png')
        self.main = pygame.transform.scale(self.main, (100, 100))
        self.rect = self.main.get_rect()
        self.rect.left, self.rect.top = 625, 600
        screen.blit(self.main, self.rect)
        write_a_word(600, 550, 'Создать пулемёт', None, 30)
        write_a_word(600, 575, '(20 л, 50 к, 50 м)', None, 30)

        self.main = load_image('flame.png', (0, 0, 0))
        self.main = pygame.transform.scale(self.main, (100, 100))
        self.rect = self.main.get_rect()
        self.rect.left, self.rect.top = 875, 600
        screen.blit(self.main, self.rect)
        write_a_word(850, 550, 'Создать огнемёт', None, 30)
        write_a_word(850, 575, '(0 л, 50 к, 50 м)', None, 30)

        self.main = load_image('health.png', (0, 0, 0))
        self.main = pygame.transform.scale(self.main, (100, 100))
        self.rect = self.main.get_rect()
        self.rect.left, self.rect.top = 1100, 600
        screen.blit(self.main, self.rect)
        write_a_word(1100, 550, 'Создать пушку', None, 30)
        write_a_word(1100, 575, '(10 л, 50 к, 80 м)', None, 30)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.x = event.pos[0]
            self.y = event.pos[1]
            if self.x >= 350 and self.x <= 450 and self.y >= 600 and self.y <= 700:
                if l.amount >= 40 and k.amount >= 50 and m.amount >= 20:
                    making_tower = True
            elif self.x >= 625 and self.x <= 725 and self.y >= 600 and self.y <= 700:
                if l.amount >= 20 and k.amount >= 50 and m.amount >= 50:
                    making_auto = True
            elif self.x >= 875 and self.x <= 975 and self.y >= 600 and self.y <= 700:
                if l.amount >= 0 and k.amount >= 50 and m.amount >= 50:
                    making_flame = True
            elif self.x >= 1100 and self.x <= 1200 and self.y >= 600 and self.y <= 700:
                if l.amount >= 10 and k.amount >= 50 and m.amount >= 80:
                    making_health = True


class Background(pygame.sprite.Sprite):
    def __init__(self, name, location, color=None, srez=None):
        pygame.sprite.Sprite.__init__(self)
        if srez is None:
            self.main = load_image(name)
        if srez is not None:
            self.main = load_image(name, srez)
        if color:
            self.main = pygame.transform.scale(self.main, color)
        self.rect = self.main.get_rect()
        self.rect.left, self.rect.top = location


class Farming_st(pygame.sprite.Sprite):
    def __init__(self, type, dif, location, name):
        pygame.sprite.Sprite.__init__(self)
        self.amount = 0
        self.t = type
        self.loc = location
        if dif == 'Easy':
            self.speed = 0.033
        elif dif == 'Normal':
            self.speed = 0.016
        elif dif == 'Hard':
            self.speed = 0.016
        img = Background(name, location)
        screen.blit(img.main, img.rect)

    def more(self):
        coords = (self.loc[0] + 150, self.loc[1])
        self.amount += self.speed
        write_a_word(int(coords[0]), int(coords[1]), str(self.t + str(int(self.amount))), None, 30)

    def get_a(self):
        return float(self.amount)


class Difficulty:
    def __init__(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.x = event.pos[0]
            self.y = event.pos[1]
            self.dif = None
            self.on_click()
        write_a_word(100, 100, "Выберете сложность игры:", None, 50)

        write_a_word(50, 200, 'Лёгкая', None, 40)
        write_a_word(55, 250, 'Много ХП', None, 30)
        write_a_word(55, 300, 'Простые враги', None, 30)
        write_a_word(55, 350, 'Быстрые ресурсы', None, 30)

        write_a_word(250, 200, 'Нормальная', None, 40)
        write_a_word(255, 250, 'Среднее кол-во хп', None, 30)
        write_a_word(255, 300, 'Средние враги', None, 30)
        write_a_word(255, 350, 'Ресурсы в норме', None, 30)

        write_a_word(500, 200, 'Сложная', None, 40)
        write_a_word(505, 250, 'Мало ХП', None, 30)
        write_a_word(505, 300, 'Сложные враги', None, 30)
        write_a_word(505, 350, 'Мало ресурсов', None, 30)

    def on_click(self):
        x = self.x
        y = self.y
        if x >= 50 and x <= 250:
            self.dif = 'Easy'
        elif x > 250 and x < 500:
            self.dif = 'Normal'
        elif x >= 500 and x <= 700:
            self.dif = 'Hard'


if __name__ == '__main__':
    start_screen = True
    dif_screen = False
    main_game = False
    stations_done = False
    endgame = False
    win = False
    pygame.init()
    clock = pygame.time.Clock()
    width, height = 700, 700
    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Portal Defence')
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if start_screen:
                write_a_word(230, 100, 'Начать игру?', None, 50)
                write_a_word(250, 200, "Да.", None, 50)
                write_a_word(350, 200, "Нет.", None, 50)
            if event.type == pygame.MOUSEBUTTONDOWN and start_screen:
                pos = event.pos
                x = pos[0]
                y = pos[1]
                if x >= 250 and x < 350 and y >= 200 and y < 300 and not dif_screen:
                    start_screen = False
                    dif_screen = True
                    screen.fill((0, 0, 0))
                elif x >= 350 and x <= 450 and y > 200 and y < 300:
                    terminate()
            elif dif_screen:
                window = Difficulty(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    window = Difficulty(event)
                    dif = window.dif
                    if dif:
                        dif_screen = False
                        main_game = True
                        stations_done = True
            if stations_done:
                stations_done = False
                l = Farming_st('Лес:', dif, (0, 0), 'les.jpg')
                k = Farming_st('Камень:', dif, (500, 0), 'kamen.jpg')
                m = Farming_st('Металл:', dif, (1000, 0), 'metal.jpg')
                if dif == 'Easy':
                    total_health = 3000
                elif dif == 'Normal':
                    total_health = 1000
                elif dif == 'Hard':
                    total_health = 100
            if main_game:
                update_damage()
                shoot_sometimes_or_whatever(time)
                time += clock.get_time() / 1000
                if l.amount < 0:
                    l.amount = 0
                if k.amount < 0:
                    k.amount = 0
                if m.amount < 0:
                    m.amount = 0
                width = 1280
                height = 720
                size = width, height
                screen = pygame.display.set_mode(size)
                b = Background('fon.png', [0, 0])
                screen.blit(b.main, b.rect)
                les_img = Background('les.jpg', (0, 0))
                kamen_img = Background('kamen.jpg', (500, 0))
                metal_img = Background('metal.jpg', (1000, 0))
                screen.blit(les_img.main, les_img.rect)
                screen.blit(kamen_img.main, kamen_img.rect)
                screen.blit(metal_img.main, metal_img.rect)
                for weapon in weapons:
                    main = Background(str(weapon[2]) + '.png', (weapon[0], 280), (75, 75))
                    screen.blit(main.main, main.rect)
                for enemy in existing_enemies:
                    main = Background(str(enemy[2]) + '.png', (enemy[0], 280), (75, 75))
                    screen.blit(main.main, main.rect)
                to_remove = []
                for bullet in fire:
                    if time <= bullet[4] + 1:
                        b = Background(bullet[1], bullet[0], (20, 20))
                        screen.blit(b.main, b.rect)
                    else:
                        to_remove.append(bullet)
                for thing in to_remove:
                    fire.remove(thing)
                l.more()
                k.more()
                m.more()
                button_1 = Update_button(event, 'upgrade.png', (50, 600), dif)
                if not making_tower and not making_auto and not making_flame and not making_health:
                    button_2 = Make_weapon(dif, event)
                elif making_tower:
                    write_a_word(325, 550, 'Выберите место на дороге.', None, 30)
                    Making_sniper(event, dif)
                elif making_flame:
                    write_a_word(600, 550, 'Выберите место на дороге.', None, 30)
                    Making_flame(event, dif)
                elif making_health:
                    write_a_word(850, 550, 'Выберите место на дороге.', None, 30)
                    Making_health(event, dif)
                elif making_auto:
                    write_a_word(975, 550, 'Выберите место на дороге.', None, 30)
                    Making_auto(event, dif)
                if time > 0 and not mass_in_mass([200, 210, 220, 230, 240, 250, 260, 270, 280, 290], dead_ids):
                    for sp_t in range(200, 300, 10):
                        Enemy(dif, 'bird_enemy', 200, 50, 400, sp_t, time, 12)
                if time > 300 and not mass_in_mass([310, 320, 330, 340, 350, 360, 370, 380, 390, 400], dead_ids):
                    for sp_t in range(310, 410, 10):
                        Enemy(dif, 'bird_enemy', 400, 100, 400, sp_t, time, 12)
                if time > 400 and not mass_in_mass([410, 420, 430, 440, 450, 460, 470, 480, 490, 500], dead_ids):
                    for sp_t in range(410, 510, 10):
                        Enemy(dif, 'bird_enemy', 600, 100, 400, sp_t, time, 12)
                if dead_ids == wining_mass:
                    screen.fill((0, 0, 0))
                    main_game = False
                    win = True
                if total_health <= 0:
                    main_game = False
                    screen.fill((0, 0, 0))
                    endgame = True
            elif endgame:
                write_a_word(960, 600, 'Вы проиграли....', None, 60)
            elif win:
                write_a_word(960, 600, 'Вы выиграли!', None, 60)

        pygame.display.flip()
        clock.tick(FPS)
