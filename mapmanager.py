import pickle
from panda3d.core import CardMaker, TextureStage

class Mapmanager():
    def __init__(self):
        self.model = 'block.egg'
        self.textures = {
            'stone': 'block.png',
            'wood': 'wod1.jpg',
            'snow': 'snow.png',
            'gift': 'gift.jpg'
        }
        self.colors = {
            'stone': (0.5, 0.5, 0.5, 1),
            'wood': (0.6, 0.4, 0.2, 1),
            'snow': (1, 1, 1, 1),
            'gift': (1, 0, 1, 1)
        }

        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def addBlock(self, position):
        """Додає блок із текстурою та кольором."""
        x, y, z = position

        # Підлога завжди кам'яна
        if z == 0:
            texture = self.textures['snow']
            color = self.colors['snow']
        elif x < 10:
            texture = self.textures['wood']
            color = self.colors['wood']
        elif x > 22:
            texture = self.textures['gift']
            color = self.colors['gift']
        else:
            texture = self.textures['stone']
            color = self.colors['stone']

        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(texture))
        self.block.setColor(color)
        self.block.setPos(position)
        self.block.setTag('at', str(position))
        self.block.reparentTo(self.land)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        return not bool(blocks)

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        """Додає новий блок над існуючим."""
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position):
        """Видаляє блок."""
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for _ in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
