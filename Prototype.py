"""Code for answer to problem B4 of Programing 2 course exam,
done without parallelization to begin with. More to be added on later."""

import numpy as np
import pandas as pd
import time
import math

#Sequence: 
# Dealer gives all players 2 cards
# Big blind/small blind
# Players call/fold/raise
# Flop
# Players call/fold/raise
# Turn
# Players call/fold/raise
# River
# Players call/fold/raise
# Remaining players show cards

class Poker():
    class Deck_of_cards():

        def __init__(self, value):
            self.value = value
            suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
            if self.value > 0 and self.value < 53:
                self.suit = suits[(value - 1) // 13]
            else:
                raise ValueError("Deck of cards only accepts integers between 1 and 52.")

        def __str__(self):
            card_deck_52 = ["A", "2", "3", "4", "5",\
                            "6", "7", "8", "9", "10",\
                            "J", "Q", "K"]
            index = self.value%13
            return card_deck_52[(index-1)] + " " + self.suit
        
        #Method for the representative value of each card. A = 14, K = 13, etc.
        def absolute_value(self):
            if self.value%13 == 1 or self.value%13 == 0:
                return (self.value%13 + 13)
            else:
                return self.value%13
        
        #If two hands with best card that have same suit = same hand.
        #-> Split the pot. No ranking of suits. Only absoulte value.
        
        #Comparison operator overloading
        def __eq__(self, other):
            return self.absolute_value() == other.absolute_value()

        def __ne__(self, other):
            return self.absolute_value() != other.absolute_value()

        def __lt__(self, other):
            return self.absolute_value() < other.absolute_value()

        def __le__(self, other):
            return self.absolute_value() <= other.absolute_value()

        def __gt__(self, other):
            return self.absolute_value() > other.absolute_value()
        
        def __ge__(self, other):
            return self.absolute_value() >= other.absolute_value()
            
    #Poker class initialization
    def __init__(self, players, deck=None):
        self.players = players
        if deck==None:
            deck = [*range(1,53)]
            # deck = [Poker.Deck_of_cards(i) for i in range(1,53)] See how to implement later
        self.deck = deck

    def shuffle(self):
        np.random.shuffle(self.deck)
        return self.deck
        
    def deal(self, player): #Deals two cards, removes from deck
        if self.deck == [*range(1, 53)]:
            self.shuffle()

        pocket_cards = np.random.choice(self.deck, size=2, replace=False, p=None)
        self.deck = [card for card in self.deck if card not in pocket_cards]
        return [Poker.Deck_of_cards(card) for card in pocket_cards]
    
    def flop(self, game_cards=None): #Turns three cards, removes from deck
        if game_cards == None:
            game_cards = np.random.choice(self.deck, size=3, replace=False, p=None)
            self.deck = [card for card in self.deck if card not in game_cards]
            return [Poker.Deck_of_cards(card) for card in game_cards]
        
    def turn(self, game_cards):
        if len(game_cards) == 3:
            turn_card = np.random.choice(self.deck, size=1, replace=False, p=None)
            game_cards = np.append(game_cards, turn_card)
            # Remove the dealt cards from the deck
            self.deck.remove(turn_card)
            return [Poker.Deck_of_cards(card) for card in game_cards]
        else:
            pass
    
    def river(self, game_cards):
        if len(game_cards) == 4:
            river_card = np.random.choice(self.deck, size=1, replace=False, p=None)
            game_cards = np.append(game_cards, river_card)
            # Remove the dealt cards from the deck
            self.deck.remove(river_card)
            return [Poker.Deck_of_cards(card) for card in game_cards]
        else:
            pass
        
    # Define hand rankings
    hand_rankings = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush",
        "Royal Flush"
    ]
        
    def evaluate_hand(self, hand):
        # Count the occurrences of each card value
        value_counts = {}
        for card in hand:
            absolute_value = card.absolute_value()
            value_counts[absolute_value] = value_counts.get(absolute_value, 0) + 1
            
        # Check for flush
        suits_count = {suit: sum(1 for card in hand if card.suit == suit) for suit in set(card.suit for card in hand)}
        is_flush = any(count >= 5 for count in suits_count.values())

        # Check for straight
        values = sorted(card.absolute_value() for card in hand)
        is_straight = (max(values) - min(values) + 1) == len(values) or \
                    (14 in values and 2 in values and 3 in values and 4 in values and 5 in values)
                    
        # Determine rank of the hand
        if is_flush and is_straight and values[-1] == 14 and values[0] == 10:
            return "Royal Flush", value_counts
        elif is_flush and is_straight:
            return "Straight Flush", value_counts
        elif max(value_counts.values()) == 4:
            return "Four of a Kind", value_counts
        elif 3 in value_counts.values() and 2 in value_counts.values():
            return "Full House", value_counts
        elif is_flush:
            return "Flush", value_counts, suits_count
        elif is_straight:
            return "Straight", value_counts
        elif max(value_counts.values()) == 3:
            return "Three of a Kind", value_counts
        elif list(value_counts.values()).count(2) == 2:
            return "Two Pair", value_counts
        elif max(value_counts.values()) == 2:
            return "One Pair", value_counts
        else:
            return "High Card", value_counts

    def compare_hands(self, hand1, hand2):
        rank1, info1 = self.evaluate_hand(hand1)
        rank2, info2 = self.evaluate_hand(hand2)
        
        # Compare hand ranks
        if self.hand_rankings.index(rank1) > self.hand_rankings.index(rank2):
            return f"Hand 1, by highest hand rank: {rank1, info1}"
        elif self.hand_rankings.index(rank1) < self.hand_rankings.index(rank2):
            return f"Hand 2, by highest hand rank: {rank2, info2}"
        elif rank1 == rank2: #Equal rank, go by highest card and secondary card
            if rank1 in ["One Pair", "Three of a Kind", "Four of a Kind"]:
                max_key_info1 = max(info1, key=lambda k: info1[k])
                max_key_info2 = max(info2, key=lambda k: info2[k])
                if max_key_info1 > max_key_info2:
                    return f"Hand 1, by higher ranking hand: {rank1}, ({info1})"
                elif max_key_info1 < max_key_info2:
                    return f"Hand 2, by higher ranking hand: {rank2}, ({info2})"
                
            if rank1 == "Two Pair":
                hand1_pairs = sorted([card for card, count in info1.items() if count == 2], reverse=True)
                hand2_pairs = sorted([card for card, count in info2.items() if count == 2], reverse=True)
                
                if hand1_pairs[0] > hand2_pairs[0]:
                    return f"Hand 1, by highest pair: {hand1_pairs[0]}"
                if hand1_pairs[0] < hand2_pairs[0]:
                    return f"Hand 2, by highest pair: {hand2_pairs[0]}"
                elif hand1_pairs[1] > hand2_pairs[1]:
                    return f"Hand 1, by highest secondary pair: {hand1_pairs[1]}"
                elif hand1_pairs[1] < hand2_pairs[1]:
                    return f"Hand 2, by highest secondary pair: {hand1_pairs[1]}"
                
            if rank1 == "Full House":
                hand1_three_of_a_kind = max([card for card, count in info1.items() if count == 3])
                hand2_three_of_a_kind = max([card for card, count in info2.items() if count == 3])
                
                # Compare three of a kind
                if hand1_three_of_a_kind > hand2_three_of_a_kind:
                    return f"Hand 1, by highest three of a kind: {hand1_three_of_a_kind}"
                elif hand1_three_of_a_kind < hand2_three_of_a_kind:
                    return f"Hand 2, by highest three of a kind: {hand2_three_of_a_kind}"

            hand1_values = sorted(list(info1.keys())[0:2], reverse=True)
            hand2_values = sorted(list(info2.keys())[0:2], reverse=True)
            print(hand1_values)
            print(hand2_values)
            if hand1_values[0] > hand2_values[0]:
                return f"Hand 1, by highest card: {str(hand1[0])}"
            elif hand1_values[0] < hand2_values[0]:
                return f"Hand 2, by highest card: {str(hand2[0])}"
            elif hand1_values[1] > hand2_values[1]:
                return f"Hand 1, by highest kicker: {str(hand1[1])}"
            elif hand1_values[1] < hand2_values[1]:
                return f"Hand 2, by highest kicker: {str(hand2[1])}"
            else:
                return "split the pot"


def main():
    print("Hello gambler! \n")
    # print("~~~ Testing Deck_of_cards method ~~~")
    # Ace_of_spades = Poker.Deck_of_cards(40)
    # print("Card:", Ace_of_spades)
    # print("Corresponding value:", Ace_of_spades.value)
    # print("Corresponding suit:", Ace_of_spades.suit)
    # Two_of_diamonds = Poker.Deck_of_cards(15)
    # print("Card:", Two_of_diamonds)
    # print("Comparing values:")
    # print("Is A Spades > 2 Diamonds?:", Ace_of_spades > Two_of_diamonds)
    # Ace_of_hearts = Poker.Deck_of_cards(1)
    # print("Is A Hearts == A Spades?:", Ace_of_hearts == Ace_of_spades, '\n')
    # print("Testing Deck_of_cards --> OK \n")

    # print("~~~ Testing class Poker, with 2 players ~~~")
    # game = Poker(2) #2 players
    # print("Initial deck:", game.deck)
    # player1_cards = game.deal(player=1)
    # print("Player 1's cards:", ", ".join(map(str, player1_cards)))
    # player2_cards = game.deal(player=2)
    # print("Player 2's cards:", ", ".join(map(str, player2_cards)))
    # flop = game.flop()
    # print("Flop revealed:", ", ".join(map(str, flop)))
    # turn = game.turn([card.value for card in flop])
    # print("Turn revealed:", ", ".join(map(str, turn)))
    # river = game.river([card.value for card in turn])
    # print("River revealed:", ", ".join(map(str, river)))
    # print("Preliminary version of dealing --> OK \n")

    # print("~~~ Trying class Poker, evaluating one hand ~~~")
    # game = Poker(2)
    # hand = [game.Deck_of_cards(14), game.Deck_of_cards(2), game.Deck_of_cards(27), game.Deck_of_cards(37), game.Deck_of_cards(24)]
    # for card in hand:
    #     print(card)
    # rank, info = game.evaluate_hand(hand)
    # print("Hand Rank:", rank)
    # info = [game.Deck_of_cards(key).absolute_value() for key, value in info.items() for _ in range(value)]
    # print("Hand Info:", info)

    # # Convert numerical values to string representations in the info dictionary
    # # info_values_strings = [str(game.Deck_of_cards(value)) for value in info["values"]]

    # # print("Hand:", ", ".join(info_values_strings))
    # print("Preliminary version of evaluation OK \n")

    # print("~~~ Trying class Poker, evaluating and comparing two hands with pre-determined river ~~~")
    # hand1 = [game.Deck_of_cards(1), game.Deck_of_cards(46)]
    # hand2 = [game.Deck_of_cards(14), game.Deck_of_cards(26)]
    # # river = [game.Deck_of_cards(40), game.Deck_of_cards(27), game.Deck_of_cards(51), game.Deck_of_cards(42), game.Deck_of_cards(28)]
    # river = [game.Deck_of_cards(3), game.Deck_of_cards(22), game.Deck_of_cards(51), game.Deck_of_cards(42), game.Deck_of_cards(28)]
    # print("Player 1's hand:")
    # # print(hand1)
    # print("Player 1's cards:", ", ".join(map(str, hand1)))
    # for card in hand1:
    #     print(card)
    # print("")
    # print("Player 2's hand:")
    # for card in hand2:
    #     print(card)
    # print("")
    # print("River:")
    # for card in river:
    #     print(card)
    # print("")
    # hand1.extend(river)
    # # print("Player 1's cards:", ", ".join(map(str, hand1[:2])))
    # hand2.extend(river)
    # # print("Player 1's cards:", ", ".join(map(str, hand2[:2])))
    # print("")
    # rank1, info1 = game.evaluate_hand(hand1)
    # print("Hand Rank:", rank1)
    # print("Hand Info:", info1, '\n')
    # # hand1_values = [game.Deck_of_cards(key).absolute_value() for key, value in info1.items() for _ in range(value)]
    # # print(hand1_values)

    # rank2, info2 = game.evaluate_hand(hand2)
    # print("Hand Rank:", rank2)
    # print("Hand Info:", info2)

    # # rank, info = game.evaluate_hand(hand1)
    # # rank, info = game.evaluate_hand(hand2)
    # winner = game.compare_hands(hand1, hand2)
    # print("Winner:\n", winner, '\n')
    
    print("~~~ Poker, comparing two hands with dealer ~~~")
    
    game2 = Poker(2) #2 players
    player1_cards2 = game2.deal(player=1)
    print("Player 1's cards:", ", ".join(map(str, player1_cards2)))
    player2_cards2 = game2.deal(player=2)
    print("Player 2's cards:", ", ".join(map(str, player2_cards2)))
    flop = game2.flop()
    print("Flop revealed:", ", ".join(map(str, flop)))
    turn = game2.turn([card.value for card in flop])
    print("Turn revealed:", ", ".join(map(str, turn)))
    river = game2.river([card.value for card in turn])
    print("River revealed:", ", ".join(map(str, river)))
    
    player1_cards2.extend(river)
    player2_cards2.extend(river)
    
    rank11, info11 = game2.evaluate_hand(player1_cards2)
    print("Hand Rank:", rank11)
    print("Hand Info:", info11, '\n')

    rank22, info22 = game2.evaluate_hand(player2_cards2)
    print("Hand Rank:", rank22)
    print("Hand Info:", info22)
    
    winner2 = game2.compare_hands(player1_cards2, player2_cards2)
    print('\033[4m' + 'Winner:' + '\033[0m \n', winner2)


    # print("Amount of cards left after dealing 2 players:", len(game.deck))
    # print("\n!!!Call/raise/fold, fix input for player 1!!!")
    # print("Sequencing needs to be fixed, make the player 2 always call for testing")
    # print("Make hands work first before fixing the sequencing\n")
    # Full_deck_of_cards = [*range(1,53)]
    # for i in Full_deck_of_cards:
    #     draw = Poker.Deck_of_cards(i)
    #     print(draw)

if __name__ == "__main__":
    main()
    print('\n')
    print('Over and out')



# Parallelization example:
    # def dice(n):
# 	"""Method thats simulates a broken dice. Do not modify."""
# 	from random import choice
# 	return [choice([1,2,3,4,5,5]) for _ in range(n)]

# def dice_average():
#     """Method that runs dice(n), with n=100000, twenty times in parallel.
#     Then, compute the average of all the throws, and return that value."""
#     for n in [10000]:
#         throws = [n for _ in range(20)]
#         print(throws)
#         import concurrent.futures as future
#         with future.ThreadPoolExecutor() as ex:
#             dices_throws = list(ex.map(dice, throws))
#         flat_throws = [i for sublist in dices_throws for i in sublist]
#         return (sum(flat_throws)/(n*20))