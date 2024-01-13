import pygame
import math


class Player:
    def __init__(self, x=300, y=300, speed=8):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = 100
        self.maxhp = 100

    def coor(self):
        return [self.x, self.y]

    def get_speed(self):
        return self.speed

    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 255, 255), (self.x - 20, self.y - 20, 40, 40))
        if self.hp > 0:
            self.hp -= p.get_enemy_projectile([self.x - 25, self.y - 25], [self.x + 25, self.y + 25])
            pygame.draw.rect(screen, (255, 255, 255), (30 - 20, 20 + 30, 150, 30))
            pygame.draw.rect(screen, (255, 0, 0), ((30 - 20), 20 + 30, 150 * (self.hp / self.maxhp), 30))

    def move(self, coor2):
        self.x += (coor2[0] * self.speed)
        self.y += (coor2[1] * self.speed)

    def calm(self):
        self.x = (self.x // 2) * 2
        self.y = (self.y // 2) * 2

    def change_speed(self, speed2):
        self.speed = speed2

    def get_hp(self):
        return self.hp

    def sword(self, coor2, screen):
        lenn = 20
        self.dex = -(coor2[0] - self.x)
        self.dey = -(coor2[1] - self.y)
        self.coof = 250 / math.sqrt((self.dex ** 2 + self.dey ** 2))
        self.dot1x = self.x + (self.dex + self.dey) * -self.coof * 0.7
        self.dot1y = self.y + (-self.dey + self.dex) * self.coof * 0.7
        self.dot2x = self.x + (self.dex - self.dey) * -self.coof * 0.7
        self.dot2y = self.y + (-self.dey - self.dex) * self.coof * 0.7
        pygame.draw.polygon(screen, (255, 255, 255), ([self.dot1x, self.dot1y], [self.dot2x, self.dot2y], [self.x, self.y]))
        p.get_sword([self.dot1x, self.dot1y], [self.dot2x, self.dot2y], [self.x, self.y])

    def sword_render(self):
        pygame.draw.polygon(screen, (255, 255, 255), ([self.dot1x, self.dot1y], [self.dot2x, self.dot2y], [self.x, self.y]))


class Projectile:
    def __init__(self):
        self.projectiles = []

    def add_projectile(self, coor, end_coor, damage, speed=20, char=0):
        self.coor = coor
        self.end_coor = end_coor
        self.dex = -(self.end_coor[0] - self.coor[0])
        self.dey = -(self.end_coor[1] - self.coor[1])
        self.coof = speed / math.sqrt((self.dex ** 2 + self.dey ** 2))
        self.damage = damage
        self.speed = speed
        self.char = char
        pr = [self.coor, self.dex, self.dey, self.coof, self.damage, self.speed, self.char]
        self.projectiles.append(pr)

    def fly(self):
        for i in self.projectiles:
            i[0][0] -= i[1] * i[3]
            i[0][1] -= i[2] * i[3]

    def render_projectile(self, screen):
        for i in self.projectiles:
            if i[6] == 0:
                pygame.draw.circle(screen, (255, 0, 0), (i[0][0], i[0][1]), 20)
            if i[6] == 1:
                pygame.draw.rect(screen, (0, 255, 0), (i[0][0]-10, i[0][1]-10, 20, 20))

    def get_projectile(self, coor1, coor2, rad=10):
        count = 0
        projsp = [0]
        delsp = []
        for ii in self.projectiles:
            if coor1[0]-rad <= ii[0][0] <= coor2[0]+rad and coor1[1]-rad <= ii[0][1] <= coor2[1]+rad and ii[6] == 0:
                qqq = int(ii[4])
                delsp.append(count)
                projsp.append(qqq)
            count += 1
        for qwe in delsp:
            self.projectiles.pop(qwe)
        return sum(projsp)

    def get_enemy_projectile(self, coor1, coor2, rad=10):
        count = 0
        projsp = [0]
        delsp = []
        for ii in self.projectiles:
            if coor1[0] - rad <= ii[0][0] <= coor2[0] + rad and coor1[1] - rad <= ii[0][1] <= coor2[1] + rad and ii[6] == 1:
                qqq = int(ii[4])
                delsp.append(count)
                projsp.append(qqq)
            count += 1
        for qwe in delsp:
            self.projectiles.pop(qwe)
        return sum(projsp)

    def get_sword(self, coor1, coor2, coor3, rad=5):
        count = 0
        delsp = []
        for ii in self.projectiles:
            a = (coor1[0] - ii[0][0]) * (coor2[1] - coor1[1]) - (coor2[0] - coor1[0]) * (coor1[1] - ii[0][1])
            b = (coor2[0] - ii[0][0]) * (coor3[1] - coor2[1]) - (coor3[0] - coor2[0]) * (coor2[1] - ii[0][1])
            c = (coor3[0] - ii[0][0]) * (coor1[1] - coor3[1]) - (coor1[0] - coor3[0]) * (coor3[1] - ii[0][1])
            if (a >= 0 ) == (b >= 0 ) == (c >= 0):
                delsp.append(count)
            count += 1
        for qwe in delsp:
            self.projectiles.pop(qwe)


class Dummy:
    def __init__(self, x=300, y=1080-100, hp=200):
        self.x = x
        self.y = y
        self.hp = hp
        self.maxhp = hp

    def render_dummy(self, screen):
        if self.hp > 0:
            self.hp -= p.get_projectile([self.x - 25, self.y - 25], [self.x + 25, self.y + 25])
            pygame.draw.rect(screen, (0, 0, 255), (self.x - 20, self.y - 20, 40, 40))
            pygame.draw.rect(screen, (255, 255, 255), (self.x - 20, self.y + 30, 50, 15))
            pygame.draw.rect(screen, (255, 0, 0), ((self.x - 20), self.y + 30, 50 * (self.hp / self.maxhp), 15))
        else:
            pygame.draw.rect(screen, (155, 155, 155), (self.x - 20, self.y - 20, 40, 40))

    def dummy_attack(self):
        if self.hp > 0:
            p.add_projectile([self.x, self.y], g.coor(), 10, 10, 1)


class Board:
    def __init__(self):
        pass

    def render(self, screen):
        pass


class Animation:
    def __init__(self):
        self.last = pygame.time.get_ticks()
        self.cooldown = 150

    def sprite_change(self, screen, sprite, num):
        now = pygame.time.get_ticks()
        screen.blit(sprite, [g.coor()[0]-40, g.coor()[1]-44])
        if now - self.last >= self.cooldown:
            self.last = now
            return num + 1
        return num


def change(num, op):
    ism = 0.6
    if op == 1:
        if (num + ism) > 1:
            return 1
        return num + ism
    if op == 2:
        if (num - ism) < -1:
            return -1
        return num - ism


def iner_change(num, op):
    ism = 0.15
    if op == 1:
        if (num - ism) < 0:
            return 0
        else:
            return num - ism
    if op == 2:
        if (num + ism) > 0:
            return 0
        else:
            return num + ism


a = Board()
g = Player()
p = Projectile()
animation = Animation()
dummy = Dummy()
dummy2 = Dummy(1400)
dummy4 = Dummy(900, 100)
stay_still = [pygame.image.load('Sprite-0001.png'),
              pygame.image.load('Sprite-0002.png'),
              pygame.image.load('Sprite-0003.png'),
              pygame.image.load('Sprite-0004.png'),
              pygame.image.load('Sprite-0005.png'),
              pygame.image.load('Sprite-0006.png'),
              pygame.image.load('Sprite-0007.png'),
              pygame.image.load('Sprite-0008.png'),
              pygame.image.load('Sprite-0009.png'),
              pygame.image.load('Sprite-0010.png'),
              pygame.image.load('Sprite-0011.png'),
              pygame.image.load('Sprite-0012.png'),
              pygame.image.load('Sprite-0013.png')]
stay_timer = 0
sprite_num = 0
if __name__ == '__main__':
    pygame.init()
    size = width, height = [1920, 1080]
    screen = pygame.display.set_mode(size, pygame.SCALED | pygame.FULLSCREEN, vsync=1)
    font = pygame.font.Font(None, 20)
    running = True
    sp = [0, 0]
    dummy_count = 0
    player_count = 0
    shift_count = 0
    sword_count = 0
    plspeed = g.get_speed()
    shift_action = 0
    sword_action = 0
    sword_coor2 = 0
    while running:
        if g.get_hp() > 0:
            dummy_count += 1
            player_count += 1
            shift_count += 1
            sword_count += 1
            if shift_action != 0:
                shift_action += 1
            if shift_action == 10:
                shift_action = 0
                g.change_speed(plspeed)
            if sword_action != 0:
                sword_action += 1
                g.sword(sword_coor2, screen)
            if sword_action == 7:
                sword_action = 0
            screen.fill((50, 50, 50))
            a.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and player_count >= 40:
                        p.add_projectile(g.coor(), event.pos, 35)
                        player_count = 0
                    if event.button == 3 and sword_count >= 70:
                        sword_count = 0
                        sword_action = 1
                        sword_coor2 = event.pos
                        g.sword(event.pos, screen)

            keys = pygame.key.get_pressed()
            sp1 = [0, 0, 0, 0]
            if keys[pygame.K_d]:
                sp[0] = change(sp[0], 1)
                sp1[0] = 1
            if keys[pygame.K_a]:
                sp[0] = change(sp[0], 2)
                sp1[1] = 1
            if keys[pygame.K_w]:
                sp[1] = change(sp[1], 2)
                sp1[2] = 1
            if keys[pygame.K_s]:
                sp[1] = change(sp[1], 1)
                sp1[3] = 1
            if keys[pygame.K_q]:
                running = False
            if keys[pygame.K_SPACE]:
                if shift_count > 50:
                    shift_count = 0
                    shift_action = 1
                    g.change_speed(30)

            if sum(sp1) == 2:
                if sp[0] > 0:
                    sp[0] = sp[0] / 1.1
                if sp[0] < 0:
                    sp[0] = sp[0] / 1.1
                if sp[1] < 0:
                    sp[1] = sp[1] / 1.1
                if sp[1] > 0:
                    sp[1] = sp[1] / 1.1

            if sp[0] > 0 and not (sp[0] == 1 and sp1[0] == 1):
                sp[0] = iner_change(sp[0], 1)
            if sp[0] < 0 and not (sp[0] == -1 and sp1[1] == 1):
                sp[0] = iner_change(sp[0], 2)
            if sp[1] > 0 and not (sp[1] == 1 and sp1[3] == 1):
                sp[1] = iner_change(sp[1], 1)
            if sp[1] < 0 and not (sp[1] == -1 and sp1[2] == 1):
                sp[1] = iner_change(sp[1], 2)

            if sp[0] == 0 and sp[1] == 0:
                g.calm()
            if dummy_count == 30:
                dummy.dummy_attack()
                dummy2.dummy_attack()
                dummy4.dummy_attack()
                dummy_count = 0
            sp[0] = round(sp[0], 2)
            sp[1] = round(sp[1], 2)
            g.move(sp)
            dummy.render_dummy(screen)
            dummy2.render_dummy(screen)
            dummy4.render_dummy(screen)
            p.fly()
            p.render_projectile(screen)
            if sword_action != 0:
                g.sword_render()
            g.draw(screen)
            '''if sp == [0, 0]:
                stay_timer += 1
            if sp != [0, 0]:
                stay_timer = 0
                sprite_num = 0'''
            if stay_timer >= 0:
                if sprite_num == 13:
                    sprite_num = 0
                sprite_num = animation.sprite_change(screen, stay_still[sprite_num], sprite_num)
        else:
            screen.fill((100, 100, 100))
            font = pygame.font.Font(None, 100)
            text1 = font.render(f'ВЫ ПОГИБЛИ', True, [255, 255, 255])
            screen.blit(text1, (700, (1080/2)-100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.display.flip()
    pygame.quit()
