from itertools import combinations

class Cribbage:
    """Submodule for Cribbage-specific operations."""

    @staticmethod
    def calculate_fifteens(hand):
        """Calculate all combinations of cards in the hand that sum to 15."""
        values = {str(i): i for i in range(2, 10)}
        values.update({"t": 10, "j": 10, "q": 10, "k": 10, "a": 1})
        
        card_values = [values[card.rank] for card in hand]
        fifteens = []

        for r in range(2, len(hand) + 1):
            for combo in combinations(card_values, r):
                if sum(combo) == 15:
                    fifteens.append(combo)

        return fifteens

    @staticmethod
    def best_discard(hand, draw_type):
        """Find the best cards to discard based on cribbage strategy.

        Parameters:
        - hand: List of Card objects representing the player's hand.
        - draw_type: '5' for draw 5, discard 1 or '6' for draw 6, discard 2.

        Returns:
        - The best cards to discard as a list of Card objects.
        """
        if draw_type not in ('5', '6'):
            raise ValueError("Invalid draw type. Use '5' for discard 1 or '6' for discard 2.")

        num_discard = 1 if draw_type == '5' else 2

        best_discard = None
        max_score = float('-inf')

        for discard_combo in combinations(hand, num_discard):
            remaining_hand = [card for card in hand if card not in discard_combo]
            score = Cribbage.hand_score(remaining_hand)

            if score > max_score:
                max_score = score
                best_discard = discard_combo

        return list(best_discard)

    @staticmethod
    def hand_score(hand):
        """Calculate the score of a cribbage hand."""
        fifteens = Cribbage.calculate_fifteens(hand)
        return len(fifteens) * 2  # Each fifteen scores 2 points

    @staticmethod
    def best_card_to_play(pegging_hand, played_cards, deck):
        """Determine the best card to play during pegging based on current cards and card counting.

        Parameters:
        - pegging_hand: List of Card objects representing the player's hand.
        - played_cards: List of Card objects representing cards already played.
        - deck: Deck object for card counting.

        Returns:
        - The best card to play as a Card object.
        """
        values = {str(i): i for i in range(2, 10)}
        values.update({"t": 10, "j": 10, "q": 10, "k": 10, "a": 1})
        
        remaining_count = deck.calculate_percentages()
        best_card = None
        best_score = float('-inf')

        for card in pegging_hand:
            potential_score = Cribbage.simulate_pegging_score(card, played_cards, values, remaining_count)

            if potential_score > best_score:
                best_score = potential_score
                best_card = card

        return best_card

    @staticmethod
    def simulate_pegging_score(card, played_cards, values, remaining_count):
        """Simulate the pegging score for a card."""
        current_score = 0
        played_values = [values[card.rank] for card in played_cards]
        total = sum(played_values) + values[card.rank]

        if total == 15:
            current_score += 2  # 15s in pegging score 2 points

        if total <= 31:
            current_score += 1  # Playing the last card within 31 scores 1 point

        # Avoid leaving the total at 5
        if total == 5:
            current_score -= 1

        return current_score

