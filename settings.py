class Settings:
    "存储游戏中所有设置的类"
    def __init__(self):
        self.screen_width=1200
        self.screen_heigh=800
        self.bg_color=(230,230,230)
        self.ship_speed = 1.5

        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3 #允许三个子弹
        self.alien_speed = 0.8
        self.ship_limit = 3
        self.fleet_drop_speed = 50
        # fleet_direction 为1表示右 -1表示左
        self.fleet_direction= 1