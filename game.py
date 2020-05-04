"""Welcome to the game 'Thalom'!"""

import random
import json
import pandas as pd
import numpy as np


class Player:
    """a player has a name and can pick cards
    and make decision about them"""

    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.cards = []
        self.thalom = False

    def initialize_cards(self):
        """Gives four cards for the player"""
        self.cards = [Card(), Card(),
                      Card(), Card()]
    def score(self):
        """Computes player's score when called"""
        score = 0
        for card in self.cards:
            score += card.value
        return score

    def show_cards_beginning(self):
        """This function explains to the player how the cards are setted
        and shows him/her two of them"""
        print("\n{}, You have four cards".format(self.name))
        print("You can only know two of your cards")
        print("Your cards are referenced as card#1, card#2, card#3 and card#4")
        print("Your card#1 is {} and has a value of {}".format(self.cards[0].name,
                                                               self.cards[0].value))
        print("Your card#2 is {} and has a value of {}".format(self.cards[1].name,
                                                               self.cards[1].value))
        print()

    def launch_turn(self):
        """Defines the process of a player's turn
        and communicates with him"""
        print("\n{} it's your turn !".format(self.name))
        if Card.rejected_cards == []:
            # if complied only in first turn or after shuffle
            new_card = self.pick()
            self.choose_action(new_card)
        else:
            last_card_rejected = Card.rejected_cards[-1]
            print("\nYou can either take the last rejected",
                  "card wich is {} or pick a new card".format(last_card_rejected.name))
            pick_or_steal = input("\nEnter 'P'' to pick a card or enter anything to take the last rejected card ").lower()
            if pick_or_steal == 'p':
                new_card = self.pick()
                self.choose_action(new_card)
            else:
                print("\nYou decided to take {}, you have to decide which card you reject".format(last_card_rejected.name))
                position = self.choose_position()
                self.steal(position)


    def say_thalom(self):
        """'Thalom' will stop the game before player's next game"""
        thalom = input("\nDo you want to say 'Thalom'? \nIf you do, enter 'T' , if not, press 'enter' ").lower()
        if thalom == 't':
            self.thalom = True


    def choose_action(self, new_card):
        """When a player picks radom card,
        he has to choose if he keeps it"""
        if len(self.cards) == 0:
            print("You don't have any cards left!",
                  "\nYou're forced to reject the card you picked")
            Card.rejected_cards.append(new_card)
        else:
            choice = input("\nDo you want to keep it? y/n ? ").lower()
            if choice == 'y':
                print("\nYou chose to keep {}".format(new_card.name))
                print("now you have to choose which card you let go")
                position = self.choose_position()
                new_rejected_card = self.cards[position - 1]
                Card.rejected_cards.append(new_rejected_card)
                print("\nYou rejected {}".format(new_rejected_card.name))
                self.cards[position - 1] = new_card
            else:
                Card.rejected_cards.append(new_card)

    def pick(self):
        """This function makes the player pick a
        card and inform him the name of this card"""
        input("\nPress enter to pick a card ! ")
        new_card = Card()
        print("\n{} You picked {}".format(self.name, new_card.name))
        return new_card

    def steal(self, position):
        """When decided, the player can switch one
        of his cards with the card rejected by
        the last player who played before"""
        stolen_card = Card.rejected_cards.pop()
        new_rejected_card = self.cards[position - 1]
        Card.rejected_cards.append(new_rejected_card)
        self.cards[position - 1] = stolen_card
        print("\nYou rejected {}".format(new_rejected_card.name))

    def throw(self):
        """A player can throw a one of his card over
        the last card rejected but they have to have the same value
        He can can also choose not to do anything"""
        last_card_rejected = Card.rejected_cards[-1]
        print("\nINFO : {} you chose to throw a card".format(self.name))
        print("The last card that was rejected is {}".format(last_card_rejected.name))
        position = self.choose_position()
        if self.cards[position - 1].value == last_card_rejected.value:
            thrown_card = self.cards.pop(position - 1)
            Card.rejected_cards.append(thrown_card)
            print("All good!")
            print("you threw {}".format(thrown_card.name))
        else:
            print("Sorry but you can't throw this card")
            print("because the values are different...")
            new_card = Card()
            self.cards.append(new_card)
            print("A new card has been added to your cards in the last position")


    def choose_position(self):
        """Player can choose a card out of a player's deck
        (Could be from his!!!)"""
        print("\nWhich card?")
        while True:
            position = input("Enter a number between 1 and {} ".format(len(self.cards)))
            if not position.isdigit():
                print("You have to enter a number !")
            else:
                position = int(position)
                if 0 < position <= len(self.cards):
                    break
                print("You didn't enter a correct number!")
        return position

    def power(self, list_of_players):
        """Player's have a special power if the card
        he rejects is an Ace, a Jack or a Queen"""
        last_card_rejected = Card.rejected_cards[-1]
        if last_card_rejected.power:
            power_type = last_card_rejected.value
            if power_type == 1:
                self.ace_power(list_of_players)
            if power_type == 11:
                self.jack_power(list_of_players)
            if power_type == 12:
                self.queen_power(list_of_players)

    def ace_power(self, list_of_players):
        """Ace power is making someone pick a card"""
        print("{}, the ace you rejected gives you the power to".format(self.name))
        print("make someone pick a card")
        players_names = [player.name.lower() for player in list_of_players]
        players_names_secure = players_names.copy()
        players_names_secure.remove(self.name.lower())
        while True:
            print("Enter the name of your victim")
            print("among these names : ", players_names_secure)
            victim = input().lower()
            if victim in players_names_secure:
                victim_index = players_names.index(victim)
                victim = list_of_players[victim_index]
                new_card = Card()
                victim.cards.append(new_card)
                print("{}, {} made you pick a card. It's been added as your last card".format(victim.name, self.name))
                break
            print("Please, enter a correct name")

    def jack_power(self, list_of_players):
        """Jacks is about messing up the game by switching cards"""
        print("{}, the jack you rejected gives you the power to".format(self.name))
        print("exchange two cards!")
        players_names = [player.name.lower() for player in list_of_players]
        while True:
            print("\nEnter the names of the players that are going to switch cards")
            print("You can switch yourself and someone else")
            print("or switch cards between two players")
            print("Remember enter names among these : ", players_names)
            print("Enter first player's name! (Can be yourself!)")
            player_a = input().lower()
            print("Enter second player's name")
            player_b = input().lower()
            if (player_a and player_b in players_names and player_a != player_b):
                player_a_index = players_names.index(player_a)
                player_a = list_of_players[player_a_index]

                player_b_index = players_names.index(player_b)
                player_b = list_of_players[player_b_index]

                print("\nYou have to decide wich card from {} you want to move".format(player_a.name))
                position_a = player_a.choose_position()

                print("\nYou now have to decide wich card from {} you want to move".format(player_b.name))
                position_b = player_b.choose_position()

                player_a.cards[position_a - 1], player_b.cards[position_b - 1] = player_b.cards[position_b - 1], player_a.cards[position_a - 1]
                print("Card  #{} from {} and card #{} from {} have been switched!".format(position_a, player_a.name, position_b, player_b.name))
                break
            print("Please, enter correct names!")

    def queen_power(self, list_of_players):
        """Queen gives the power to see a card from an opponent"""
        print("{}, the queen you rejected gives you the power to".format(self.name))
        print("see one card from someone (but not yourself!)")
        players_names = [player.name.lower() for player in list_of_players]
        players_names_secure = players_names.copy()
        players_names_secure.remove(self.name.lower())#ATTENTION AUX INDEX!
        while True:
            print("Enter the name of your victim")
            print("among these names : ", players_names_secure)
            victim = input().lower()
            if victim in players_names_secure: #On ne peut pas regarder son jeu!
                victim_index = players_names.index(victim) #mais il faut recuperer l'index dans la liste original
                victim = list_of_players[victim_index]
                position = victim.choose_position()
                spied_card = victim.cards[position - 1]
                print("{} has {} in position {}".format(victim.name, spied_card.name, position))
                break
            print("Please, enter a correct name")

class Card:
    """A card is a classic playing
    card that has a value between 1 and 13"""
    DECK = {}
    rejected_cards = []

    def __init__(self):
        random_card = Card.pick_a_random_card_from_deck()
        self.name = random_card[0]
        self.value = random_card[1]
        if self.value in [1, 11, 12]:
            self.power = True
        else:
            self.power = False

    @classmethod
    def initialize_deck_from_json(cls):
        """Get the infos about json file's deck"""
        cls.DECK = {}
        path = "deck.json"
        with open(path) as deck_file:
            deck_raw = json.load(deck_file)
        for card in deck_raw:
            cls.DECK.update(card)

    @classmethod
    def pick_a_random_card_from_deck(cls):
        """used in __init__() Gets a random card and pops it
        from the deck so that next players don't pick this card"""
        card_key = random.choice(list(cls.DECK.keys()))
        card_value = cls.DECK.pop(card_key)
        return card_key, card_value

    @classmethod
    def shuffle_new_deck(cls):
        """Creates a new deck from the rejected cards"""
        if not cls.DECK:
            print("Deck's empty! We gotta shuffle a new one with the rejected cards")
            for card in cls.rejected_cards:
                cls.DECK[card.name] = card.value
            cls.rejected_cards = []

class ScoreChart:
    """ScoreChart is an object that's basically a pandas dataframe
    rows are rounds, columns are players"""

    def __init__(self, list_of_players):
        zeros = np.zeros(len(list_of_players), int)
        zeros = np.array([zeros])
        players_names = [player.name for player in list_of_players]
        self.dataframe = pd.DataFrame(index=["Round 1"], data=zeros, columns=players_names)

    def update_scores(self, rounds, list_of_players):
        """Adds scores from last round in the score chart"""
        scores = [player.score() for player in list_of_players]
        scores = np.array([scores])
        # score_chart = self.dataframe
        if rounds == 1:
            self.dataframe.iloc[0] = scores
            self.compute_totals_scores()
        else:
            new_row_scores = pd.DataFrame(index=["Round {}".format(rounds)], data=scores, columns=self.dataframe.columns)
            self.dataframe = self.dataframe.drop(index="Totals")
            self.dataframe = pd.concat([self.dataframe, new_row_scores])
            self.compute_totals_scores()

    def compute_totals_scores(self):
        """sums up the scores of everyplayer an stores it in the final line"""
        final_scores = [sum(self.dataframe[player]) for player in self.dataframe.columns]
        final_scores = np.array([final_scores])
        total_row = pd.DataFrame(index=["Totals"], data=final_scores, columns=self.dataframe.columns)
        self.dataframe = pd.concat([self.dataframe, total_row])
        print("Here's the Scores' Chart !!!")
        print(self.dataframe)

    def determine_winner(self):
        """Determines the winner using
        score chart's last line"""
        final_scores = self.dataframe.loc["Totals"]
        winner = final_scores.idxmin()
        print("\nThe winner is : {} !!!".format(winner.upper()))

def initialize_players():
    """This fucntion creates the players
    the list_of_players that is going to be
    used to iterate for next functions.
    list_of_players contains Player objects"""
    while True:
        nb_of_players = input("\nEntrez le nombre de joueurs : ")
        if not nb_of_players.isdigit():
            print("You have to enter a number!")
        else:
            nb_of_players = int(nb_of_players)
            if nb_of_players < 2:
                print("You have to enter at least two!")
            else:
                break
    nb_of_players = int(nb_of_players)
    list_of_players = [] #This list is going to be returned
    names_secure = [] #stores player's names in lower mode for security
    for index in range(1, nb_of_players+1):
        while True:
            player_name = input("Entrer le nom du joueur {} ".format(index))
            if (player_name.lower() == 'end' or player_name.lower() in names_secure):
                print("Incorrect Name")
            else:
                names_secure.append(player_name.lower())
                new_player = Player(player_name, index)
                list_of_players.append(new_player)
                break
    return list_of_players

def round_loop(list_of_players, score_chart):
    """Everything that happens in a round is here"""
    rounds = 0
    while True:
        rounds += 1
        initialize_round(list_of_players)
        inform_players(list_of_players)
        loop_until_thalom(list_of_players)
        give_round_scores(list_of_players)
        score_chart.update_scores(rounds, list_of_players)
        # score_chart.compute_totals_scores()
        if not continue_playing():
            break

def initialize_round(list_of_players):
    """Makes the cards and the players ready for a new round"""
    Card.rejected_cards = []
    Card.initialize_deck_from_json()
    for player in list_of_players:
        player.initialize_cards()
        player.thalom = False

def inform_players(list_of_players):
    """At the begining of the game every player
    needs to know two of his cards"""
    for player in list_of_players:
        player.show_cards_beginning()
        input("Press enter to pass your turn")
        print()

def loop_until_thalom(list_of_players):
    """Main loop that stops before the game
    goes back to the player who said thalom"""
    player_that_said_thalom = 0
    someone_said_thalom = False
    check = True
    while check: #makes the loop re-read list_of_players
        for player in list_of_players:
            if player == player_that_said_thalom:
                check = False
                break
            player.launch_turn()
            player.power(list_of_players)
            if not someone_said_thalom:
                player.say_thalom()
            throwing_proposition(list_of_players)
            Card.shuffle_new_deck() #happens only if the deck's empty
            if player.thalom:
                player_that_said_thalom = player
                someone_said_thalom = True

def throwing_proposition(list_of_players):
    """Players can tell if they want to throw cards"""
    list_of_players_name = [player.name.lower() for player in list_of_players]
    while True:
        print("\nIf you want to throw a card over {},".format(Card.rejected_cards[-1].name))
        print("Write your name and press enter")
        print("If everyone's done enter 'END' to continue the game")
        user_entry = input().lower()
        if user_entry == 'end':
            break
        if user_entry in list_of_players_name:
            get_player_index = list_of_players_name.index(user_entry)
            player = list_of_players[get_player_index]
            player.throw()
            print("Anyone else?")
        else:
            print("Incorrect entry")

def give_round_scores(list_of_players):
    """Informs enveryone about the round's scores
    and the cards of the players"""
    print("\nThe round has ended !\nWe shall now unveil the cards and the scores!")

    for player in list_of_players:
        cards = [card.name for card in player.cards]
        cards_string = " "
        for card in cards:
            cards_string += card + ", "
        cards_string = cards_string[:-2]
        print("\n{} has these cards: ".format(player.name), cards_string)
        print("{} has a score of {}".format(player.name, player.score()))
    final_scores = [player.score() for player in list_of_players]
    min_score = min(final_scores)
    winners_index = [i for i, x in enumerate(final_scores) if x == min_score]
    if len(winners_index) == 1:
        index_winner = winners_index[0]
        winner = list_of_players[index_winner]
        print(winner.name, "won the round with a score of {}".format(winner.score()))
    if len(winners_index) > 1:
        print("It's a tie!")
        winners_names = ""
        winners = [list_of_players[i] for i in winners_index]
        for winner in winners:
            winners_names += winner.name
        print(winners_names, "won the round with a score of ", str(min_score))

def continue_playing():
    """ends the round loop or launches a new round"""
    while True:
        print("\nDo you want to continue? y/n")
        choice = input().lower()
        if choice == 'y':
            return True
        if choice == 'n':
            return False
        print("Incorrect entry")

def give_winner(score_chart):
    """who's the WINNNER!"""
    score_chart.determine_winner()


def main():
    """You know....."""

    list_of_players = initialize_players()
    score_chart = ScoreChart(list_of_players)

    round_loop(list_of_players, score_chart)

    give_winner(score_chart)

if __name__ == "__main__":
    main()
