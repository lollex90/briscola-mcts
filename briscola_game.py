import random
from games4e import Game
from tools import get_card_value, compare_cards, draw_cards 

class Briscola(Game):
    """Play a game of Briscola between two players.

    A state is represented by a dictionary of:
        - the cards in the hand of each player (0, 1)
        - the cards on the table (2)
        - the player to move (3)
        - the cards taken by each player (4, 5)
        - the briscola card (6)
        - the cards in the deck (7)

    state = {'hand1': hand1, 'hand2': hand2, 'table': table, 'player': player, 'taken1': taken1, 'taken2': taken2, 'briscola': briscola, 'deck': deck}

    Each card is represented by a tuple of (suit, rank).
    The deck is represented by a list of cards.    
    """

    full_deck = [('Ace', 'Bastoni'), ('Ace', 'Denari'), ('Ace', 'Spade'), ('Ace', 'Coppe'),
                 ('2', 'Bastoni'), ('2', 'Denari'), ('2', 'Spade'), ('2', 'Coppe'),
                 ('3', 'Bastoni'), ('3', 'Denari'), ('3', 'Spade'), ('3', 'Coppe'),
                 ('4', 'Bastoni'), ('4', 'Denari'), ('4', 'Spade'), ('4', 'Coppe'),
                 ('5', 'Bastoni'), ('5', 'Denari'), ('5', 'Spade'), ('5', 'Coppe'),
                 ('6', 'Bastoni'), ('6', 'Denari'), ('6', 'Spade'), ('6', 'Coppe'),
                 ('7', 'Bastoni'), ('7', 'Denari'), ('7', 'Spade'), ('7', 'Coppe'),
                 ('Jack', 'Bastoni'), ('Jack', 'Denari'), ('Jack', 'Spade'), ('Jack', 'Coppe'),
                 ('Horse', 'Bastoni'), ('Horse', 'Denari'), ('Horse', 'Spade'), ('Horse', 'Coppe'),
                 ('King', 'Bastoni'), ('King', 'Denari'), ('King', 'Spade'), ('King', 'Coppe')]
    
    # the initial state is a random trump, random hands and a random player to move
    my_sample = random.sample(full_deck, 7)
    hand1, hand2, trump = my_sample[:3], my_sample[3:6], [my_sample[6]]
    # delete the cards from the deck
    deck = full_deck
    for card in my_sample:
        deck.remove(card)

    trump = trump[0]
    initial = {'hand1': hand1, 'hand2': hand2, 'table': [], 'player': random.choice([1, 2]), 'taken1': [], 'taken2': [], 'briscola': trump, 'deck': deck}   

    def __init__(self):
        """Initialize the game."""
        self.state = self.initial

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        # available actions are the cards in the hand of the player to move
        return state['hand' + str(state['player'])]

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        # move is the card played by the player to move
        # the card is removed from the hand of the player to move
        hand = state['hand' + str(state['player'])]
        hand.remove(move)

        # the card is added to the table
        table = state['table']
        table.append(move)

        # if there are two cards on the table, evaluate who wins the trick
        if len(table) == 2:
            print("The cards on the table are: ", table)
            # get the trump card
            trump = state['briscola']

            # get the cards on the table
            card_first_to_move = table[0]
            card_second_to_move = table[1]

            # if the first card wins, the player that had just moved loses the trick
            if compare_cards(card_first_to_move, card_second_to_move, trump):
                winner = 3 - state['player']
                print("The winner is (if): ", winner)
            else:
                winner = state['player']
                print("The winner is (else): ", winner)

            # update the state
            # each player draws a card from the deck if there are still cards in the deck
            if state['deck'] != []:
                state = draw_cards(state)
                print("The new hands are: ", state['hand1'], state['hand2'])

            # add the cards on the table to the taken cards of the winner
            taken = state['taken' + str(winner)]
            taken.extend(table)
            state['taken' + str(winner)] = taken

            # empty the table
            state['table'] = []

            # update the player to move
            state['player'] = winner

            return state
        
        # if there is only one card on the table, the player to move is changed
        else:
            state['player'] = 3 - state['player']
            return state

    def utility(self, state, player):
        """Return the value of this final state to player."""

        # the player wins if the sum of all cards they took is greater than 60
        taken = state['taken' + str(player+1)]
        sum_taken = 0
        for card in taken:
            sum_taken += get_card_value(card)
        
        if sum_taken > 60:
            return 1
        else:
            return 0
        
    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        # the game is over if the deck is empty and the players have no more cards in their hands
        if state['deck'] == [] and state['hand1'] == [] and state['hand2'] == []:
            return True
        else:
            return False

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state['player']

    def display(self):
        """Print or otherwise display the state."""
        print(self.state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, player1, player2):
        """Play an 2-person, move-alternating game."""
        state = self.initial
        print("GAME START")
        print("The trump is: ", state['briscola'])
        print("Player 0 hand: ", state['hand1'])
        print("Player 1 hand: ", state['hand2'])
        print("The first to play is: ", state['player'])
        while True:
            # the player to move makes a move
            if self.to_move(state) == 1:
                move = player1.generate_move(state, self)
            else:
                move = player2.generate_move(state, self)
            
            # the move is applied to the state
            state = self.result(state, move)

            # check if the game is over
            if self.terminal_test(state):
                print('Game over')
                if self.utility(state, 0) == 1:
                    print('Player 0 wins. Total points:', sum([get_card_value(card) for card in state['taken1']]))
                    print(state['taken1'])
                    break
                elif self.utility(state, 1) == 1:
                    print('Player 1 wins. Total points:', sum([get_card_value(card) for card in state['taken2']]))
                    print(state['taken2'])
                    break



