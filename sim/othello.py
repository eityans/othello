import random
import time
import math
import tkinter
from tkinter import messagebox

SPACE = 0
BLACK = 1
WHITE = -1

CELL_LENGTH = 8
BOARD_PX_SIZE = 500
CELL_PX_SIZE = BOARD_PX_SIZE / CELL_LENGTH
PADDING = 4 if CELL_PX_SIZE>20 else 1

class Position:
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x

    def is_inner(self, y, x):
        if y >= 0 and x >= 0 and y < CELL_LENGTH and x < CELL_LENGTH:
            return True
        else:
            return False


class Board:
    DIR = [ [-1, -1], [-1, 0],  [-1, 1],
            [0, -1],            [0, 1],
            [1, -1],  [1, 0],   [1, 1]]
    def __init__(self):
        self.board = [[SPACE for i in range(CELL_LENGTH)] for j in range(CELL_LENGTH)]
        self.turn = BLACK
        self.move_num = 1
        self.reverse_num = 0

    def init_board(self):
        for y in range(CELL_LENGTH):
            for x in range(CELL_LENGTH):
                self.board[y][x] = SPACE
        self.board[int(CELL_LENGTH/2 - 1)][int(CELL_LENGTH/2 -1)] = WHITE
        self.board[int(CELL_LENGTH/2 - 1)][int(CELL_LENGTH/2)] = BLACK
        self.board[int(CELL_LENGTH/2)][int(CELL_LENGTH/2 - 1)] = BLACK
        self.board[int(CELL_LENGTH/2)][int(CELL_LENGTH/2)] = WHITE

        self.turn = BLACK
        self.move_num = 1
        self.reverse_num = 0

    def get_discs(self):
        black_discs = 0
        white_discs = 0
        for y in range(CELL_LENGTH):
            for x in range(CELL_LENGTH):
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
        for y in range(CELL_LENGTH):
            for x in range(CELL_LENGTH):
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
                        self.reverse_num += 1
                        y -= dir[0]
                        x -= dir[1]
        
        self.turn = -self.turn
        self.move_num += 1


    def move_pass(self):
        self.turn = -self.turn

    def is_game_end(self):
        if self.move_num == CELL_LENGTH * CELL_LENGTH -3:
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

    def get_reverse_num(self):
        return self.reverse_num

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

        if self.board.is_game_end():
            #print("黒： %d  白： %d" %(self.board.get_discs()))
            print(self.board.get_reverse_num())
            self.game_mode = 2
            #messagebox.showinfo(u"", u"対局終了")
            return

        move_list = self.board.get_move_list()
        if len(move_list) == 0:
            self.board.move_pass()
            #messagebox.showinfo(u"パス", u"打てる場所がないのでパスします")

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





    


