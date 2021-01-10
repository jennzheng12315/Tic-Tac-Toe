import math
import random
import time

class Player():
    def __init__(self, letter):
        #letter is x or o
        self.letter = letter

        def get_move(self, game):
            pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ")
            #try to cast square as an integer. If it's not or if the spot is
            #not available, print invalid message
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    def get_move(self, game):
        #at the beginning of the game, randomly chose a spot
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            #get the square based on minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'o' if player == 'x' else 'x'

        #check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, \
            'score': 1*(state.num_empty_squares() + 1) \
            if other_player == max_player else -1 * (state.num_empty_squares() + 1)}

        #no empty squares
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        #initializing position and score
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            #make a move and try that spot
            state.make_move(possible_move, player)
            #use recurison to simulate a game after making the move
            sim_score = self.minimax(state, other_player) #alternate player

            #undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            #update the dictionaries
            if player == max_player: #maximize max_player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else: #minimize other_player
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class TicTacToe():
    def __init__(self):
        self.board = [' ' for _ in range(9)] # use a single list to represent 3x3 board
        self.current_winner = None #keep track of winner

    def print_board(self):
        #i*3:(i+1)*3 --> which group of 3 are being chosen
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range (3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

        ## another way to program the above line
        #moves = []
        #for (i, spot) in enumerate(self.board):
        #    # ['x', 'x', 'o'] --> [(0, 'x'), (1, 'x'), (2, 'o')]
        #    if spot == ' ':
        #        moves.append(i)
        #return moves
    def empty_squares(self):
        return ' ' in self.board
    def num_empty_squares(self):
        return self.board.count(' ')
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    def winner(self, square, letter):
    #checking if there is three in a row anywhere
        #check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        #check column
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        #check diagnoals
        #only moves possible to get a diagonal are even numbers
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]] #left to right diagnoals
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 6]] #right to left diagonal
            if all ([spot == letter for spot in diagonal2]):
                return True

        #if all of these fail, there is no winner
        return False

def play(game, x_player, o_player, print_game=True):
#returns the winner of the game or None for a tie
    if print_game:
        game.print_board_nums()

    letter = 'x' #starting letter

    #iterate while the game still has empty squares
    while game.empty_squares():
        #get move from appropriate player
        if letter == 'o':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            #alternate letter
            letter = 'o' if letter == 'x' else 'x'
            #another way to program the above line
            #if letter == 'x':
            #    letter = 'o'
            #else:
            #letter = 'x'
        #add delay
        if print_game:
            time.sleep(1)

    if print_game:
        print("Tie!")

def main():
    mode = 0

    while mode not in [1, 2, 3]:
        mode = input('Enter 1 to play against a random computer. \nEnter 2 to play against a smart computer. \nEnter 3 for smart computer vs random computer: ')
        try:
            mode = int(mode)
            if mode < 1 or mode > 3:
                raise ValueError
        except ValueError:
            print('Invalid input')
    #person vs random computer
    if mode == 1:
        x_player = HumanPlayer('x')
        o_player = RandomComputerPlayer('o')
        t = TicTacToe()
        play(t, x_player, o_player, print_game=True)

    #person vs smart computer
    elif mode == 2:
        x_player = HumanPlayer('x')
        o_player = SmartComputerPlayer('o')
        t = TicTacToe()
        play(t, x_player, o_player, print_game=True)

    #random vs smart computer
    elif mode == 3:
        x_wins = 0
        o_wins = 0
        ties = 0
        iterations = 0
        while iterations < 1 or iterations > 1000:
            iterations = input('Enter number of iterations between 1-1000: ')
            try:
                iterations = int(iterations)
                if iterations < 1 or iterations > 1000:
                    raise ValueError
            except ValueError:
                print('Invalid number.')

        for i in range(iterations):
            x_player = RandomComputerPlayer('x')
            o_player = SmartComputerPlayer('o')
            t = TicTacToe()
            result = play(t, x_player, o_player, print_game=False)
            if result == 'x':
                x_wins += 1
            elif result == 'o':
                o_wins += 1
            else:
                ties += 1
        print(f'After {iterations} iterations, we see {x_wins} random computer wins, {o_wins} smart computer wins, and {ties} ties')
main()