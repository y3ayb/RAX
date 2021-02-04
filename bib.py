from random import shuffle
from copy import deepcopy

DIM = 5             # Dimensão do tabuleiro: 5 por padrão
COINS_TRADE = 7

#Cada peça do jogo tem uma  peça, que aqui é um valor(número), e uma cor
class Block:
    def __init__ (self, value, color):
        self.value = value
        self.color = color

#O movimento precisa de uma direção. Aqui são definidas essas direção:
#w é cima, d é direita, s é baixo, a é esquerda. Essa estrutura é usada no movimento do bloco, principalmente pela rede neural
class Arrow:
    def __init__(self, w, d, s, a):
        self.w = w
        self.d = d
        self.s = s
        self.a = a

#No app orginal, o movimento é feito selecionando um bloco (com o dedo) e empurrando para alguma direção. Logo o movimento tem um posição (loc) e uma direção (dir)
class Move:
    def __init__ (self, x, y, d):
        self.x = x
        self.y = y
        self.d = d

def sortBlock (piece, player):
    if (piece == 0): block = Block(1, 'yellow')
    else: block = Block(piece, player)
    return block

'''Checa se um movimento é possível.
Blocos azuis podem se movimentar em direção de outro bloco azul, desde que tenha o mesmo valor ou em direção de um bloco com cor diferente, desde que tenha um valor maior.
Blocos amarelos podem se movimentar em direção de outro bloco amarelo com o mesmo valor.
#Verifica os movimentos possíveis'''
def moveIsPossible (blockSelected, blockNeighbor, player):
    if blockSelected.color == player:
        if blockNeighbor.color == player and blockNeighbor.value == blockSelected.value: psb = True
        elif blockNeighbor.color != player and blockNeighbor.value <= blockSelected.value: psb = True
        else: psb = False
    elif blockSelected.color == 'yellow':
        if blockNeighbor.color == 'yellow' and blockNeighbor.value == blockSelected.value: psb = True
        else: psb = False
    else: psb = False
    return psb

def changePlayer (player):
    if player == 'blue': newplayer = 'red'
    else: newplayer = 'blue'
    return newplayer

def createBoard ():
    A = []
    B = []
    for i in range (DIM): 
        B.append([])
        for j in range (DIM - 2): A.append(Block(1, 'yellow'))
        A.append(Block(i+1, 'blue'))
        A.append(Block(i+1, 'red'))
        for j in range (DIM): B[i].append(Block(0,'yellow'))
    A[0] = Block(1, 'red')
    valid = True
    while valid:
        shuffle(A)
        for i in range (DIM):
            for j in range (DIM): 
                B[i][j] = A[DIM*i+j]
                if B[i][j].value == 5: q = [i,j]
        if (q[0]!=0 and B[q[0]-1][q[1]].value!=5) and (q[1]!=0 and B[q[0]][q[1]-1].value!=5): valid = False
    return B

# retorna uma matriz de Arrow zerada    
def iniMatrixArrow ():
    P = []
    for i in range(DIM): 
        P.append([])
        for j in range (DIM): P[i].append(Arrow(False, False, False, False))
    return P

def iniPlayer (n):
    ini = {'blue': n, 'red': n}
    return ini

def tradeCoins (blockSel, blockNei, coin):
    naxt = 0
    newcoin = coin
    if blockNei.color == 'yellow' and blockSel.color != 'yellow': 
        naxt = (coin + 2**blockNei.value - 1)//COINS_TRADE
        newcoin = (coin + 2**blockNei.value - 1)%COINS_TRADE
    return naxt, newcoin

#Realiza o movimento para cima. Retorna uma matriz de blocos
def moveUp (B, x, block):
    A = deepcopy(B)
    aux = A[x]
    if A[x-1].color == A[x].color: aux.value = aux.value + 1
    if x != DIM-1:
        for i in range (DIM-1 - x): A[i+x] = A[i+1+x]
    A[DIM-1] = block
    A[x-1] = aux
    return A

#Realiza o movimento para direita. Retorna uma matriz de blocos
def moveRight (B, y, block):
    A = deepcopy(B)
    aux = A[y]
    if A[y+1].color == A[y].color: aux.value = aux.value + 1
    if y != 0:
        for i in range (y): A[y-i] = A[y-i-1]
    A[0] = block
    A[y+1] = aux
    return A

#Realiza o movimento para baixo. Retorna uma matriz de blocos
def moveDown (B, x, block):
    A = deepcopy(B)
    aux = A[x]
    if A[x+1].color == A[x].color: aux.value = aux.value + 1
    if x != 0:
        for i in range (x): A[x-i] = A[x-i-1]
    A[0] = block
    A[x+1] = aux
    return A

#Realiza o movimento para esquerda. Retorna uma matriz de blocos
def moveLeft (B, y, block):
    A = deepcopy(B)
    aux = A[y]
    if A[y-1].color == A[y].color: aux.value = aux.value + 1
    if y != DIM - 1:
        for i in range(DIM - 1 - y): A[y+i] = A[y+i+1]
    A[DIM - 1] = block
    A[y-1] = aux
    return A

'''Essa classe é composta pelo tabuleiro (B, que é uma matriz de blocos), as possibilidades de movimento (P, que é uma matriz de Arrow),
a quantidade de movimentos cm, que inicialmente é 0, o nível lvl, que inicialmente é 2, e a quantidade de movimentos possiveis cp, que será calculada.'''
class Game:
    def __init__ (self):
        self.cm = 0
        self.coins = iniPlayer(0)
        self.next = iniPlayer(0)
        self.count = iniPlayer(5)
        self.max = iniPlayer(5)
        self.player = 'blue'
        self.B = createBoard()
        self.P = iniMatrixArrow()
        self.findPossibilities('blue')
      
    # Acha os movimento possíveis do jogo
    def findPossibilities (self, player):  
        self.cp = 0  
        for i in range (DIM - 1):
            for j in range (DIM):
                self.P[i+1][j].w = moveIsPossible(self.B[i+1][j], self.B[i][j], player)    #Movimento para cima
                if self.P[i+1][j].w == True: self.cp = self.cp + 1
                self.P[j][i].d = moveIsPossible(self.B[j][i], self.B[j][i+1], player)      #Movimento para direita
                if self.P[j][i].d == True: self.cp = self.cp + 1
                self.P[i][j].s = moveIsPossible(self.B[i][j], self.B[i+1][j], player)      #Movimento para baixo
                if self.P[i][j].s == True: self.cp = self.cp + 1
                self.P[j][i+1].a = moveIsPossible(self.B[j][i+1], self.B[j][i], player)    #Movimento para esquerda
                if self.P[j][i+1].a == True: self.cp = self.cp + 1

    #Realiza o movimento no tabuleiro
    def modBoard (self, move):
        self.cm = self.cm + 1
        block = sortBlock(self.next[self.player], self.player)
        if move.d == 'w': 
            self.next[self.player], self.coins[self.player] = tradeCoins(self.B[move.x][move.y], self.B[move.x-1][move.y], self.coins[self.player])
            A = []
            for i in range (DIM): A.append(self.B[i][move.y])
            A = moveUp(A, move.x, block)
            for i in range (DIM): self.B[i][move.y] = A[i]
        if move.d == 'd': 
            self.next[self.player], self.coins[self.player] = tradeCoins(self.B[move.x][move.y], self.B[move.x][move.y+1], self.coins[self.player])
            self.B[move.x] = moveRight(self.B[move.x], move.y, block)
        if move.d == 's':
            self.next[self.player], self.coins[self.player] = tradeCoins(self.B[move.x][move.y], self.B[move.x+1][move.y], self.coins[self.player]) 
            A = []
            for i in range (DIM): A.append(self.B[i][move.y])
            A = moveDown(A, move.x, block)
            for i in range (DIM): self.B[i][move.y] = A[i]
        if move.d == 'a': 
            self.next[self.player], self.coins[self.player] = tradeCoins(self.B[move.x][move.y], self.B[move.x][move.y-1], self.coins[self.player])
            self.B[move.x] = moveLeft(self.B[move.x], move.y, block) 
        self.count = iniPlayer(0)
        self.max = iniPlayer(0)  
        for i in range (DIM):
            for j in range (DIM):
                if self.B[i][j].color == 'blue':
                    self.count['blue'] = self.count['blue'] + 1
                    if self.B[i][j].value > self.max['blue']: self.max['blue'] = self.B[i][j].value
                if self.B[i][j].color == 'red':
                    self.count['red'] = self.count['red'] + 1
                    if self.B[i][j].value > self.max['red']: self.max['red'] = self.B[i][j].value                        
    
    # Move o tabuleiro e já acha os movimentos possíveis
    def moveGame (self, move):
        self.modBoard(move)
        self.player = changePlayer(self.player)
        self.findPossibilities(self.player)
        return self
