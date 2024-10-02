"""
    Title: Kalah Game Analysis Script
    Description: This Python script analyzes a game of Kalah by reading 
                    a sequence of moves from a text file.
    Input Args: text file
    Output: STDOUT
    
    Author: Oluwabusayo Adeyemi .
    Date: 25th of June 2024.
"""

import sys

ERROR_PREFIX = "kalah: error: "

class KalahGame:
    def __init__(self, houses, seeds):
        """
        Initialize the Kalah game with given number of houses and seeds per house.
        """
        self.houses = houses
        self.board = list([seeds] * (houses * 2))  #Initialize board with list for efficient rotation 
        self.stores = [0, 0] # Stores for each player
        self.current_player = 0  # Current player (0 or 1)

    def execute_move(self, house):
        """
        Execute a move for the current player.
        Player 0 moves from houses 1 to m .
        Player 1 moves from houses m+1 to 2m.
        """
        start_index = self.current_player * self.houses

        actual_house_index = start_index + (house - 1)
        spreading_seeds = self.board[actual_house_index]  
        self.board[actual_house_index] = 0
        last_receiver = 0
        
        if spreading_seeds <= 0:
            raise ValueError("Invalid move: house is empty ")
        receiver = actual_house_index + 1
        while(int(spreading_seeds) > 0):
            if receiver > self.houses*2:
                receiver = 0   
            if receiver == self.houses and self.current_player == 0:
                self.stores[0] = int(self.stores[0]) + 1  
                spreading_seeds = int(spreading_seeds) - 1 
                if spreading_seeds > 0:
                   self.board[receiver] = self.board[receiver] + 1
                   spreading_seeds = int(spreading_seeds) - 1 
            elif receiver == int(self.houses)*2 and self.current_player == 1:
                self.stores[1] = int(self.stores[1]) + 1
                spreading_seeds = int(spreading_seeds) - 1
            else:
                self.board[receiver] = self.board[receiver] + 1
                spreading_seeds = int(spreading_seeds) - 1
      
            if int(spreading_seeds) == 0:
                last_receiver = receiver
            else:
                receiver = receiver + 1
                if int(receiver) > self.houses*2:
                    receiver = 0
        
        if (self.current_player == 0 and last_receiver == self.houses) or \
        (self.current_player == 1 and last_receiver == self.houses * 2):
            # print(f"current player : {self.current_player}") # for debugging 
            pass  # Current player does not change
        elif(self.current_player == 0 and int(self.board[last_receiver]) == 1 and int(last_receiver) < int(self.houses)):
            # print(f"current player : {self.current_player}") # for debugging 
            self.stores[0] = int(self.stores[0]) + int(self.board[last_receiver]) + int(self.board[(int(self.houses) + int(last_receiver))])
            self.board[last_receiver] = 0
            self.board[(int(self.houses) + int(last_receiver))] = 0
            self.current_player = 1 - self.current_player
        elif(self.current_player == 1 and int(self.board[last_receiver]) == 1 and int(last_receiver) > int(self.houses)):
            # print(f"current player : {self.current_player}") # for debugging 
            self.stores[1] = int(self.stores[1]) + int(self.board[last_receiver]) + int(self.board[(int(last_receiver) - int(self.houses))])
            self.board[last_receiver] = 0
            self.board[(int(last_receiver) - int(self.houses))] = 0
            self.current_player = 1 - self.current_player
        else:
            # print(f"current player : {self.current_player}") # for debugging 
            self.current_player = 1 - self.current_player
        
    def is_game_over(self):
        """
        Check if the game is over.
        """
        return all(self.board[i] == 0 for i in range(self.houses)) or \
               all(self.board[i] == 0 for i in range(self.houses, 2*self.houses))

    def finalize_game(self):
        """
        Finalize the game by collecting remaining seeds into stores and clearing the board.
        """
        for i in range(2):
            self.stores[i] += sum(self.board[i * self.houses:(i + 1) * self.houses])
            self.board[i * self.houses:(i + 1) * self.houses] = [0] * self.houses

    def get_result(self):
        """
        Get the final result of the game.
        """
        if self.stores[0] > self.stores[1]:
            return 1, self.stores[0], self.stores[1]
        elif self.stores[1] > self.stores[0]:
            return 2, self.stores[0], self.stores[1]
        return 0, self.stores[0], self.stores[1]

    def print_state(self):
        """
        Print the current state of the game for debuging.
        """
        print(f"Board: {list(self.board)}")
        print(f"Stores: {self.stores}")

def parse_file(filepath):
    """
    Parse the input file to retrieve game settings and moves.
    """
    try:
        with open(filepath, 'r') as file:
            header = next(file).split()
            if len(header) != 2:
                raise ValueError()
            houses, seeds = map(int, header)
            if houses <= 0 or seeds <= 0:
                raise ValueError()
            try:
                moves = [int(line.strip()) for line in file if line.strip()]
            except ValueError:
                report_error("expected one value in body line")
    except IOError:
        if len(sys.argv) == 2: 
            report_error("could not open file")
    except ValueError:
        report_error("expected two values in header line" if len(header) != 2 
        else "invalid value in header line")
    except (IOError, ValueError, StopIteration):
        report_error("invalid input file")
    
    if (len(moves) < 1):
       report_error("expected one value in body line") 
    elif any(move < 1 or move > houses for move in moves):
        report_error("invalid value in body line")
    
    return houses, seeds, moves

def analyze_game(filepath):
    """
    Analyze the game using the provided input file.
    """
    houses, seeds, moves = parse_file(filepath)
    game = KalahGame(houses, seeds)
    # print(f"Starting game with {houses} houses and {seeds} seeds") # for debugging 
    # game.print_state()  # for debuging

    for i, move in enumerate(moves, 1):
        #print(f"\nExecuting move {i}: {move}")   # for debuging
        try:
            game.execute_move(move)
            #game.print_state() # for debuging
            if game.is_game_over():
                game.finalize_game()
                return game.get_result()
        except ValueError as e:
            report_error(str(e))

    report_error("insufficient moves")
    
def report_error(message):
    """
    Report an error message to stderr and exit with error code 1.
    """
    print(f"{ERROR_PREFIX}{message}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        report_error("no input file" if len(sys.argv) < 2 else "too many arguments")
    result = analyze_game(sys.argv[1])
    print(*result)
