import bib
from tkinter import Frame, Label, Button

EDGE_LENGTH = 600       #Tamanho da tela
CELL_PAD = 10           #Distância entre os blocos
ARROW_PAD = 75          #Posição da seta dentro do bloco
NEW_GAME_PAD = 50       #Tamanho do placar
BOARD_BD = 10           #Tamanho da borda do tabuleiro
SCORE_POS_RX = 0.92     #Posição relativa do placar na horizontal (.5 significa no meio)
SCORE_POS_Y = 30        #Posição do placar na vertical
PREVIEW_POS_RX = .5
PREVIEW_POS_Y = 796
PREVIEW_PAD = 50
COIN_PAD = 20           #Posição da contagem de moedas
NEXT_PAD = 250          #Posição de onde mostra a proxima peça

LABEL_FONT = ('Calibri', 20, 'bold')            #Fonte do bloco
ARROW_FONT = ('Calibri', 10)                    #Fonte da direção
SCORE_LABEL_FONT = ('Helvetica', 20, 'bold')    #Fonte do placar
SCORE_FONT = ('Helvetica', 24, 'bold')          #Fonte do palavra "pontuação"

GAME_COLOR = 'white'                                                    #Cor do fundo do tabuleiro
LABEL_COLORS = {'blue': 'white', 'yellow': 'black', 'red': 'black'}     #Cor das letras dos blocos
ARROW_COLOR = 'gray'
ARROW_MOVE_COLOR = 'lightyellow'

BUTTON_PAD = 75
BUTTON_FONT = ("Calibri", 10)
BUTTON_STATE = {True: "normal", False: "disable"}

def head (display):
    display.grid()                      #Constrói a janela, 
    display.master.title('RAX')      #a barra de título e 
    display.score = []                  #também a lista onde ficará guadada as pontuções
    return display

def bg (display):
    background = Frame(display, bg=GAME_COLOR, bd = BOARD_BD, width=EDGE_LENGTH, height=EDGE_LENGTH)    #Cria o local do tabuleiro
    background.grid(pady = (NEW_GAME_PAD, PREVIEW_PAD), padx = CELL_PAD)                                #Coloca o tabuleiro no lugar certo
    return background

#Cria os locais dos blocos, cada cell é um lugar para um bloco
def buildBoardDraw(background):
    grid = []
    val = []
    for i in range(bib.DIM):
        grid.append([])
        val.append([])
        for j in range(bib.DIM):
            cell = Frame(background, width=EDGE_LENGTH/bib.DIM, height=EDGE_LENGTH/bib.DIM)
            cell.grid(row=i, column=j, padx=CELL_PAD, pady=CELL_PAD)
            grid[i].append(cell)
            t = Label(background, font=LABEL_FONT)
            t.grid(row=i, column = j)
            val[i].append(t)
    return grid, val

def buildNewGameButton (display):
    score_frame = Frame(display)
    score_frame.place(relx=SCORE_POS_RX, y=SCORE_POS_Y, anchor='center')
    new_game = Button (score_frame, text = 'Novo Jogo', command=display.newGame)
    new_game.grid()

#Cria o placar
def buildPreview (display):
    score_frame = Frame(display)
    score_frame.place(relx=PREVIEW_POS_RX, y=PREVIEW_POS_Y, anchor='center')
    coins_blue = Label (score_frame, text = '0', font = SCORE_LABEL_FONT, fg = 'blue')
    coins_blue.grid (row = 1, column = 0, padx=(0,COIN_PAD))
    next_blue = Label (score_frame, text = '0', font = SCORE_LABEL_FONT, fg = 'blue')
    next_blue.grid (row = 1, column = 1, padx=(0,NEXT_PAD))
    score_label = Label(score_frame, text = '', font = SCORE_FONT)
    score_label.grid(row=1, column = 2)
    next_red = Label(score_frame, text = '0', font = SCORE_LABEL_FONT, fg = 'red')
    next_red.grid(row = 1, column = 3, padx=(NEXT_PAD,0))
    coins_red = Label(score_frame, text = '0', font = SCORE_LABEL_FONT, fg = 'red')
    coins_red.grid(row = 1, column = 4, padx=(COIN_PAD,0))
    return score_label, coins_blue, coins_red, next_blue, next_red

#Cria uma matriz com todas as propriedades dos blocos, inclusive as direções mostrando os movimentos possíveis
def gridCells (frame, number, arrow):
    grid_cells = []
    for i in range(bib.DIM):
        grid_row = []
        for j in range(bib.DIM):
            cell_data = {'frame': frame[i][j], 'number': number[i][j], 'w': arrow[i][j].w, 'd': arrow[i][j].d, 's': arrow[i][j].s, 'a': arrow[i][j].a}
            grid_row.append(cell_data)
        grid_cells.append(grid_row)
    return grid_cells

def buildButton (display, x, y, d):
    b = Button(display.background, bg = "white", text= d, padx=8, font=BUTTON_FONT, relief = "flat", bd = 0, command = lambda: display.selectMove (x, y, d))
    if d == 'w': b.grid(row=x, column=y, pady=(0,BUTTON_PAD))
    elif d == 'd': b.grid(row=x, column=y, padx=(BUTTON_PAD,0))
    elif d == 's': b.grid(row=x, column=y, pady=(BUTTON_PAD,0))
    else: b.grid(row=x, column=y, padx=(0,BUTTON_PAD))
    return b

def buildArrowButton(display):
    grid = []
    for i in range(bib.DIM):
        grid.append([])
        for j in range(bib.DIM):
            move_w = buildButton(display, i, j, 'w')
            move_d = buildButton(display, i, j, 'd')
            move_s = buildButton(display, i, j, 's')
            move_a = buildButton(display, i, j, 'a')
            grid[i].append(bib.Arrow(move_w, move_d, move_s, move_a))
    return grid

def configureGridCells (game, pieces, coins, grid_cells):
    for i in range(bib.DIM):
        for j in range(bib.DIM):
                tile_value = game.B[i][j].value
                tile_color = game.B[i][j].color
                if tile_color == 'yellow': grid_cells[i][j]["number"].configure(image = coins[tile_value], bg=tile_color, fg=LABEL_COLORS[tile_color])
                else: grid_cells[i][j]["number"].configure(image = pieces[tile_value], bg=tile_color, fg=LABEL_COLORS[tile_color])
                grid_cells[i][j]["frame"].configure(bg=tile_color)
                grid_cells[i][j]["w"].configure(state = BUTTON_STATE[game.P[i][j].w])
                grid_cells[i][j]["d"].configure(state = BUTTON_STATE[game.P[i][j].d])
                grid_cells[i][j]["s"].configure(state = BUTTON_STATE[game.P[i][j].s])
                grid_cells[i][j]["a"].configure(state = BUTTON_STATE[game.P[i][j].a])
    return grid_cells

def grayButtons (grid_cells):
    for i in range(bib.DIM):
        for j in range(bib.DIM):
                grid_cells[i][j]["w"].configure(bg = "white")
                grid_cells[i][j]["d"].configure(bg = "white")
                grid_cells[i][j]["s"].configure(bg = "white")
                grid_cells[i][j]["a"].configure(bg = "white")
    return grid_cells

def configureGameOver (game, grid_cells, pieces, coins):
    for i in range(bib.DIM):
        for j in range(bib.DIM):
                tile_value = game.B[i][j].value
                tile_color = game.B[i][j].color
                if tile_color == 'yellow': grid_cells[i][j]["number"].configure(image = coins[tile_value], bg=tile_color, fg=LABEL_COLORS[tile_color])
                else: grid_cells[i][j]["number"].configure(image = pieces[tile_value], bg=tile_color, fg=LABEL_COLORS[tile_color])
                grid_cells[i][j]["frame"].configure(bg=tile_color)
                grid_cells[i][j]["w"].configure(state = 'disable', bg=tile_color)
                grid_cells[i][j]["d"].configure(state = 'disable', bg=tile_color)
                grid_cells[i][j]["s"].configure(state = 'disable', bg=tile_color)
                grid_cells[i][j]["a"].configure(state = 'disable', bg=tile_color)
    return grid_cells

        
def drawGridCellsButton(display):
    display.grid_cells = configureGridCells(display.game, display.pieces, display.coins, display.grid_cells)
    display.coins_blue.configure(text = str(display.game.coins['blue']))
    display.next_blue.configure(image = display.pieces[display.game.next['blue']])
    display.next_red.configure(image = display.pieces[display.game.next['red']])
    display.coins_red.configure(text = str(display.game.next['red']))
    display.update_idletasks()

def gameOver (display, player):
    display.grid_cells = configureGameOver(display.game, display.grid_cells, display.pieces, display.coins)
    display.coins_blue.configure(text = '')
    display.coins_red.configure (text = '')
    display.next_blue.configure(image = display.pieces[7])
    display.next_red.configure(image = display.pieces[7])
    if (player == 'blue'): display.score_label.configure(text = 'Azul venceu!', fg = 'blue')
    elif (player == 'red'): display.score_label.configure(text = 'Vermelho venceu!', fg = 'red')
    else: display.score_label.configure(text = 'Empate!')
    display.update_idletasks()
