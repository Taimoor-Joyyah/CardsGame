from Card_Classes import *


class Game:
    ranks = ('First', 'Second', 'Third', 'Forth')

    def __init__(self):
        self.players = self.set_players()

    # get no of players from host
    def set_players(self):
        while True:
            players = input('Enter no of players : ')  # listen host for no of players input
            if players.isnumeric() and 2 <= int(players) <= 4:
                return int(players)
            else:
                print('No of Player must be 2, 3 or 4')  # return message to host for wrong input

    # returns the order of play in each session
    def play_order(self, start_player):
        return (self.players_playing * 2)[self.players_playing.index(start_player):
                                          self.players_playing.index(start_player) + len(self.players_playing)]

    # return who to start first
    def get_start_player(self):
        for player, card_pack in enumerate(self.players_card_packs):
            for card in card_pack:
                if card == Card('Spade', 'A'):
                    return player

    # let player enter card no for card selection
    def enter_card(self, player):
        while True:
            card_no = input(f'Enter Card No. to Throw > ')  # listen current player for card no input
            if card_no.isnumeric() and 0 <= int(card_no) < len(self.players_card_packs[player]):
                card = self.players_card_packs[player][int(card_no)]
                if not self.card_follow:
                    return card
                else:
                    if (card.suit == self.card_follow or self.thulla or
                            self.winnerfollowthulla or self.firstsessionthulla):
                        return card
                    else:
                        print(
                            f'Please throw {self.card_follow} card.')  # return message to current player for wrong input
            else:
                print('Please enter a valid card no. !!!')  # return message to current player for wrong input

    # sort all players card pack before gameplay
    def players_card_sort(self):
        for card_pack in self.players_card_packs:
            card_pack.sort_cards()

    # shuffle card packs before players posses
    def players_card_shuffle(self):
        shuffle(self.players_card_packs)

    # throw card by current player in session
    def throw_card(self, player):
        if self.isfirstplay():
            card = Card('Spade', 'A')
            self.card_follow = card.suit
            self.big_card = (player, 'A')
        else:
            if self.card_follow:
                if self.isthulla(player):
                    self.thulla = True
                    print(f'\nGive THULLA to Player {self.big_card[0]} !!!')  # return message to current player
                elif self.iswinnerfollowthulla(player) and self.isfirstsessionthulla(player):
                    self.winnerfollowthulla = True
                    self.firstsessionthulla = True
                    print('Throw any card')  # return message to current player
                else:
                    print(f'\nFollowing {self.card_follow} card')  # return message to current player
            card = self.enter_card(player)
            if not self.card_follow:
                self.card_follow = card.suit
                self.big_card = (player, card.rank)
        self.players_card_packs[player].throw_card(card)
        self.thrown_cards.append((player, card))
        return card

    # check if current player won
    def iswon(self, player):
        return not self.players_card_packs[player]

    def suit_exist(self, player):
        return [card.suit for card in self.players_card_packs[player]].count(self.card_follow)

    # checking thulla
    def isthulla(self, player):
        return not self.suit_exist(player) and self.session_count

    def iswinnerfollowthulla(self, player):
        return self.card_follow and not self.suit_exist(player) and self.ranking.count(self.thrown_cards[0])

    def isfirstsessionthulla(self, player):
        return not self.session_count and self.card_follow and not self.suit_exist(player)

    # check if the first player is playing
    def isfirstplay(self):
        return not self.session_count and not self.card_follow

    # if last player remaining
    def islastplayer(self):
        return len(self.ranking) == self.players - 1

    # plays session of gameplay
    def play_session(self):
        for player in self.play_order(self.start_player):
            print('----------------------------------------')
            print(f'\nPlayer {player} is Playing')  # return message to all players
            print(self.players_card_packs[player])  # return cards to current player
            card = self.throw_card(player)
            print(f'\nCard {card} is thrown by Player {player}')  # return message to all players
            if self.iswon(player):
                print(
                    f'\nPlayer {player} is {self.ranks[len(self.ranking)]} -------------------->>>>>>>>>>>>>>>>>>>>')  # return message to all players
                self.ranking.append(player)
                self.players_playing.remove(player)
            elif card_ranks.index(card.rank) > card_ranks.index(self.big_card[1]) and not self.thulla:
                self.big_card = (player, card.rank)
            self.start_player = self.big_card[0]
            if self.winnerfollowthulla:
                break
            if self.thulla:
                for thrown_card in self.thrown_cards:
                    self.players_card_packs[self.big_card[0]].add_card(thrown_card[1])
                self.players_card_packs[self.big_card[0]].sort_cards()
                break

    # initialize game before playing
    def initialization(self):
        self.players_playing = list(range(self.players))
        self.card_deck = CardDeck()
        self.card_deck.shuffle()
        self.players_card_packs = [CardPack() for player in self.players_playing]
        self.card_deck.distribution(self.players_card_packs)
        self.players_card_shuffle()
        self.players_card_sort()
        self.start_player = self.get_start_player()
        self.ranking = []
        self.session_count = 0

    # controls gameplay
    def play(self):
        while True:
            self.card_follow = ''
            self.thrown_cards = []
            self.big_card = ()
            self.thulla = False
            self.winnerfollowthulla = False
            self.firstsessionthulla = False
            print('----------------------------------------')
            print('----------------------------------------')
            print(f'\nSession {self.session_count}')  # return message to all players
            self.play_session()
            self.session_count += 1
            if self.islastplayer():
                for item in range(self.players):
                    if not self.ranking.count(item):
                        self.ranking.append(item)
                break
        print(self.end_stats())  # return end statistics to all players

    # return ending statistics to all players
    def end_stats(self):
        stat_display = '\n\n----------------------------------------'
        stat_display += 'GAME END Statistics'
        for index, player in enumerate(self.ranking):
            stat_display += f'\nPlayer {player} is {self.ranks[index]}'
        return stat_display
