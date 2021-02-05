from tkinter import Frame, PhotoImage
from random import random
from copy import deepcopy
import bib
import uibib as ui

MC_COUNT = 10

def randMove (p, cp):
    B = []
    for i in range(bib.DIM):
        for j in range(bib.DIM):
            if p[i][j].w == True: B.append(bib.Move(i, j, 'w'))
            if p[i][j].d == True: B.append(bib.Move(i, j, 'd'))
            if p[i][j].s == True: B.append(bib.Move(i, j, 's'))
            if p[i][j].a == True: B.append(bib.Move(i, j, 'a'))
    move = B[int(cp*random())]
    return move

def mcArrowMove(game, move):
    gaux = deepcopy(game)
    gaux.moveGame(move)
    valid  = True
    i = 0
    while valid:
        maux = randMove(gaux.P, gaux.cp)
        gaux.moveGame(maux)
        i = i + 1
        if gaux.max['red']==6 or gaux.max['blue']==6 or gaux.count['red']==0 or gaux.count['blue']==0 or gaux.cp==0 or i==MC_COUNT: valid = False
    score = 0
    for i in range (bib.DIM):
        for j in range (bib.DIM):
            if gaux.B[i][j].color == 'red': score = score + 2**gaux.B[i][j].value - 1
            elif gaux.B[i][j].color == 'blue': score = score - 2**gaux.B[i][j].value + 1
    return score

def scoreMove (game, i, j, d, move, score):
    newmove = move
    newscore = score
    aux = bib.Move(i, j, d) 
    saux = mcArrowMove(game, aux)
    for k in range (10): saux = saux + mcArrowMove(game, aux)
    if saux > score: 
        newmove = aux
        newscore = saux
    return newmove, newscore

def mcMove(game):
    score = -10240
    move = bib.Move(0, 0, 'w')
    for i in range (bib.DIM):
        for j in range (bib.DIM):
            if game.P[i][j].w == True: move, score = scoreMove(game, i, j, 'w', move, score)
            if game.P[i][j].d == True: move, score = scoreMove(game, i, j, 'd', move, score)
            if game.P[i][j].s == True: move, score = scoreMove(game, i, j, 's', move, score)            
            if game.P[i][j].a == True: move, score = scoreMove(game, i, j, 'a', move, score)    
    return move

def chooseColor():
    diece = 6*random()
    if (diece<3): return 'blue'
    else: return 'red'

class Display(Frame):
    def __init__(self):
        Frame.__init__(self)
        self = ui.head(self)
        self.background = ui.bg(self)
        self.pieces = {0: PhotoImage (file =  'coin1.png'),1: PhotoImage (file = 'pawnw.png'), 2: PhotoImage (file = 'knightw.png'), 3: PhotoImage (file = 'bishopw.png'),
                      4: PhotoImage (file = 'rookw.png'), 5: PhotoImage (file = 'queenw.png'), 6: PhotoImage (file = 'kingw.png'), 'empty': PhotoImage(file = 'empty.png')}
        self.coins = {1: PhotoImage (file = 'coin1.png'), 2: PhotoImage (file = 'coin2.png'), 3: PhotoImage (file = 'boot.png'), 
                      4: PhotoImage (file = 'shield.png'), 5: PhotoImage (file = 'guns.png')}
        self.arrow = {'red': PhotoImage(file = 'arrowr.png'), 'blue': PhotoImage(file = 'arrowl.png'), 'empty': PhotoImage(file = 'empty.png')}
        frame, number = ui.buildBoardDraw(self.background)
        arrow = ui.buildArrowButton(self)
        self.grid_cells = ui.gridCells(frame, number, arrow)
        ui.buildNewGameButton(self)
        self.score_label, self.coins_blue, self.coins_red, self.next_blue, self.next_red, self.arrow_blue, self.arrow_red = ui.buildPreview(self)
        self.iniGame()
        self.mainloop()

    def iniGame (self):
        self.game = bib.Game()
        self.user = chooseColor()
        self.ai = bib.changePlayer(self.user)
        ui.drawGridCellsButton(self)
        if self.user == 'red': 
            self.move = mcMove(self.game)
            self.game.moveGame(self.move)
            ui.drawGridCellsButton(self)    
    
    def selectMove (self, x, y, d):
        self.move = bib.Move(x, y, d)
        self.game.moveGame(self.move)
        if (self.game.max[self.user] == 6 or self.game.count[self.ai]==0): ui.gameOver(self, self.user)
        elif (self.game.cp == 0): ui.gameOver(self, 'yellow')
        else: 
            ui.drawGridCellsButton(self)
            self.move = mcMove(self.game)
            self.game.moveGame(self.move)
            if (self.game.max[self.ai] == 6 or self.game.count[self.user]==0): ui.gameOver(self, self.ai)
            elif (self.game.cp == 0): ui.gameOver(self, 'yellow')
            else: ui.drawGridCellsButton(self)

    def newGame(self):
        self.score_label.configure(text = '')
        self.grid_cells = ui.grayButtons(self.grid_cells)
        self.iniGame()
        