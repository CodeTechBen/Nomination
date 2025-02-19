"""Plays a game of Nomination Whist"""

from random import Random, randint


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
        suits = ['S', 'D', 'C', 'H']

        return [Card(rank, suit) for suit in suits for rank in ranks]


    def draw(self, num_cards: int = 1):
        """Removes and returns the top x number of cards from the deck"""
        if num_cards == 1:
            return self.cards.pop()  # Return a single Card object
        return [self.cards.pop() for _ in range(min(num_cards, len(self.cards)))]



    def shuffle(self, seed: int = None) -> None:
        """Shuffles the deck with an optional seed"""
        random = Random(seed)
        random.shuffle(self.cards)


class Hand:
    """defines a Hand object"""
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def play_card(self, index: int):
        """removes a card from the hand"""
        return self.cards.pop(index)

    def add_card(self, card: Card):
        """Adds a selected card to the hand"""
        self.cards.append(card)

    def get_hand_value(self):
        """Gets the total value of the hand"""
        value = 0
        for card in self.cards:
            value += card.value
        return value


    def __repr__(self):
        return f"Hand: {self.cards}"


class PlayerBase:
    """Defines Player base class"""
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()
        self.tricks_won = 0
        self.bid = 0
        self.player_score = 0

    def make_bid(self, max_tricks: int, total_bids: int, trump_suit: str):
        pass

    def play_card(self, lead_suit: str, trump_suit: str):
        pass

    def write_to_csv(self):
        pass

    def __repr__(self):
        return f"{self.name}: {self.hand}"


class BotPlayer(PlayerBase):
    """defines a Bot class"""
    def __init__(self, name: str):
        super().__init__(name)

    def make_bid(self, max_tricks: int, total_bids: int, trump_suit: str):
        """Bot makes a bid, ensuring total bids != max_tricks."""

        possible_bids = list(range(max_tricks + 1))  # Bids from 0 to max_tricks
        if total_bids == max_tricks and max_tricks > 0:
            # Remove the bid that would sum to max_tricks
            possible_bids.remove(max_tricks - total_bids)

        self.bid = randint(0, max_tricks) if not possible_bids else randint(
            min(possible_bids), max(possible_bids))
        print(f"{self.name} bids {self.bid} tricks.")

    def play_card(self, lead_suit: str, trump_suit: str):
        """Plays a card, following suit if possible, then trump, then lowest."""

        if not self.hand.cards:
            print(f"{self.name} has no cards left to play!")
            return None  # Handle this case in calling functions

        if lead_suit:
            # Step 1: Try to follow suit
            follow_suit_cards = [
                card for card in self.hand.cards if card.suit == lead_suit]
            if follow_suit_cards:
                played_card = min(follow_suit_cards, key=lambda card: card.value)
            else:
                # Step 2: No lead suit, try to play trump
                trump_cards = [
                    card for card in self.hand.cards if card.suit == trump_suit]
                if trump_cards:
                    played_card = min(trump_cards, key=lambda card: card.value)
                else:
                    # Step 3: No trump either, play the lowest card in hand
                    played_card = min(self.hand.cards, key=lambda card: card.value)
        else:
            # First player to play: Choose the highest card
            played_card = max(self.hand.cards, key=lambda card: card.value)

        # Remove the played card from hand and return it
        self.hand.cards.remove(played_card)
        return played_card


    def write_to_csv(self):
        """Writes the hand, tricks won to csv"""
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

    def bidding_phase(self, players: list[PlayerBase]):
        """Every player bids how many tricks they will win"""
        max_tricks = self.round_info[self.round]['cards']
        total_bid = 0
        trump_suit = self.round_info[self.round]['trump']
        for player in players:
            player.make_bid(max_tricks, total_bid, trump_suit)


    def play_trick(self, players: list[PlayerBase]):
        """Each player plays a card in turn"""
        lead_suit = None
        trick_cards = []  # Stores (player, card) tuples

        for i, player in enumerate(players):
            played_card = player.play_card(lead_suit, self.trump_suit)

            if i == 0:  # First player determines the lead suit
                lead_suit = played_card.suit

            trick_cards.append((player, played_card))
            print(f"{player.name} plays {played_card}")

    def play_round(self, players: list[PlayerBase]):
        tricks = self.round_info[self.round]['cards']
        for _ in range(tricks):
            self.play_trick(players)


    def determine_trick_winner(self):
        """Determines who wins the trick."""
        pass

    def score_round(self, players: list[PlayerBase]):
        """Calculates each player score"""
        for player in players:
            player.player_score += player.tricks_won
            if player.tricks_won == player.bid:
                player.player_score += 10
                print(f'{player.name} score = {player.player_score}')

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
            print(f'round: {self.round}')
            for player in self.players:
                print(f'{player.name}:{player.hand}')

            self.bidding_phase(self.players)

            self.play_round(self.players)

            self.score_round(self.players)

            self.next_round(self.players)


if __name__ == '__main__':
    # Run the Game
    game = GameState()
    game.play_game()
