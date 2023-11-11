import random
from briscola_game import Briscola
from tools import get_card_value, compare_cards, draw_cards
from games4e import monte_carlo_tree_search
from copy import deepcopy

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
        
    def generate_move(self, state_copy, game):
        """Take user input to choose a move."""

        # Print the player's hand and the table
        print("Your hand: ", state_copy['hand' + str(self.number)])
        print("Table: ", state_copy['table'])

        # Ask the user to pick 0, 1 or 2 and check if the input is valid
        while True:
            move_index = input("Pick a card (0, 1 or 2): ")
            if move_index in ['0', '1', '2']:
                break
            else:
                print("Invalid input, try again.")

        move = state_copy['hand' + str(self.number)][int(move_index)]
                    
        # Return the move
        return move
    
class SmartPlayer:
    """A player that chooses a legal move based on the briscola strategy.
    Plays the lowest card if it is the first to move, otherwise maximises the score."""
    
    def __init__(self, number):
        """Initialize the player."""
        self.number = number # the player number (1 or 2)

    def evaluate_move(self, move, state_copy, game):
        # calculate the total value of the trick
        total_value = get_card_value(move) + get_card_value(state_copy['table'][0])

        # return the total value if the move wins the trick, otherwise negative
        if compare_cards(move, state_copy['table'][0], state_copy['briscola']):
            return total_value
        else:
            return -total_value
    
    def generate_move(self, state_copy, game):
        # if the table is empty, play the lowest card
        if len(state_copy['table']) == 0:
            return min(state_copy['hand' + str(self.number)], key=lambda x: get_card_value(x))
        else:
            # check the evaluation of each move
            moves = game.actions(state_copy)
            moves_eval = []
            for move in moves:
                moves_eval.append(self.evaluate_move(move, state_copy, game))

            # return the move with the highest evaluation
            return moves[moves_eval.index(max(moves_eval))]
        
class MonteCarloTreeSearchPlayer:
    """A player that chooses a legal move based on the Monte Carlo Tree Search algorithm."""

    def __init__(self, simulations=1000):
        """Initialize the player."""
        self.simulations = simulations # the number of simulations
        
    def generate_move(self, state_copy, game):
        """Choose a move based on the Monte Carlo Tree Search algorithm."""
        return monte_carlo_tree_search(state_copy, game, self.simulations)

                

