from cardcounter import Card, Deck, CardCounting
from cardcounter.cribbage import Cribbage
deck = Deck()
deck.shuffle()

print("-- Cribbage --\n")

# Input hand size and discards
hand_size = int(input("Enter hand size (5 or 6): "))
player_hand = [deck.draw_card() for _ in range(hand_size)]
print("Your hand:", ', '.join(str(card) for card in player_hand))

draw_type = str(hand_size)
best_discard = Cribbage.best_discard(player_hand, draw_type)
print("Best cards to discard:", ', '.join(str(card) for card in best_discard))

for card in best_discard:
    player_hand.remove(card)

print("Your remaining hand:", ', '.join(str(card) for card in player_hand))

# Pegging phase
pegging_total = 0
played_cards = []
num_players = int(input("Enter number of players: "))
while player_hand:
    print("Current pegging total:", pegging_total)
    print("Played cards:", ', '.join(str(card) for card in played_cards))

    # Player's turn
    if pegging_total < 31:
        best_card = Cribbage.best_card_to_play(player_hand, played_cards, deck)
        print("Best card to play:", best_card)
        pegging_total += int(CardCounting.card_value(best_card))
        played_cards.append(best_card)
        player_hand.remove(best_card)

        if pegging_total == 31:
            print("31 reached! Resetting pegging total.")
            pegging_total = 0

    # Other players' turns
    for _ in range(num_players - 1):
        opponent_card_notation = input("Enter opponent's played card (e.g., kd, jc, 3h, 7s) or press Enter if they go: ").lower()
        if not opponent_card_notation:
            print("Opponent goes.")
            continue

        opponent_card = Card(opponent_card_notation[0], opponent_card_notation[1])
        pegging_total += int(CardCounting.card_value(opponent_card))
        played_cards.append(opponent_card)

        if pegging_total == 31:
            print("31 reached! Resetting pegging total.")
            pegging_total = 0

print("Pegging phase over! Final played cards:", ', '.join(str(card) for card in played_cards))