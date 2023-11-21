import random
from copy import deepcopy 

def get_card_value(card):
    '''
    card: a list of two elements, the first one is the value, the second one is the suite
    '''
    card_value = card[0]

    if card_value == 'Ace': 
        return 11
    elif card_value == '3': 
        return 10
    elif card_value == 'King': 
        return 4
    elif card_value == 'Horse': 
        return 3
    elif card_value == 'Jack': 
        return 2
    elif card_value == '7': 
        return 0.0007
    elif card_value == '6': 
        return 0.0006
    elif card_value == '5': 
        return 0.0005
    elif card_value == '4': 
        return 0.0004
    elif card_value == '2': 
        return 0.0002

def compare_cards(card_first_to_move, card_second_to_move, trump):
    """
    Returns True if the first card wins, False otherwise
    """
    # Get the suites and values of the cards
    trump_suite = trump[1]
    card_first_to_move_suite = card_first_to_move[1]
    card_second_to_move_suite = card_second_to_move[1]
    card_first_to_move_value = get_card_value(card_first_to_move)
    card_second_to_move_value = get_card_value(card_second_to_move)

    # If one card is the trump and the other is not, the trump wins
    if card_first_to_move_suite == trump_suite and card_second_to_move_suite != trump_suite:
        return True
    elif card_first_to_move_suite != trump_suite and card_second_to_move_suite == trump_suite:
        return False
    
    # If the suites are the same, the highest value wins
    elif card_first_to_move_suite == card_second_to_move_suite:
        if card_first_to_move_value > card_second_to_move_value:
            return True
        elif card_first_to_move_value < card_second_to_move_value:
            return False
        
    # If the suites are different and none of them is the trump, the first one to move wins
    else:
        return True
    
def draw_cards(state):
    """
    Removes two random cards from the deck and puts is in the hands
    """
    state_copy = deepcopy(state)
    card1 = random.choice(state_copy['deck'])
    state_copy['deck'].remove(card1)

    try:
        card2 = random.choice(state_copy['deck'])
        state_copy['deck'].remove(card2)
    except IndexError:
        card2 = state_copy['briscola']
        # print('Deck is empty, trump is drawn')

    state_copy['hand1'].append(card1)
    state_copy['hand2'].append(card2)

    return state_copy

def evaluation_function(state, player_number):
    """
    Evaluates the state given a player. It is the difference in points earned
    """
    # the evaluation is points in players hand minus points in opponent's hand

    # get the points in the hands
    eval = sum(get_card_value(card) for card in state['hand' + str(player_number)]) - sum(get_card_value(card) for card in state['hand' + str(3 - player_number)])
    return eval

def my_monte_carlo_tree_search(state, game, n_sim):
    """
    Monte Carlo Tree Search algorithm
    """   
    # Explore the possible moves given the state
    possible_moves = game.actions(state)

    # If there is only one possible move, return it
    if len(possible_moves) == 1:
        return possible_moves[0]
    
    # Create a dictionary to store the number of wins for each move
    wins = {}
    player = game.to_move(state)

    if player != 1:
        raise Exception("Player to move is not 1")

    # For each possible move, simulate n_sim games and store the number of wins
    for move in possible_moves:
        wins[move] = 0

        for sim in range(n_sim):
            # Create a copy of the state
            state_copy = deepcopy(state)

            if len(state_copy['table']) == 0:
                hand_2_new = random.sample(state_copy['hand2'], 3)
            else: 
                hand_2_new = random.sample(state_copy['hand2'], 2)

            state_copy['hand2'] = hand_2_new  

            # Play the move
            state_copy = game.result(state_copy, move)

            # randomise a hand for the second player
               

            # Simulate the game
            while not game.terminal_test(state_copy):
                # print("Deck length: ", len(state_copy['deck']))
                total_cards = len(state_copy['hand1']) + len(state_copy['hand2']) + len(state_copy['table']) + len(state_copy['deck']) + len(state_copy['taken1']) + len(state_copy['taken2'])
                action = random.choice(game.actions(state_copy))
                state_copy = game.result(state_copy, action)

            # If the player wins, add one to the number of wins
            if game.utility(state_copy, player) == 1:
                wins[move] += 1

    # Return the move with the highest number of wins
    return max(wins, key=wins.get)

def evaluate_move(move, state_copy):
    # calculate the total value of the trick
    total_value = get_card_value(move) + get_card_value(state_copy["table"][0])

    # return the negative total value if the move loses the trick, otherwise positive
    if compare_cards(state_copy["table"][0], move, state_copy["briscola"]):
        return -total_value
    else:
        return total_value

def generate_move_smart(state_copy, game):
    # if the table is empty, play the lowest card
    player_number = state_copy["player"]
    if len(state_copy["table"]) == 0:
        return min(state_copy[f"hand{player_number}"], key=lambda x: get_card_value(x))
    else:
        # check the evaluation of each move
        moves = game.actions(state_copy)
        moves_eval = [evaluate_move(move, state_copy) for move in moves]

        # return the move with the highest evaluation
        return moves[moves_eval.index(max(moves_eval))]

