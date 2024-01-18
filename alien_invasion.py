import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width, self.settings.screen_heigh))

        self.screen=pygame.display.set_mode((1200, 800))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)   全屏玩法
        # self.settings.screen_width = self.screeen.get_rect().width
        # self.settings.screen_height = self.screeen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.bg_color = (230, 230, 230)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.stats = GameStats(self)

        self._create_fleet()
    def run_game(self):
        while(True):
            self._check_events() #每次循环重构屏幕

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()        #更新屏幕上的图像 并切换到新屏幕

    def _check_events(self):
        # 响应按键和鼠标事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP: # 根据up和down实现持续按下移动
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_q: # 按下q键可以快捷退出
            sys.exit()
        elif event.key == pygame.K_SPACE: # 空格键实现开火
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed: # 检查未消失的子弹数是否小于允许的数量
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))  可以判断屏幕上还有多少子弹
        self._check_bullet_alien_collisions()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            print("Ship hit!!!")

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:# 如果外星人没了 删除现有的子弹并且新建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """创建外星人群"""

        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2*alien_width) # 查看可用的水平空间
        number_aliens_x = available_space_x//(2*alien_width) # 假设两个外星人间距为一个宽度 求出数量

        for alien_number in range(number_aliens_x):
            self._create_alien(alien_number)

    def _create_alien(self, alien_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        # 检查是否由外星人到了屏幕底端
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit() # 像飞船被撞到一样处理
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self): # 响应飞船被外星人撞到
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)#重绘屏幕
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()#让最近绘制的屏幕可见


if __name__=='__main__':
    ai = AlienInvasion()
    ai.run_game()
