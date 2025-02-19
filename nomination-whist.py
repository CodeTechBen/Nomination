"""Plays a game of Nomination Whist"""

from random import Random
from collections import deque


class Card:
    """Defines a Card object"""

    RANK_VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit.upper()
        self.value = self.RANK_VALUES[rank]

    def to_string(self) -> str:
        """Returns the correct string to represent the card"""
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return self.to_string()


class Deck:
    """Defines a deck object"""

    def __init__(self) -> None:
        self.cards = self.generate_deck()

    def generate_deck(self) -> list[Card]:
        """Generates a deck of cards and returns them."""
        ranks = ['2', '3', '4', '5', '6', '7',
                 '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'D', 'C', 'H']  # Short suits

        return [Card(rank, suit) for suit in suits for rank in ranks]


    def draw(self, num_cards: int = 1) -> list[Card]:
        """Removes and returns the top `num_cards` from the deck"""
        return [self.cards.pop(0) for _ in range(min(num_cards, len(self.cards)))]


    def shuffle(self, seed: int = None) -> None:
        """Shuffles the deck with an optional seed"""
        random = Random(seed)
        random.shuffle(self.cards)


class Hand:
    """defines a Hand object"""
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def play_card(self, index: int):
        return self.cards.pop(index)

    def add_card(self, card: Card):
        self.cards.append(card)

    def __repr__(self):
        return f"Hand: {self.cards}"


class PlayerBase:
    """Defines Player base class"""
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()
        self.tricks_won = 0
        self.bid = 0

    def make_bid(self, max_tricks: int, total_bids: int):
        pass

    def play_card(self, lead_suit: str, trump_suit: str):
        pass

    def __repr__(self):
        return f"{self.name}: {self.hand}"


class BotPlayer(PlayerBase):
    """defines a Bot class"""
    def __init__(self, name: str):
        super().__init__(name)

    def make_bid(self, max_tricks: int, total_bids: int):
        """Bot makes a bid, ensuring total bids != max_tricks."""
        pass

    def play_card(self, lead_suit: str, trump_suit: str):
        """Plays a card, prioritizing following suit, then trump, then lowest."""
        pass


class GameState:
    """defines the Game object"""
    def __init__(self, num_players=4):
        self.players = [BotPlayer(f"Bot {i+1}") for i in range(num_players)]
        self.deck = Deck()
        self.round = 1
        self.max_rounds = 10
        self.trump_suit = None
        self.round_info = {
            1: {'cards': 10, 'trump': 'Hearts'},
            2: {'cards': 9, 'trump': 'Clubs'},
            3: {'cards': 8, 'trump': 'Diamonds'},
            4: {'cards': 7, 'trump': 'Spades'},
            5: {'cards': 6, 'trump': 'None'},
            6: {'cards': 5, 'trump': 'Hearts'},
            7: {'cards': 4, 'trump': 'Clubs'},
            8: {'cards': 3, 'trump': 'Diamonds'},
            9: {'cards': 2, 'trump': 'Spades'},
            10: {'cards': 1, 'trump': 'None'}
        }


    def next_round(self, players):
        """moves to the next round"""
        for player in players:
            player.hand = Hand()
        self.round += 1
        return self.round

    def bidding_phase(self):
        """Every player bids how many tricks they will win"""
        pass

    def play_round(self):
        """each player plays a card"""
        pass

    def determine_trick_winner(self):
        """Determines who wins the trick."""
        pass

    def score_round(self):
        """Calculates each player score"""
        pass

    def get_cards(self, deck: Deck, players: list[PlayerBase]):
        """Each player gets hand for the round"""
        for _ in range(self.round_info[self.round]['cards']):
            for player in players:
                player.hand.add_card(deck.draw())


    def play_game(self):
        """Plays the game"""
        while self.round <= self.max_rounds:
            self.deck = Deck()
            self.deck.shuffle()

            self.trump_suit = self.round_info[self.round]['trump']

            self.get_cards(self.deck, self.players)
            print(self.round)
            for player in self.players:
                print(f'{player.name}:{player.hand}')

            self.bidding_phase()

            self.play_round()

            self.score_round()

            self.next_round(self.players)


if __name__ == '__main__':
    # Run the Game Simulation
    game = GameState()
    game.play_game()
