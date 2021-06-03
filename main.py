import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import QSize, Qt

SIZE = 10
LVL_COUNT = 2

BLOCK_LETTER = 'Б'
FINISH_LETTER = 'Ф'
READY_LETTER = 'Г'
VOID_LETTER = '1'
BRICK_LETTER = '0'



class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Сокобан'
        self.left = 300
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.choseLevel = QPushButton('Выбрать уровень', self)
        self.choseLevel.setFont(QFont('Arial', 40))
        self.choseLevel.move(100, 100)
        self.choseLevel.setMinimumSize(600, 100)
        self.choseLevel.clicked.connect(self.levelsShow)

        self.levels = []
        for i in range(LVL_COUNT):
                temp = QPushButton('Уровень ' + str(i + 1), self)
                temp.setFont(QFont('Arial', 25))
                temp.move(10 + (i % 3) * 260, 10 + (i // 3) * 110)
                temp.setMinimumSize(250, 100)
                temp.hide()
                temp.clicked.connect(self.activateLevel)
                self.levels.append(temp)

        self.tiles = []
        for i in range(SIZE):
            tt = []
            for j in range(SIZE):
                temp = 0
                temp = QFrame(self)
                temp.setLineWidth(3)
                temp.setFrameShape(QFrame.Box)
                temp.setFrameShadow(QFrame.Plain)
                temp.setFont(QFont('Arial', 25))
                temp.setFixedSize(QSize(60, 60))
                temp.move(10 + i * 58, 10 + j * 58)
                temp.setAutoFillBackground(True)
                temp.hide()
                tt.append(temp)
            self.tiles.append(tt)

        self.laborer = QLabel('←',self)
        self.laborer.setFont(QFont('Arial', 25))
        self.laborer.hide()
        
        self.levelsBack = QPushButton('Назад',self)
        self.levelsBack.setFont(QFont('Arial', 25))
        self.levelsBack.move(610, 510)
        self.levelsBack.setMinimumSize(170, 70)
        self.levelsBack.hide()
        self.levelsBack.clicked.connect(self.backMenu)
        
        self.gameBack = QPushButton('Назад',self)
        self.gameBack.setFont(QFont('Arial', 25))
        self.gameBack.move(610, 510)
        self.gameBack.setMinimumSize(170, 70)
        self.gameBack.hide()
        self.gameBack.clicked.connect(self.backLevels)

        self.restart = QPushButton('Заново',self)
        self.restart.setFont(QFont('Arial', 25))
        self.restart.move(610, 270)
        self.restart.setMinimumSize(170, 70)
        self.restart.hide()
        self.restart.clicked.connect(self.resetlvl)
        
        self.forward = QPushButton('Вперёд',self)
        self.forward.setFont(QFont('Arial', 25))
        self.forward.move(610, 30)
        self.forward.setMinimumSize(170, 70)
        self.forward.hide()
        self.forward.clicked.connect(self.nextlvl)
        
        self.show()

    def nextlvl(self):
        lvlnum = int(''.join(x for x in self.lvlname if x.isdigit())) + 1
        self.forward.hide()
        
        if lvlnum>LVL_COUNT:
            self.backLevels()
        else:
            self.lvlname = "level_" + str(lvlnum) + ".txt"
            self.resetlvl()

    def levelsShow(self):
        self.choseLevel.hide()
        for i in self.levels:
            i.show()
        self.levelsBack.show()
        
    def backMenu(self):
        self.choseLevel.show()
        for i in self.levels:
            i.hide()
        self.levelsBack.hide()
    def backLevels(self):
        for i in self.levels:
            i.show()
        for i in self.tiles:
            for j in i:
                j.hide()
        self.laborer.hide()
        self.levelsBack.show()
        self.gameBack.hide()
        self.restart.hide()
    
    def redrawGame(self):
        brick = QPalette(QColor("orange"))
        void = QPalette(QColor("blue"))
        block = QPalette(QColor("yellow"))
        finish = QPalette(QColor("darkGray"))
        ready = QPalette(QColor("green"))
        for i in range(10):
            for j in range(10):
                tile = self.g.field[i][j]
                if tile == BRICK_LETTER:
                    pal = brick
                elif tile == VOID_LETTER:
                    pal = void
                elif tile == BLOCK_LETTER:
                    pal = block
                elif tile == FINISH_LETTER:
                    pal = finish
                elif tile == READY_LETTER:
                    pal = ready
                self.tiles[i][j].setPalette(pal)
                '''←↑→↓'''
        (x,y) = (self.g.coords[0],self.g.coords[1])
        rotato = self.g.direction
        if rotato == 0:
            self.laborer.setText('←')
        elif rotato == 1:
            self.laborer.setText('↑')
        elif rotato == 2:
            self.laborer.setText('→')
        elif rotato == 3:
            self.laborer.setText('↓')
        shift = 11 if rotato % 2 ==1 else 0
        self.laborer.move(19 + shift + x * 58, 15 + y * 58)
        
    def activateLevel(self):
        sender = self.sender()
        self.lvlname = "level_" + sender.text().split(' ')[-1] + ".txt"
        self.resetlvl()
        
    def resetlvl(self):
        for i in self.levels:
            i.hide()
        self.g = Game(self.lvlname)
        self.redrawGame()
        for i in self.tiles:
            for j in i:
                j.show()
        self.laborer.show()
        self.levelsBack.hide()
        self.gameBack.show()
        self.restart.show()
        
    def keyPressEvent(self, event):
        rotato = 5
        if event.key() == Qt.Key_A:
            rotato = 0
        elif event.key() == Qt.Key_W:
            rotato = 1
        elif event.key() == Qt.Key_D:
            rotato = 2
        elif event.key() == Qt.Key_S:
            rotato = 3
        win = self.g.action(rotato)
        self.redrawGame()
        if win:
            self.forward.show()
        
class Game:
    dirs = [[-1,0],
            [0,-1],
            [1,0],
            [0,1]]

    def __init__(self,fName):
        self.fromFile(fName)       
    
    def singleMove(self):
        return [self.coords[0] + self.dirs[self.direction][0], self.coords[1] + self.dirs[self.direction][1]]
    
    def doubleMove(self):
        return [self.coords[0] + self.dirs[self.direction][0] * 2, self.coords[1] + self.dirs[self.direction][1] * 2]      
    
    def getTile(self, cord):
        return self.field[cord[0]][cord[1]]
    
    def setTile(self, cord, tile):
        self.field[cord[0]][cord[1]] = tile
        
    def moveBlock(self):
        nextNextTile = self.getTile(self.doubleMove())
        nextTile = self.getTile(self.singleMove())
        counter = 0
        if nextNextTile == VOID_LETTER:
            self.setTile(self.doubleMove(), BLOCK_LETTER)
            counter += 1
        elif nextNextTile == FINISH_LETTER:
            self.setTile(self.doubleMove(), READY_LETTER)
            counter += 1
            
        if nextTile == READY_LETTER:
            self.setTile(self.singleMove(), FINISH_LETTER)
            counter += 1
        elif nextTile == BLOCK_LETTER:
            self.setTile(self.singleMove(), VOID_LETTER)
            counter += 1
        if counter == 2:
                self.coords = self.singleMove()
        
    def fromFile(self, fName):
        f = open("levels/" + fName, "r", encoding = 'utf-8')
        Name = f.readline()
        
        self.field = [f.readline().split(" ")[:SIZE] for i in range(SIZE)]
        self.field = [[row[i] for row in self.field] for i in range(len(self.field[0]))]
        self.coords = [int(i) for i in (f.readline().split(" "))[:2]]
        self.direction = 0
        f.close()
        
    def checkWin(self):
        for i in self.field:
            for j in i:
                if j == FINISH_LETTER:
                    return False
        return True

    def action(self,butt):
        if self.direction != butt:
            if butt<4:
                self.direction = butt
        else:
            1  
        if True:
            nextTile = self.getTile(self.singleMove())
            nextNextTile = self.getTile(self.doubleMove())
            if nextTile == VOID_LETTER or nextTile == FINISH_LETTER:
                self.coords = self.singleMove()
            elif nextTile == BLOCK_LETTER or nextTile == READY_LETTER:
                if nextNextTile == FINISH_LETTER or nextNextTile == VOID_LETTER:
                    self.moveBlock()
                    return self.checkWin()
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
    
    
    
    
    