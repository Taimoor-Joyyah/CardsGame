import os
import random

cards_no = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
cards_group = ('Diamond', 'Heart', 'Pan', 'Tree')

# Create and shuffle card deck
cards_deck = [(group, no) for group in cards_group for no in cards_no]
random.shuffle(cards_deck)

# Getting no of player from user
# while True:
#     no_of_players = input('Enter no of players : ')
#     if '2' <= no_of_players <= '4':
#         no_of_players = int(no_of_players)
#         break
#     else:
#         print('No of Player must be between 2 and 4')

no_of_players = 4

# Distributing cards among players
cards_distribution = [[card for index, card in enumerate(cards_deck)
                       if index % no_of_players is player]
                      for player in range(no_of_players)]

# Sorting Cards
for player_cards in cards_distribution:
    player_cards.sort(key=lambda x: cards_no.index(x[1]))
    player_cards.sort(key=lambda x: cards_group.index(x[0]))


def player_order(start_player):
    return list(range(start_player, no_of_players)) + list(range(0, start_player))


# Current Player
start_player = None
for player_no, player_cards in enumerate(cards_distribution):
    for card in player_cards:
        if card == ('Pan', 'A'):
            start_player = player_no

thrown_cards = []
throw_count = 0
session_count = 0
while True:
    thrown_cards.clear()
    for current_player in player_order(start_player):
        print(f'Player {current_player} :-')
        for index, card in enumerate(cards_distribution[current_player]):
            print(f'{index} - {cards_distribution[current_player][index]}')
        if throw_count:
            card = cards_distribution[current_player][int(input(f'Enter Card no to Throw > '))]
        else:
            card = ('Pan', 'A')
        throw_count += 1
        thrown_cards.append([current_player, card])
        cards_distribution[current_player].remove(card)
        print(f'Card {card} is thrown by Player {current_player}')
    session_count += 1
    break
