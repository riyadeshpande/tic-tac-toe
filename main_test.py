import pygame
import sys
import numpy as np
import random
import copy

from constant import *
#asterisk means we import all the content from constants file

#tip: pygame coordinates are like 4th quadrant
#x axis increases left to right
#y axis increases top to bottom

#pygame setup:
pygame.init()
screen = pygame.display.set_mode((width, height)) #screen will be of 600x600
pygame.display.set_caption('TIC-TAC-TOE AI')
screen.fill(bg_colour)

# -----CLASSES-----

class Board:

    def __init__(self):
        self.squares = np.zeros( (rows, cols) )
        #print(self.squares)
        self.empty_sqrs = self.squares #list of empty squares
        self.marked_sqrs = 0 #to keep a count of all the marked squares,
        #will help us know when our board is full

    def final_state(self, show = False):
        '''

        #return 0 if there is no win yet
        #this doesn't mean there's a draw
        #for draw, we need to check if the board is full AND there is no win

        #return 1 if player 1 wins
        #return 2 if player 2 wins

        '''

        #vertical wins
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
                if show:
                    colour = circ_colour if self.squares[0][col] == 2 else cross_colour
                    initial_pos = (col*sqsize + sqsize//2, 20) #20 is offset
                    final_pos = (col*sqsize + sqsize//2, height-20)
                    pygame.draw.line(screen, colour, initial_pos, final_pos, line_width)
                return self.squares[0][col]

        #horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    colour = circ_colour if self.squares[row][0] == 2 else cross_colour
                    initial_pos = (20, row*sqsize + sqsize//2) #20 is offset
                    final_pos = (width-20, row*sqsize + sqsize//2)
                    pygame.draw.line(screen, colour, initial_pos, final_pos, line_width)
                return self.squares[row][0]

        #desc diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
            if show:
                colour = circ_colour if self.squares[0][0] == 2 else cross_colour
                initial_pos = (20, 20)  # 20 is offset
                final_pos = (width-20, height-20)
                pygame.draw.line(screen, colour, initial_pos, final_pos, line_width)
            return self.squares[0][0]

        #asc diagonal win
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] !=0:
            if show:
                colour = circ_colour if self.squares[0][2] == 2 else cross_colour
                initial_pos = (20, height-20)  # 20 is offset
                final_pos = (width-20, 20)
                pygame.draw.line(screen, colour, initial_pos, final_pos, line_width)
            return self.squares[0][2]

        #no win yet
        return 0


    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs +=1

    def empty_sqr(self, row, col):
        return (self.squares[row][col] == 0)

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
                    #print(empty_sqrs)

        return empty_sqrs

    def isfull(self):
        return (self.marked_sqrs==9)

  #  def isempty(self):
  #      return (self.marked_sqrs==0)


class AI:
    def __init__(self, level=1, player=2): #level=0 means random ai, level=1 means minimax algo, by default, ai is player 2
        self.level = level
        self.player = player

    # -----RANDOM-----
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        #idx = random.randrange(0, len(empty_sqrs))
        #return empty_sqrs[idx]
        return random.choice(empty_sqrs) #will return any random tuple of row,col from a list of all available empty squares

    #-----MINIMAX-----
    def minimax(self, board, alpha, beta, maximizingPlayer):
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull() and case == 0 : #case==0 is actually kind of redundant as if board is full, and player 1 and player 2 haven't won, then obviously case=0, but i put it just to be safe
            return 0, None

        if maximizingPlayer:
            max_eval = -10
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, alpha, beta, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    #depth

                alpha = max (eval, alpha)
                if beta <= alpha:
                    break

            return max_eval, best_move

        elif not maximizingPlayer:
            min_eval = 10
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, alpha, beta, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col) #keeping best move inside this if condition is very important
                    #if we do min_eval= min(min_eval, eval) without the if condition, then the best move will be every iteration's row,col
                    #even if eval is not less than min_eval, min_eval's value is correct, but best move is the row,col which is not the best nove
                    #so at the end, on top of the stack, whatever row,col is there, that will become the best move, which is wrong

                beta = min(eval, beta)
                if beta <= alpha:
                    break

            return min_eval, best_move


    def main_eval(self, main_board):
        if self.level==0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)

        else:
            #minimax
            eval, move = self.minimax(main_board, -10, 10, False) #ai is the one who minimizes
            #alpha=-10 is the worst possible score/eval for maximizing player,
            # #beta=10 is the worst score for minimizing player

        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')

        return move #move is just a tuple - (row,col)

class Game:
    def __init__(self):
        self.board = Board() #creating a new attribute 'board'
        self.ai=AI()

        self.player = 1 # player 1 is the one putting cross, player 2 is putting circles
        #X maximises
        #O minimises
        #above if you initiate self.player=2, then ai will start the game first
        #the optimal starting move for the ai is always going to be one of the four corners
        #because if we put X anywhere other than the centre, we'll lose

        self.gamemode = 'ai' #pvp or ai
        self.running = True #running=True means game not over,
        #game over is when a player wins or there's a draw

        self.show_lines()

    #def make_move(self, row, col):
     #   self.mark_sqr(row, col, self.player)
     #   self.draw_fig(row, col)
     #   self.next_turn()

    def show_lines(self):
        #we need to paint our screen again when we reset the game,
        #hence the below line
        #if we dont write it, then after restarting, there'll be no change on the screen
        screen.fill (bg_colour)

        #vertical:
        pygame.draw.line(screen, line_colour, (sqsize,0), (sqsize,height), line_width)
        #first param is the surface, so we give screen
        #second param is the colour value so we give the line_colour
        #first vertical line's start position coordinate is at (sqsize,0)
        #its end position coordinate is (sqsize, height)
        #width of line value is defined in constant.py

        pygame.draw.line(screen, line_colour, (width-sqsize,0), (width-sqsize,height), line_width)
        #above is for the second vertical line

        #horizontal:
        pygame.draw.line(screen, line_colour, (0,sqsize), (width,sqsize), line_width)
        pygame.draw.line(screen, line_colour, (0,height-sqsize), (width,height-sqsize), line_width)

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross
            #cross means one ascending and one descending line

            #descending line
            start_desc = (col*sqsize + offset, row*sqsize + offset) #offset is the distance between the end of line with the board line of the box
            end_desc = (col*sqsize + sqsize - offset, row*sqsize + sqsize - offset)
            pygame.draw.line(screen, cross_colour, start_desc, end_desc, cross_width )

            #ascending line
            start_asc = (col * sqsize + offset, row * sqsize + sqsize - offset)  # offset is the distance between the end of line with the board line of the box
            end_asc = (col * sqsize + sqsize - offset, row * sqsize + offset)
            pygame.draw.line(screen, cross_colour, start_asc, end_asc, cross_width)

        elif self.player == 2:
            #draw circle
            center = (col*sqsize + sqsize//2, row*sqsize + sqsize//2)

            pygame.draw.circle(screen, circ_colour, center, radius, circ_width)

    def next_turn(self):
        self.player = self.player%2 + 1 #when player is 1, 1%2=1, 1+1=2
        #and when player is 2, 2%2=0, 0+1=1

    def change_gamemode(self):
        #if self.gamemode == 'pvp':
            #self.gamemode == 'ai'
        #else:
            #self.gamemode == 'pvp'

        #above can be written as:
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def reset(self):
        self.__init__() #we are creating a new game object, or more precisely, resetting all the game attrobutes to their default values
        #that's it

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull() #final state non zero means there is a win


def main():

    #game object
    game = Game() #game is the object, when it is created, the init method is called
    #then show_lines method will be called

    board = game.board
    ai = game.ai
    #main loop
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # g - gamemode (by default, game mode is ai)
                if event.key == pygame.K_g:
                    game.change_gamemode()  # if we press the key g, then the gamemode changes

                # r - restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0 - random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1 - unbeatable ai
                if event.key == pygame.K_1:
                    ai.level = 1


            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event.pos) #using trackpad, click anywhere on the screen, this will give the coordinate of that point
                pos = event.pos #this gives exact coordinate or pixel
                #like (512, 400), etc because these are pixels
                #these are very big numbers
                #so to convert them into 3x3 matrix indices:

                row = pos[1]//sqsize #pos[1] is y coordinate
                col = pos[0]//sqsize #pos[0] is x coordinate
                #what the above code does is, with your trackpad wherever you click, (row,col) will give the coordinate of that box
                #think of a 3x3 matrix
                #if you click the centre box, (row,col) will give (1,1)
                #if you click on top left box, (row,col) gives (0,0)

                #so its like
                #00 01 02
                #10 11 12
                #20 21 22

                #print(row, col)

                if board.empty_sqr(row, col) and game.running: #we click on a box, and if its empty (0 as we have initialised), then

                    board.mark_sqr(row, col, game.player) #this will make whatever box we're clicking on, as player in our console matrix, only if the box is empty
                    #print(board.squares) #this will print the 2d array (matrix) on our console
                    #from the graphic board, we are sending information to our console board

                    game.draw_fig(row, col)

                    game.next_turn()
                    #print(board.squares) #now first when we click on a box, it'll show 1, next time we click on another box, it'll show 2, and so on

                    #instead of above three lines, you can use the following one line
                    #game.make_move(row, col)

                    if game.isover():
                        game.running = False


        if game.gamemode == 'ai' and game.player==ai.player and game.running:
            pygame.display.update()

            #ai methods
            row, col = ai.main_eval(board)

            board.mark_sqr(row, col, ai.player)
            game.draw_fig(row, col)
            game.next_turn()

            #instead of above three lines, we use:
            #game.make_move(row, col)

            if game.isover():
                game.running = False #if we dont write this if condition, we'll get an error
                #if the board is full and there's a draw, then ai still tries to make a next move
                #but empty squares is an empty list, so it returns None
                #and we get a type error that we are trying to unpack a Nonetype
                #so we need to stop the game from running as soon as board is full and there's a draw

        pygame.display.update()

main()