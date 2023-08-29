import random
import time

# Initialize card names and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        composition = ''
        for card in self.deck:
            composition += '\n' + card.__str__()
        return 'Deck Composition: ' + composition

    def shuffle(self):
        self.__init__()
        random.shuffle(self.deck)

    def deal(self):
        selected_card = self.deck.pop()
        return selected_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def __str__(self):
        if len(self.cards) == 1:
            return str(self.cards[0]) + " and Hidden Card"
        elif len(self.cards) == 2:
            string = str(self.cards[0]) + " and " + str(self.cards[1])
            return string
        else:
            string = ""
            for card in self.cards[:-1]:
                string = string + str(card) + ", "
            string += "and " + str(self.cards[-1])
            return string

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Participant:
    def __init__(self):
        self.hand = Hand()
        self.bank = 0

    def hit(self, deck):
        new_card = deck.deal()
        self.hand.add_card(new_card)
        self.hand.adjust_for_ace()

    def stand(self):
        pass

    def show_hand(self):
        string = str(self.hand) + " (" + str(self.hand.value) + ")"
        print(string)


class Player(Participant):
    def __init__(self):
        Participant.__init__(self)
        self.bank = 1000
        self.wins = 0
        self.losses = 0
        self.bet = 0

    def take_bet(self):
        while True:
            try:
                self.bet = int(input('How much would you like to bet?'))
            except ValueError:
                print("Please input a valid answer.")
            else:
                if self.bet > self.bank:
                    print('Sorry, your bet cannot exceed {} '.format(self.bank))
                else:
                    break
        self.bank -= self.bet
        print('Bet: ' + str(self.bet))
        print('Bank: ' + str(self.bank))

    # Ask user whether they would like to hit or stand
    def hit_or_stand(self, deck):
        while True:
            try:
                x = input("Would you like to hit or stand? Input 'h' or 's'")

                # Hit
                if x[0].lower() == 'h':
                    self.hit(deck)
                    print("Player hits.")
                    return True

                # Stand
                elif x[0].lower() == 's':
                    print("Player stands.")
                    return False

                # Invalid input
                else:
                    print("Sorry, please try again.")
                    continue

            # Blank Input
            except IndexError:
                print("Please input a valid answer.")

    def show_hand(self):
        string = str(self.hand) + " (" + str(self.hand.value) + ")"
        print("Your Hand: " + string)


class Dealer(Participant):
    def __init__(self):
        Participant.__init__(self)
        self.bank = 999999999999999999999999999
        self.half_hidden_hand = Hand()

    def show_hand(self):
        string = str(self.hand) + " (" + str(self.hand.value) + ")"
        print("Dealer Hand: " + string)

    # Initial hand only appears at the start of the game
    def show_hand_initial(self):
        self.half_hidden_hand.add_card(self.hand.cards[0])
        string = str(self.half_hidden_hand) + " (" + str(self.half_hidden_hand.value) + ")"
        print("Dealer Hand: " + string)


class Session:
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.shuffle()
        self.games_played = 0

    # Update session stats depending on the outcome
    def player_wins(self):
        print("######################################################################")
        self.games_played += 1
        self.player.bank += self.player.bet * 2
        self.dealer.bank -= self.player.bet
        self.player.bet = 0
        self.player.wins += 1
        return True

    def player_loses(self):
        print("######################################################################")
        self.games_played += 1
        self.dealer.bank += self.player.bet
        self.player.bet = 0
        self.player.losses += 1
        return False

    def push(self):
        print("######################################################################")
        self.games_played += 1
        self.player.bank += self.player.bet
        self.player.bet = 0

    # Plays a single game
    def play_game(self):
        print("######################################################################")
        # Ask for a bet amount
        self.player.take_bet()
        print("----------------------------------------------------------------------")
        time.sleep(2)

        # Deal 2 cards to player
        self.player.hit(self.deck)
        self.player.hit(self.deck)

        # Deal 2 cards to dealer
        self.dealer.hit(self.deck)
        self.dealer.hit(self.deck)

        # Show cards
        self.player.show_hand()
        self.dealer.show_hand_initial()

        # Check for blackjack
        if self.player.hand.value == 21:
            print("BLACKJACK!")
            return self.player_wins()

        # Player's turn
        while True:
            print("----------------------------------------------------------------------")
            still_playing = self.player.hit_or_stand(self.deck)
            self.player.show_hand()
            # Check if player goes over 21
            if self.player.hand.value > 21:
                self.dealer.show_hand()
                print("----------------------------------------------------------------------")
                print("PLAYER BUSTS!")
                return self.player_loses()
            elif still_playing:
                continue
            break

        # Dealer's turn
        time.sleep(2)
        print("----------------------------------------------------------------------")
        print("Dealer Plays...")
        print("----------------------------------------------------------------------")
        time.sleep(2)
        self.dealer.show_hand()
        while True:
            print("----------------------------------------------------------------------")
            time.sleep(2)
            if self.dealer.hand.value > 21:
                print("DEALER BUSTS!")
                return self.player_wins()
            elif self.dealer.hand.value >= self.player.hand.value or self.dealer.hand.value == 21:
                print("Dealer stands.")
                self.dealer.show_hand()
                break
            elif self.dealer.hand.value < self.player.hand.value:
                print("Dealer hits.")
                self.dealer.hit(self.deck)
                self.dealer.show_hand()
                continue
        if self.player.hand.value > self.dealer.hand.value:
            print("PLAYER WINS!")
            return self.player_wins()
        elif self.player.hand.value < self.dealer.hand.value:
            print("DEALER WINS!")
            return self.player_loses()
        else:
            print("PUSH!")
            self.push()

    def show_stats(self):
        print("Bank: %d    Wins: %d    Losses: %d    Games: %d" % (
            self.player.bank, self.player.wins, self.player.losses, self.games_played))

    # Rest hands after every game
    def reset_hands(self):
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        self.dealer.half_hidden_hand = Hand()


# Function to ask player if they would like to play again.
def ask_to_play_again():
    while True:
        playing_status = input("Would you like to play again? Input 'yes' or 'no'")
        if playing_status.lower() == "no":
            print("Have a nice day! Bye.")
            return False
        elif playing_status.lower() == "yes":
            return True
        else:
            print("Please answer with either 'yes' or 'no'")


# Main game loop
def main():
    print("######################################################################")
    print("Welcome to Black Jack!")
    session = Session()

    while True:
        # Check if deck is less than 50% of original size
        if len(session.deck.deck) <= 26:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Shuffling...")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            session.deck.shuffle()
            time.sleep(3)

        session.play_game()
        session.show_stats()
        # First check if they still have money left in the bank
        if session.player.bank <= 0:
            print("Sorry, you have no money left. Goodbye.")
            break

        # Ask player if they want to play again. If not, then leave session.
        if not ask_to_play_again():
            break
        else:
            session.reset_hands()


if __name__ == "__main__":
    main()
