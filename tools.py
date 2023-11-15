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
    

