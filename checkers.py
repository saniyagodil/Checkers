# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 10:56:35 2017

@author: saniya 
"""

class Board():

    '''
    Method initializes board which is displayed using a nested list, creating piece objects in the starting positions
    R for red pieces, B for blue pieces and - for empty positions
    '''
    def __init__(self):
        self.boarddisp = list(range(8))
        for x in self.boarddisp:
            yboarddisp = ['-', '-', '-', '-', '-', '-', '-', '-']
            self.boarddisp[x]= yboarddisp
        self.allpieces = list()

        #Starting coordinates for red and blue pieces
        redlocation = [(0, 0), (0, 2), (1, 1), (2, 0), 
                          (2, 2), (3, 1), (4, 0), (4, 2), 
                          (5, 1), (6, 0), (6, 2), (7, 1)]
        bluelocation = [(0, 6), (1, 5), (1, 7), (2, 6), 
                           (3, 5), (3, 7), (4, 6), (5, 5), 
                           (5, 7), (6, 6), (7, 5), (7, 7)]
        
        for i in range(12):
            self.boarddisp[redlocation[i][1]][redlocation[i][0]] = 'R'         
            self.allpieces.append(Piece(redlocation[i][1], redlocation[i][0], 'Red'))
            self.boarddisp[bluelocation[i][1]][bluelocation[i][0]] = 'B'
            self.allpieces.append(Piece(bluelocation[i][1], bluelocation[i][0], 'Blue')) 

    '''
    This method prints the legend (A-H, 1-8) as well as the positions of pieces on board
    R for Red piece, B for Blue piece, - for empty spot
    '''   
    def print_board(self):
        Border = '------------------------------------------'
        Columns = '    A    B    C    D    E    F    G    H'
        Rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        print(Border)
        print(Columns)
        for i in range(8):
            print(Rows[i], self.boarddisp[i])

    '''
    This method moves the piece on board by updating the board display with the new location of the piece (/empty spot)
    as well as changing the piece's characteristics (x,y) and updating the allpieces list
    '''
    def move_piece_on_board(self, piece, c, d):
        i = self.allpieces.index(piece)
        self.boarddisp[c][d] = self.boarddisp[piece.x][piece.y]
        self.boarddisp[piece.x][piece.y] = '-'
        piece.x = c
        piece.y = d
        self.allpieces[i] = piece   

    '''
    This method checks to see if there is a piece present on a given board position
    '''
    def is_empty(self, a, b):
        return self.boarddisp[a][b] == '-':

    def find_piece(self, a, b):
        for object in self.allpieces:
            if object.x == a and object.y == b:
                return object
  
class Piece():
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.state = 'Alive'
   
    '''
    Method removes piece from board display, changes the properties of the piece object 
    Using (-1, -1) to mean not on board/dead
    '''
    def eaten(self, board):
        board.boarddisp[self.x][self.y] = '-'
        self.x = -1
        self.y = -1
        self.state = 'Dead'

    def potential_moves(self):
        # Iterate over all non-'Dead' pieces

    def valid_move(self, c, d, board):
        r = 0
        a = self.x
        b = self.y
        otherteam = ''
        if self.team == 'Red': 
            r = 1 
        if self.team == 'Blue': 
            r = -1
        
        if board.is_empty(c, d):
            if c - a == 1 * r and abs(d - b) == 1:
                return True
            elif c - a == 2 * r and abs(d - b) == 2:
                if (board.find_piece(a + 1 * r, b + 1)).team != self.team:
                   (board.find_piece(a + 1 * r, b + 1)).eaten(board)
                   self.score = self.score + 1
                   return True
                elif (board.find_piece(a + 1 * r, b - 1)).team != self.team:
                    (board.find_piece(a + 1 * r, b - 1)).eaten(board)
                    self.score = self.score + 1
                    return True
            else:
                print('This is not a valid move, Try again')
                self.move_piece(board)

# should overrite some methods in the piece class
class StarPiece(Piece):
    pass

class Player():

    '''
    Initializes player object, Team: Red/Blue
    '''
    def __init__(self, name, team):
        self.team = team
        self.name = name
        self.score = 0
    
    def get_current(self):
        return self.get_input('Current Position')
        
    def get_desired(self):
        return self.get_input('Desired Position')

    def get_input(self, str):
        ypos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        pos = input('Enter ' + str + ':')
        try: 
            a = int(pos[1])-1
        except ValueError:
            print(str + ' in wrong format, Try again')
            self.get_input(str)
        # maybe ensure that it is betwen 0 and 7 ???
        try:
            b = ypos.index((pos[0]).upper())
        except ValueError:
            print(str + ' in wrong format, Try again')
            self.get_input(str)
        return([a,b])
        
    def move_piece(self, board):
        [a,b] = self.get_current()
        [c,d] = self.get_desired()
        if board.boarddisp[a][b] != '-':
            piece = board.find_piece(a, b)
            if self.my_piece(piece, board) and piece.valid_move(c, d, board):
                board.move_piece_on_board(piece, c, d)
                piece.x = c
                piece.y = d
        else:
            print('Error, no piece found, Try again')
            self.move_piece(board)       

    '''
    Method varifies that the piece belongs to the player trying to move it
    '''
    def my_piece(self, piece, board):
        if piece.team == self.team:
            return True
        else:
            print('Error: Piece selected does not belong to Player, Try again')
            self.move_piece(board)
    
'''
This takes the names of both players, creates the board, creates player objects
and prints the board
'''
class Game():
    def __init__(self):
        self.PlayingBoard = Board()
        self.RedPlayer    = Player(input('Name of Red Player:'), 'Red')
        self.BluePlayer   = Player(input('Name of Blue Player:'), 'Blue')
        
    def print_score(self):
        print('\n Red Player Score:', self.RedPlayer.score, 'Blue Player Score:', self.BluePlayer.score)
        
    def play(self):
        # temporary 50, until i create a method to determine end of game
        for x in range(50):
            self.PlayingBoard.print_board()
            self.print_score()
            player = self.RedPLayer if x % 2 == 0 else self.BluePlayer
            print('\n ' + player.team + ' Player Turn')
            player.move_piece(self.PlayingBoard)

Game().play()