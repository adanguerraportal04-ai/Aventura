
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window

Window.size = (800, 480)

class Aventura(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.xp = 80
        self.yp = 100
        self.vy = 0
        self.speed = 5
        self.score = 0
        self.lives = 3
        self.ground = 65
        self.camera = 0
        self.left = False
        self.right = False
        self.jump = False
        self.coins = [250, 380, 600, 850, 1100, 1400, 1700, 2050]
        self.enemy_x = 900
        self.enemy_dir = 1
        self.chest_x = 2300
        self.finished = False

        self.hud = Label(
            text="AVENTURAS | Monedas: 0 | Vidas: 3",
            size_hint=(None, None),
            size=(500, 45),
            pos=(10, self.height-45)
        )
        self.add_widget(self.hud)

        Clock.schedule_interval(self.update, 1/60)
        self.bind(size=self.draw_game, pos=self.draw_game)

    def on_touch_down(self, touch):
        if self.finished:
            self.reset()
            return True

        x = touch.x / self.width

        if x < 0.25:
            self.left = True
        elif x < 0.50:
            self.right = True
        else:
            self.jump = True

        return True

    def on_touch_up(self, touch):
        self.left = False
        self.right = False
        self.jump = False
        return True

    def reset(self):
        self.xp = 80
        self.yp = 100
        self.vy = 0
        self.score = 0
        self.lives = 3
        self.coins = [250, 380, 600, 850, 1100, 1400, 1700, 2050]
        self.enemy_x = 900
        self.finished = False

    def update(self, dt):
        if self.finished:
            self.draw_game()
            return

        if self.left:
            self.xp -= self.speed
        if self.right:
            self.xp += self.speed

        self.xp = max(0, min(2400, self.xp))

        self.vy -= 0.7
        self.yp += self.vy

        if self.yp <= self.ground:
            self.yp = self.ground
            self.vy = 0

        if self.jump and self.yp <= self.ground + 1:
            self.vy = 13

        for c in self.coins[:]:
            if abs(self.xp-c) < 30 and self.yp < 150:
                self.coins.remove(c)
                self.score += 10

        self.enemy_x += self.enemy_dir * 2
        if self.enemy_x > 1050 or self.enemy_x < 850:
            self.enemy_dir *= -1

        if abs(self.xp-self.enemy_x) < 35 and self.yp < 130:
            self.lives -= 1
            self.xp = max(0, self.xp-100)
            self.enemy_x = 900

        if self.lives <= 0:
            self.finished = True

        if abs(self.xp-self.chest_x) < 40:
            self.finished = True

        self.camera = max(0, self.xp-self.width/2)

        self.hud.text = (
            f"AVENTURAS | Monedas: {self.score} | Vidas: {self.lives}"
        )
        self.hud.pos = (10, self.height-45)

        self.draw_game()

    def draw_game(self, *args):
        w, h = self.width, self.height
        cam = self.camera

        self.canvas.clear()

        with self.canvas:
            # Cielo
            Color(0.35, 0.68, 0.90)
            Rectangle(pos=self.pos, size=self.size)

            # Sol
            Color(1, 0.85, 0.1)
            Ellipse(pos=(w-100, h-100), size=(60, 60))

            # Montañas
            Color(0.25, 0.48, 0.40)
            for i in range(-1, 7):
                x = i*220 - (cam*0.3 % 220)
                Rectangle(pos=(x, self.ground+45), size=(150, 130))

            # Suelo
            Color(0.35, 0.19, 0.08)
            Rectangle(pos=(0, 0), size=(w, self.ground))

            Color(0.15, 0.55, 0.20)
            Rectangle(pos=(0, self.ground), size=(w, 15))

            # Árboles
            for i in range(12):
                x = i*230 - (cam % 230)
                Color(0.30, 0.16, 0.06)
                Rectangle(pos=(x, self.ground+15), size=(12, 55))
                Color(0.04, 0.35, 0.12)
                Ellipse(pos=(x-25, self.ground+50), size=(65, 65))

            # Cuevas
            Color(0.08, 0.08, 0.12)
            Ellipse(pos=(1500-cam, self.ground), size=(130, 110))

            # Monedas
            for c in self.coins:
                Color(1, 0.8, 0)
                Ellipse(pos=(c-cam, self.ground+85), size=(20, 20))

            # Monstruo
            Color(0.85, 0.12, 0.12)
            Rectangle(pos=(self.enemy_x-cam, self.ground), size=(38, 42))

            # Cofre
            Color(0.45, 0.22, 0.05)
            Rectangle(pos=(self.chest_x-cam, self.ground), size=(48, 42))
            Color(1, 0.8, 0)
            Rectangle(pos=(self.chest_x-cam, self.ground+17), size=(48, 7))

            # Mochila
            px = self.xp-cam
            Color(0.45, 0.22, 0.05)
            Rectangle(pos=(px-8, self.yp+12), size=(13, 25))

            # Explorador
            Color(0.1, 0.25, 0.85)
            Rectangle(pos=(px, self.yp), size=(30, 35))

            Color(1, 0.76, 0.55)
            Ellipse(pos=(px+5, self.yp+35), size=(22, 22))

            # Sombrero
            Color(0.45, 0.25, 0.08)
            Rectangle(pos=(px, self.yp+53), size=(32, 7))
            Rectangle(pos=(px+7, self.yp+59), size=(18, 7))

            # Botones
            Color(0.08, 0.12, 0.25, 0.85)
            Rectangle(pos=(15, 15), size=(75, 65))
            Rectangle(pos=(105, 15), size=(75, 65))
            Rectangle(pos=(w-95, 15), size=(80, 65))

            # Si termina
            if self.finished:
                Color(0, 0, 0, 0.8)
                Rectangle(pos=(w/2-180, h/2-50), size=(360, 100))

                Color(1, 0.85, 0)
                Rectangle(pos=(w/2-150, h/2-5), size=(300, 5))

class JuegoApp(App):
    def build(self):
        return Aventura()

if __name__ == "__main__":
    JuegoApp().run()

