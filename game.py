from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero
from panda3d.core import LColor

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Встановлюємо білий фон
        base.setBackgroundColor(LColor(1, 1, 1, 1))

        self.land = Mapmanager()
        x, y = self.land.loadLand("land.txt")
        self.hero = Hero((x, y, 2), self.land)
        base.camLens.setFov(90)




game = Game()

game.run()