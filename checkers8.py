# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 10:56:35 2017

@author: saniya 
"""

''' BOARD OBJECT'''
class PlayingBoard():
    def __init__(self):
        board = list(range(8))
        for x in board:
            yboard = ['-', '-', '-', '-', '-', '-', '-', '-']
            board[x]= yboard
        redplaces = [(0, 0), (0, 2), (1, 1), (2, 0), 
                          (2, 2), (3, 1), (4, 0), (4, 2), 
                          (5, 1), (6, 0), (6, 2), (7, 1)]
        blueplaces = [(0, 6), (1, 5), (1, 7), (2, 6), 
                           (3, 5), (3, 7), (4, 6), (5, 5), 
                           (5, 7), (6, 6), (7, 5), (7, 7)]
        allpieces = list()
        
        for i in range(12):
            board[redplaces[i][1]][redplaces[i][0]] = 'R'
            board[blueplaces[i][1]][blueplaces[i][0]] = 'B'
            allpieces.append(NormalPiece(redplaces[i][1], redplaces[i][0], 'Red'))
        for i in range(12):
            allpieces.append(NormalPiece(blueplaces[i][1], blueplaces[i][0], 'Blue'))
        
        self.allpieces = allpieces
        self.board = board
        self.bluepieces = allpieces[12:]
        self.redpieces = allpieces[:12]
       
    def print_board(self):
        Border = '------------------------------------------'
        Columns = '    A    B    C    D    E    F    G    H'
        Rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        print(Border)
        print(Columns)
        for i in range(8):
            print(Rows[i], self.board[i])
    def move_piece_on_board(self, piece, c, d):
        i = self.allpieces.index(piece)
        a = piece.x
        b = piece.y
        piece.x = c
        piece.y = d
        self.board[c][d] = self.board[a][b]
        self.board[a][b] = '-'
        self.allpieces[i] = piece
  
''' PIECE OBJECT'''

class Piece():
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.state = 'Alive'
   
    def read(self):
        print('X:', self.x, 'Y:', self.y, 'Team:', self.team, 'State:', self.state)
        
    def eaten(self, board):
        board.board[self.x][self.y] = '-'
        self.x = -1
        self.y = -1
        self.State = 'Dead'

''' NORMAL PIECE OBJECT''' 
class NormalPiece(Piece):
    def __init__(self):
        super(NormalPiece, self).__init__()
        self.kind = 'Normal'

'''STAR PIECE OBJECT'''
class StarPiece(Piece):
    pass


''' PLAYER OBJECT'''
class Player():
    def __init__(self, name, team):
        self.team = team
        self.name = name
        self.score = 0
    
    def get_current(self):
        ypos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        currentpos = input('Enter Current Position:')
        try: 
            a = int(currentpos[1])-1
        except ValueError:
            print('Current Position in wrong format, Try again')
            self.get_current()
        try:
            b = ypos.index((currentpos[0]).upper())
        except ValueError:
            print('Current Position in wrong format, Try again')
            self.get_current()
        current = []
        current.append(a)
        current.append(b)
        return(current)
        
    def get_desired(self):
        ypos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        desiredpos = input('Enter Desired Position:')
        try: 
            c = int(desiredpos[1])-1
        except ValueError:
            print('Desired Position in wrong format, Try again')
            self.get_desired()
        try: 
            d = ypos.index((desiredpos[0]).upper())
        except ValueError:
            print('Desired Position in wrong format, Try again')
            self.get_desired()
        desired = []
        desired.append(c)
        desired.append(d)
        return(desired)
            
            
        
    def move_piece(self, Board):
        current = self.get_current()
        desired = self.get_desired()
        a = current[0]
        b = current[1]
        c = desired[0]
        d = desired[1]
        if Board.board[a][b] != '-':
            piece = self.find_piece(Board, a, b)
            if self.my_piece(piece, Board) and self.valid_move(piece, c, d, Board):
                Board.move_piece_on_board(piece, c, d)
                piece.x = c
                piece.y = d
        else:
            print('Error, no piece found, Try again')
            self.move_piece(Board)

    def find_piece(self, board, a, b):
        for object in board.allpieces:
            if object.x == a and object.y == b:
                return object
            
    def is_empty(self, board, a, b):
        for object in board.allpieces:
            if (object.x != a) and (object.y != b):
                continue
            else: 
                break
        return '-'
            
    def my_piece(self, piece, board):
        if piece.team == self.team:
            return True
        else:
            print('Error: Piece selected does not belong to Player, Try again')
            self.move_piece(board)
    
    def valid_move(self, piece, c, d, board):
        r = 0
        a = piece.x
        b = piece.y
        otherteam = ''
        if self.team == 'Red': 
            r = 1 
            otherteam = 'Blue'
        if self.team == 'Blue': 
            r = -1
            otherteam = 'Red'
        
        if self.is_empty(board, c, d) == '-':
            if c-a == 1*r and abs(d-b) == 1:
                return True
            elif c-a == 2*r and abs(d-b) == 2:
                if (self.find_piece(board, a +1*r, b+1)).team == otherteam:
                   (self.find_piece(board, a +1*r, b+1)).eaten(board)
                   self.score = self.score + 1
                   return True
                elif (self.find_piece(board, a +1*r, b-1)).team == otherteam:
                    (self.find_piece(board, a +1*r, b-1)).eaten(board)
                    self.score = self.score + 1
                    return True
            else:
                print('This is not a valid move, Try again')
                self.move_piece(board)
        
    
''' GAME OBJECT
This takes the names of both players, creates the board, creates player objects
and prints the board'''
class Game():
    def __init__(self):
        RedPlayerName = input('Name of Red Player:')
        BluePlayerName = input('Name of Blue Player:')
        newBoard = PlayingBoard()
        self.Board = newBoard
        RedPlayer = Player(RedPlayerName, 'Red')
        self.RedPlayer = RedPlayer
        BluePlayer = Player(BluePlayerName, 'Blue')
        self.BluePlayer = BluePlayer
        self.Board.print_board()
        
    def print_score(self):
        print('\n Red Player Score:', self.RedPlayer.score, 'Blue Player Score:', self.BluePlayer.score)
        
    def game_play(self):
        for x in range(50):
            print('\n Red Player Turn')
            self.RedPlayer.move_piece(self.Board)
            self.Board.print_board()
            self.print_score()
            print('\n Blue Player Turn')
            self.BluePlayer.move_piece(self.Board)
            self.Board.print_board()
            self.print_score()


newGame = Game()
newGame.game_play()


        