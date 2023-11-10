import random
from briscola_game import Briscola

class RandomPlayer:
    """A player that chooses a legal move at random."""

    def generate_move(self, state, game):
        """Choose a random move from the given legal moves."""
        
        return random.choice(game.actions(state))
    
class HumanPlayer:
    """A player that chooses a legal move based on user input."""

    def __init__(self, number):
        """Initialize the player."""
        self.number = number # the player number (1 or 2)
        
    def generate_move(self, state, game):
        """Take user input to choose a move."""

        # Print the player's hand and the table
        print("Your hand: ", state['hand' + str(self.number)])
        print("Table: ", state['table'])

        # Ask the user to pick 0, 1 or 2 and check if the input is valid
        while True:
            move_index = input("Pick a card (0, 1 or 2): ")
            if move_index in ['0', '1', '2']:
                break
            else:
                print("Invalid input, try again.")

        move = state['hand' + str(self.number)][int(move_index)]
                    
        # Return the move
        return move
    
class SmartPlayer:
    """A player that chooses a legal move based on the briscola strategy.
    Plays the lowest card if it is the first to move, otherwise maximises the score."""
    
    def __init__(self, number):
        """Initialize the player."""
        self.number = number # the player number (0 or 1)
    
    def generate_move(self, state, game):
        # if the table is empty, play the lowest card
        if len(state[2]) == 0:
            return min(state[self.number], key=lambda x: game.get_card_value(x))
        else:
            # check the evaluation of each move
            moves = game.actions(state)
            moves_eval = []
            for move in moves:
                moves_eval.append(self.evaluate_move(move, state, game))

            # return the move with the highest evaluation
            return moves[moves_eval.index(max(moves_eval))]
        
    def evaluate_move(self, move, state, game):
        # calculate the total value of the trick
        total_value = game.get_card_value(move) + game.get_card_value(state[2][0])

        # return the total value if the move wins the trick, otherwise negative
        if game.compare_cards(move, state[2][0], state[6]):
            return total_value
        else:
            return -total_value
