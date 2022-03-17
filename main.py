import random

cards_no = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
cards_group = ('Diamond', 'Heart', 'Pan', 'Tree')
rank = ('First', 'Second', 'Third', 'Forth')

# Create and shuffle card deck
cards_deck = [(group, no) for group in cards_group for no in cards_no]
random.shuffle(cards_deck)

# Getting no of player from user
while True:
    no_of_players = input('Enter no of players : ')
    if '2' <= no_of_players <= '4':
        no_of_players = int(no_of_players)
        break
    else:
        print('No of Player must be between 2 and 4')

player_rank = []

# Distributing cards among players
cards_distribution = [[card for index, card in enumerate(cards_deck)
                       if index % no_of_players is player]
                      for player in range(no_of_players)]


def player_order(begin_player):
    player_list = list(range(begin_player, no_of_players)) + list(range(0, begin_player))
    for player in player_rank:
        player_list.remove(player)
    return player_list


def sort_cards(cards):
    cards.sort(key=lambda x: cards_no.index(x[1]))
    cards.sort(key=lambda x: cards_group.index(x[0]))


def enter_card(player):
    while True:
        card_no = input(f'Enter Card No. to Throw > ')
        if card_no.isnumeric() and 0 <= int(card_no) < len(cards_distribution[player]):
            return int(card_no)


# Sorting Cards
for player_cards in cards_distribution:
    sort_cards(player_cards)

# Current Player
start_player = None
for player_no, player_cards in enumerate(cards_distribution):
    for card in player_cards:
        if card == ('Pan', 'A'):
            start_player = player_no
            break

big_card = []
thrown_cards = []
throws_in_session = 0
session_count = 0
thulla = None

# Gameplay
while True:
    card_follow = ''
    thrown_cards.clear()
    session_count += 1
    big_card.clear()
    thulla = False
    print('\n')
    print(f'Session {session_count}')
    for current_player in player_order(start_player):
        print('\n')
        print(f'Player {current_player} :-')
        for index, card in enumerate(cards_distribution[current_player]):
            print(f'{index} - {cards_distribution[current_player][index]}')
        if card_follow:
            # thulla checking
            if not [card[0] for card in cards_distribution[current_player]].count(card_follow) and \
                    session_count != 1 and cards_distribution[big_card[0]]:
                print(f'Give THULLA to Player {big_card[0]} !!!')
                thulla = True
            else:
                print(f'Following {card_follow} card')
        if throws_in_session:
            while True:
                card = cards_distribution[current_player][enter_card(current_player)]
                if card_follow:
                    if card_follow == card[0] or thulla:
                        break
                    else:
                        print(f'Please throw {card_follow} card.')
                else:
                    card_follow = card[0]
                    big_card = [current_player, card[1]]
                    break
        else:
            card = ('Pan', 'A')
            card_follow = card[0]
            big_card = [current_player, 'A']
        throws_in_session += 1
        thrown_cards.append((current_player, card))
        cards_distribution[current_player].remove(card)
        if not cards_distribution[current_player]:
            print(f'Player {current_player} is {rank[len(player_rank)]}')
            player_rank.append(current_player)
        print(f'Card {card} is thrown by Player {current_player}')
        if cards_no.index(card[1]) > cards_no.index(big_card[1]) and not thulla:
            big_card = [current_player, card[1]]
        start_player = big_card[0]
        if thulla:
            for card in thrown_cards:
                cards_distribution[big_card[0]].append(card[1])
            # sort
            sort_cards(cards_distribution[big_card[0]])
            break
    if len(player_rank) == no_of_players - 1:
        for item in range(no_of_players):
            if not player_rank.count(item):
                player_rank.append(item)
        break

print('\n\n')
print('GAME END Statistics')
for index, player in enumerate(player_rank):
    print(f'Player {player} is {rank[index]}')
