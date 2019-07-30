import random
import time
import math
import tkinter
from tkinter import messagebox

SPACE = 0
BLACK = 1
WHITE = -1

BOARD_PX_SIZE = 500
CELL_PX_SIZE = BOARD_PX_SIZE / 8

class Position:
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x

    def is_inner(self, y, x):
        if y >= 0 and x >= 0 and y < 8 and x < 8:
            return True
        else:
            return False


class Board:
    DIR = [ [-1, -1], [-1, 0],  [-1, 1],
            [0, -1],            [0, 1],
            [1, -1],  [1, 0],   [1, 1]]
    def __init__(self):
        self.board = [[SPACE for i in range(8)] for j in range(8)]
        self.turn = BLACK
        self.move_num = 1

    def init_board(self):
        for y in range(8):
            for x in range(8):
                self.board[y][x] = SPACE
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE

        self.turn = BLACK
        self.move_num = 1

    def get_discs(self):
        black_discs = 0
        white_discs = 0
        for y in range(8):
            for x in range(8):
                disc = self.board[y][x]
                if disc == BLACK:
                    black_discs += 1
                elif disc == WHITE:
                    white_discs += 1
        return (black_discs, white_discs)

    #指定のマスに打てるならtrueを返す
    def is_movable(self, position):
        if self.board[position.y][position.x] != SPACE:
            return False
        
        for dir in Board.DIR:
            y = position.y + dir[0]
            x = position.x + dir[1]
            newP = Position(y,x)
            if newP.is_inner(y, x) and self.board[y][x] == -self.turn:
                y += dir[0]
                x += dir[1]
                while newP.is_inner(y, x) and self.board[y][x] == -self.turn:
                    y += dir[0]
                    x += dir[1]
                if newP.is_inner(y, x) and self.board[y][x] == self.turn:
                    return True
        
        return False

    def get_move_list(self):
        move_list = []
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == SPACE:
                    position = Position(y,x)
                    if self.is_movable(position):
                        move_list.append(position)
        return move_list

    #1手すすめる
    def move(self, position):
        self.board[position.y][position.x] = self.turn

        for dir in Board.DIR:
            y = position.y + dir[0]
            x = position.x + dir[1]
            newP = Position(y,x)
            if newP.is_inner(y, x) and self.board[y][x] == -self.turn:
                y += dir[0]
                x += dir[1]
                while newP.is_inner(y, x) and self.board[y][x] == -self.turn:
                    y += dir[0]
                    x += dir[1]
                if newP.is_inner(y, x) and self.board[y][x] == self.turn:
                    #返せることがわかったので、石をひっくり返しながら来た方向へ戻る
                    y -= dir[0]
                    x -= dir[1]
                    while newP.is_inner(y, x) and self.board[y][x] == -self.turn:
                        self.board[y][x] = self.turn
                        y -= dir[0]
                        x -= dir[1]
        
        self.turn = -self.turn
        self.move_num += 1


    def move_pass(self):
        self.turn = -self.turn

    def is_game_end(self):
        if self.move_num == 61:
            return True
        (black_disks, white_disks) = self.get_discs()
        if black_disks == 0 or white_disks == 0:
            return True
        
        move_list1 = self.get_move_list()
        if len(move_list1) == 0:
            self.move_pass()
            move_list2 = self.get_move_list()
            self.move_pass()
            if len(move_list2) == 0:
                return True
        
        return False

class Game:
    def __init__(self):
        #ゲームの状態 0:対局まち 1:対局中 2:対局終了
        self.game_mode = 0
        #● 0:人間 1:コンピュータ
        self.black_player = 0
        self.white_player = 0
        
        self.board = Board()
        self.board.init_board()

    def start(self, _black_player, _white_player):
        self.black_player = _black_player
        self.white_player = _white_player
        self.game_mode = 1
        self.board.init_board()

    def game_move(self, position):
        self.board.move(position)
        draw_board()

        if self.board.is_game_end():
            self.game_mode = 2
            disp_mess()
            messagebox.showinfo(u"", u"対局終了")
            return

        move_list = self.board.get_move_list()
        if len(move_list) == 0:
            self.board.move_pass()
            messagebox.showinfo(u"パス", u"打てる場所がないのでパスします")
        disp_mess()

    #次の手番がPCならtrueを返す
    def is_com_turn(self):
        if self.board.turn ==  BLACK and self.black_player == 1 or self.board.turn == WHITE and self.white_player == 1:
            return True
        return False

    #手番がコンピュータならば、指し手を選択させる
    def proc_com_turn(self):
        while True:
            if self.is_com_turn():
                position = AI().select_move(self.board)
                self.game_move(position)
                if self.game_mode == 2 :
                    break
            else:
                break

class AI:
    def select_move(self, board):
        move_list = board.get_move_list()
        r = random.randint(0, len(move_list)-1)
        return move_list[r]
    
def draw_board():
    global game 
    global canvas_board

    canvas_board.delete('all')
    #背景
    canvas_board.create_rectangle(0, 0, BOARD_PX_SIZE, BOARD_PX_SIZE, fill = '#00a000')
    #石
    for y in range(8):
        for x in range(8):
            disc = game.board.board[y][x]
            if disc != SPACE:
                if disc == BLACK:
                    color = "black"
                else:
                    color = "white"
                canvas_board.create_oval(x*CELL_PX_SIZE+4, y*CELL_PX_SIZE+4, (x+1)*CELL_PX_SIZE-4, (y+1)*CELL_PX_SIZE-4, fill=color)
    #枠
    for x in range(8):
        canvas_board.create_line(x*CELL_PX_SIZE, 0, x*CELL_PX_SIZE, BOARD_PX_SIZE, fill="black", width=1)
    for y in range(8):
        canvas_board.create_line(0, y*CELL_PX_SIZE, BOARD_PX_SIZE, y*CELL_PX_SIZE, fill="black", width=1)
    
    canvas_board.update()

def disp_mess():
    global game
    global mess_var

    mess = ""
    if game.game_mode == 0:
        mess = u"対局を開始してください"
    elif game.game_mode == 1:
        mess = u"対局中"
        mess += str(game.board.move_num) + u"手目 "
        if game.board.turn == BLACK:
            mess += u"黒番"
        else:
            mess += u"白番"
        
        (black_discs, white_discs) = game.board.get_discs()
        mess += " 黒:" + str(black_discs) + " 白：" + str(white_discs)

    elif game.game_mode == 2:
        (black_discs, white_discs) = game.board.get_discs()
        mess = u"対局終了 " + str(game.board.move_num-1) + u"手" + " 黒："+ str(black_discs) + " 白：" + str(white_discs)
        if black_discs == white_discs:
            mess += u" 引き分け"
        elif black_discs > white_discs:
            mess += u"黒の勝ち"
        else:
            mess += u"白の勝ち"
    mess_var.set(mess)

def play_start():
    global game
    global black_var, white_var

    black_player = black_var.get()
    white_player = white_var.get()

    game.start(black_player, white_player)
    disp_mess()
    draw_board()

    game.proc_com_turn()

def click_board(event):
    global game
    if game.game_mode != 1:
        messagebox.showinfo(u"", u"対局を開始してください")
        return
    y = math.floor(event.y / CELL_PX_SIZE)
    x = math.floor(event.x / CELL_PX_SIZE)
    position = Position(y, x)
    if game.board.is_movable(position) == False:
        messagebox.showinfo(u"", u"そこには打てません")
        return

    game.game_move(position)
    if game.game_mode == 2:
        return

    game.proc_com_turn()
    


root = tkinter.Tk()
root.title(u"オセロ")
window_width = BOARD_PX_SIZE + 32
window_height = BOARD_PX_SIZE + 88
root.geometry(str(window_width) + "x" + str(window_height))

canvas_board = tkinter.Canvas(root, width=BOARD_PX_SIZE, height=BOARD_PX_SIZE)
canvas_board.bind("<Button-1>", click_board)
canvas_board.place(x = 16, y = 72)

black_label = tkinter.Label(text=u"先手●")
black_label.place(x=16, y=4)
black_var =tkinter.IntVar()
black_rdo0 = tkinter.Radiobutton(root, value = 0, variable = black_var, text=u"プレーヤー")
black_rdo0.place(x=70, y=4)
black_rdo1 = tkinter.Radiobutton(root, value = 1, variable = black_var, text=u"コンピュータ")
black_rdo1.place(x=160, y=4)

white_label = tkinter.Label(text=u"後手○")
white_label.place(x=16, y=24)
white_var =tkinter.IntVar()
white_rdo0 = tkinter.Radiobutton(root, value = 0, variable = white_var, text=u"プレーヤー")
white_rdo0.place(x=70, y=24)
white_rdo1 = tkinter.Radiobutton(root, value = 1, variable = white_var, text=u"コンピュータ")
white_rdo1.place(x=160, y=24)

button_start = tkinter.Button(root, text=u"対局開始", width=15, command=play_start)
button_start.place(x=300, y=12)


#メッセージ欄
mess_var = tkinter.StringVar()
mess_label = tkinter.Label(root, textvariable = mess_var)
mess_label.place(x=16, y=48)

game = Game()
draw_board()
disp_mess()
root.mainloop()