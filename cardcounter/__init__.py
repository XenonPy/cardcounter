import random
from collections import Counter

class Card:
    """Represents a single playing card."""
    suits = {'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs', 's': 'Spades'}
    ranks = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        't': '10', 'j': 'Jack', 'q': 'Queen', 'k': 'King', 'a': 'Ace'
    }

    def __init__(self, rank, suit):
        self.rank = rank.lower()
        self.suit = suit.lower()

    def __str__(self):
        return f"{Card.ranks[self.rank]} of {Card.suits[self.suit]}"

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    """Represents a standard deck of 52 playing cards."""
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in 'hdcs' for rank in '23456789tjqka']
        self.discard_pile = []

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self, num_cards):
        """Deal a specified number of cards."""
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal.")
        dealt_cards = [self.cards.pop() for _ in range(num_cards)]
        return dealt_cards

    def discard(self, cards):
        """Move cards to the discard pile."""
        self.discard_pile.extend(cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def reset(self):
        """Reset the deck to a full 52 cards."""
        self.__init__()
        self.shuffle()

    def calculate_percentages(self):
        """Calculate the percentage of each rank remaining in the deck."""
        rank_count = Counter(card.rank for card in self.cards)
        total_cards = len(self.cards)
        return {rank: (count / total_cards) * 100 for rank, count in rank_count.items()}

class CardCounting:
    """Utility functions for card counting and hand evaluation."""

    @staticmethod
    def parse_hand(hand_str):
        """Convert a hand string (e.g., 'kdjc3h7s') into a list of Card objects."""
        hand = []
        for i in range(0, len(hand_str), 2):
            rank, suit = hand_str[i], hand_str[i + 1]
            hand.append(Card(rank, suit))
        return hand

    @staticmethod
    def hand_probability(deck, hand_size, trials=10000):
        """Simulate hand draws to calculate the probability of specific hands."""
        original_deck = deck.cards[:]
        success_count = 0

        for _ in range(trials):
            random.shuffle(deck.cards)
            hand = deck.cards[:hand_size]
            deck.cards = original_deck[:]
            # Define your custom success condition here
            if len(set(card.rank for card in hand)) == hand_size:  # Example: all unique ranks
                success_count += 1

        return success_count / trials * 100

# Example usage
if __name__ == "__main__":
    print("-- Cardcounter Demo --\n")
    deck = Deck()
    deck.shuffle()

    # Deal a hand
    hand = deck.deal(5)
    print("Dealt hand:", hand)

    # Discard some cards
    deck.discard(hand[:2])
    print("Deck after discards:", deck)

    # Calculate remaining card percentages
    percentages = deck.calculate_percentages()
    print("Remaining card percentages:", percentages)

    # Parse a hand from string
    parsed_hand = CardCounting.parse_hand("kdjc3h7s")
    print("Parsed hand:", parsed_hand)

    # Simulate hand probabilities
    probability = CardCounting.hand_probability(deck, 5)
    print("Probability of unique ranks in a 5-card hand:", probability)
