from random import shuffle

card_suits = ('Diamond', 'Heart', 'Spade', 'Club')
card_ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"({self.rank} of {self.suit})"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank


class CardPack:
    def __init__(self):
        self.pack = []

    def __str__(self):
        cards_display = ''
        for index, card in enumerate(self.pack):
            cards_display += f"\n{index} - {card}"
        return cards_display

    def __len__(self):
        return len(self.pack)

    def __iter__(self):
        return iter(self.pack)

    def __getitem__(self, item):
        return self.pack[item]

    def add_card(self, card):
        self.pack.append(card)

    def sort_cards(self):
        self.pack.sort(key=lambda card: card_ranks.index(card.rank))
        self.pack.sort(key=lambda card: card_suits.index(card.suit))

    def throw_card(self, card):
        self.pack.remove(card)


class CardDeck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in card_suits for rank in card_ranks]

    def shuffle(self):
        shuffle(self.deck)

    def distribution(self, card_packs):
        for index, card in enumerate(self.deck):
            card_packs[index % len(card_packs)].add_card(card)
