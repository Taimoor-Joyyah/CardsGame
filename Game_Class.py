from Card_Classes import *
import Server


class Game:
    ranks = ('First', 'Second', 'Third', 'Forth')

    def __init__(self):
        Server.connect_host_player()
        self.players = self.set_players()
        self.allplayers = list(range(self.players))
        Server.connect_players(self.players)
        Server.send_message(self.allplayers, f'\n{self.players} players are playing')
        self.initialization()
        self.play()

    # get no of players from host_player
    def set_players(self):
        while True:
            players = Server.receive_message(Server.host_player, '\nEnter no of players : ')
            if players.isnumeric() and 2 <= int(players) <= 4:
                return int(players)
            else:
                Server.send_message([Server.host_player], '\nNo of Player must be 2, 3 or 4')

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
            card_no = Server.receive_message(player, '\nEnter Card No. to Throw > ')
            if card_no.isnumeric() and 0 <= int(card_no) < len(self.players_card_packs[player]):
                card = self.players_card_packs[player][int(card_no)]
                if not self.card_follow:
                    return card
                else:
                    if (card.suit == self.card_follow or self.thulla or
                            self.winnerfollowthulla or self.firstsessionthulla):
                        return card
                    else:
                        # return message to current player for wrong input
                        Server.send_message([player], f'\nPlease throw {self.card_follow} Card.')
            else:
                # return message to current player for wrong input
                Server.send_message([player], '\nPlease enter a valid card no. !!!')

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
                    Server.send_message([player], f'\nGive THULLA to Player {Server.nicknames[self.big_card[0]]} !!!')
                elif self.iswinnerfollowthulla(player) and self.isfirstsessionthulla(player):
                    self.winnerfollowthulla = True
                    self.firstsessionthulla = True
                    Server.send_message([player], '\nThrow any card')
                else:
                    Server.send_message([player], f'\nFollowing {self.card_follow} Card')
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

    # check if suit exist in player card pack
    def suit_exist(self, player):
        return [card.suit for card in self.players_card_packs[player]].count(self.card_follow)

    # checking thulla
    def isthulla(self, player):
        return not self.suit_exist(player) and self.session_count

    # check if winner is followed and on thulla
    def iswinnerfollowthulla(self, player):
        return self.card_follow and not self.suit_exist(player) and self.ranking.count(self.thrown_cards[0])

    # check if player getting thulla on first session
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
            Server.send_message(self.allplayers, '--------------------------------------------------')
            Server.send_message(self.allplayers, f'\n{Server.nicknames[player]} is Playing')
            Server.send_message([player], str(self.players_card_packs[player]))
            card = self.throw_card(player)
            Server.send_message(self.allplayers, f'\n{Server.nicknames[player]} has thrown Card {card}')
            if self.iswon(player):
                Server.send_message(self.allplayers, f'\n{Server.nicknames[player]} is {self.ranks[len(self.ranking)]}')
                self.ranking.append(player)
                self.players_playing.remove(player)
            elif card_ranks.index(card.rank) > card_ranks.index(self.big_card[1]) and not self.thulla:
                self.big_card = (player, card.rank)
            self.start_player = self.big_card[0]
            if self.winnerfollowthulla:
                break
            if self.thulla:
                Server.send_message(self.allplayers, f'{Server.nicknames[self.big_card[0]]}'
                                                     f' got THULLA by {Server.nicknames[player]}')
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
            Server.send_message(self.allplayers, '--------------------------------------------------')
            Server.send_message(self.allplayers, '--------------------------------------------------')
            Server.send_message(self.allplayers, f'\nSession {self.session_count}')
            self.play_session()
            self.session_count += 1
            if self.islastplayer():
                for item in range(self.players):
                    if not self.ranking.count(item):
                        self.ranking.append(item)
                break
        Server.send_message(self.allplayers, '--------------------------------------------------')
        Server.send_message(self.allplayers, str(self.end_stats()))

    # return ending statistics to all players
    def end_stats(self):
        stat_display = ''
        stat_display += 'GAME END Statistics'
        for index, player in enumerate(self.ranking):
            stat_display += f'\n{Server.nicknames[player]} is {self.ranks[index]}'
        return stat_display
