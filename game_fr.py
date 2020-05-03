"""Bienvenue au Jeu Thalom!"""

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
        print("\n{}, tu as 4 cartes".format(self.name))
        print("Tu ne peux en voir que 2")
        print("Tes cartes sont reférencées comme : carte#1, carte#2, carte#3 and carte#4")
        print("Ta carte#1 est {} et a une valeur de {}".format(self.cards[0].name,
                                                               self.cards[0].value))
        print("Ta carte#2 est {} et a une valeur de {}".format(self.cards[1].name,
                                                               self.cards[1].value))
        print()

    def launch_turn(self):
        """Defines the process of a player's turn
        and communicates with him"""
        print("\n{} c'est ton tour !".format(self.name))
        if Card.rejected_cards == []:
            # if complied only in first turn or after shuffle
            new_card = self.pick()
            self.choose_action(new_card)
        else:
            last_card_rejected = Card.rejected_cards[-1]
            print("\nTu peux soit prendre la dernière jetée",
                  "qui est {} ou piocher".format(last_card_rejected.name))
            pick_or_steal = input("\nEntre 'P'' pour piocher ou entre n'importequoi pour prendre la dernière carte jetée ").lower()
            if pick_or_steal == 'p':
                new_card = self.pick()
                self.choose_action(new_card)
            else:
                print("\nTu as choisi de garder {}, tu dois choisir quelle carte tu jettes".format(last_card_rejected.name))
                position = self.choose_position()
                self.steal(position)


    def say_thalom(self):
        """'Thalom' will stop the game before player's next game"""
        thalom = input("\nVeux tu dire 'Thalom'? \nSi oui, entre 'T' , sinon tape entrée ").lower()
        if thalom == 't':
            self.thalom = True


    def choose_action(self, new_card):
        """When a player picks radom card,
        he has to choose if he keeps it"""
        if len(self.cards) == 0:
            print("Tu n'as plus de cartes!!",
                  "\nTu es obligé de jeter la carte piochée")
            Card.rejected_cards.append(new_card)
        else:
            choice = input("\nVeux-tu la garder o/n ? ").lower()
            if choice == 'o':
                print("\nTu as a choisi de garder {}".format(new_card.name))
                print("tu dois choisir quelle carte tu jettes")
                position = self.choose_position()
                new_rejected_card = self.cards[position - 1]
                Card.rejected_cards.append(new_rejected_card)
                print("\nTu as jeté {}".format(new_rejected_card.name))
                self.cards[position - 1] = new_card
            else:
                Card.rejected_cards.append(new_card)

    def pick(self):
        """This function makes the player pick a
        card and inform him the name of this card"""
        input("\nAppuie sur entrée pour piocher! ")
        new_card = Card()
        print("\n{} tu as pioché {}".format(self.name, new_card.name))
        return new_card

    def steal(self, position):
        """When decided, the player can switch one
        of his cards with the card rejected by
        the last player who played before"""
        stolen_card = Card.rejected_cards.pop()
        new_rejected_card = self.cards[position - 1]
        Card.rejected_cards.append(new_rejected_card)
        self.cards[position - 1] = stolen_card
        print("\nTu as jeté {}".format(new_rejected_card.name))

    def throw(self):
        """A player can throw a one of his card over
        the last card rejected but they have to have the same value
        He can can also choose not to do anything"""
        last_card_rejected = Card.rejected_cards[-1]
        print("\nINFO : {} tu as choisi de défausser une carte".format(self.name))
        print("La dernière carte jetée est {}".format(last_card_rejected.name))
        position = self.choose_position()
        if self.cards[position - 1].value == last_card_rejected.value:
            thrown_card = self.cards.pop(position - 1)
            Card.rejected_cards.append(thrown_card)
            print("C'est bon!")
            print("Tu as défaussé {}".format(thrown_card.name))
        else:
            print("Désolé, tu ne peux pas défausser cette carte")
            print("car les valeurs sont différentes...")
            new_card = Card()
            self.cards.append(new_card)
            print("Une nouvelle carte a été ajoutée à ton jeu en dernière position")


    def choose_position(self):
        """Player can choose a card out of a player's deck
        (Could be from his!!!)"""
        print("\nQuelle carte?")
        while True:
            position = input("Entre un numéro entre 1 et {} ".format(len(self.cards)))
            if not position.isdigit():
                print("Tu dois entrer un nombre !")
            else:
                position = int(position)
                if 0 < position <= len(self.cards):
                    break
                print("Ce nombre n'est pas correct")
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
        print("{}, L'as jeté te donne le pouvoir".format(self.name))
        print("de faire piocher quelqu'un")
        players_names = [player.name.lower() for player in list_of_players]
        players_names_secure = players_names.copy()
        players_names_secure.remove(self.name.lower())
        while True:
            print("Entre le nom de ta victime")
            print("parmi ces noms : ", players_names_secure)
            victim = input().lower()
            if victim in players_names_secure:
                victim_index = players_names.index(victim)
                victim = list_of_players[victim_index]
                new_card = Card()
                victim.cards.append(new_card)
                print("{}, {} t'a fait piocher une carte. Elle a été ajoutée en dernière position".format(victim.name, self.name))
                break
            print("Ce nom n'est pas correct")

    def jack_power(self, list_of_players):
        """Jacks is about messing up the game by switching cards"""
        print("{}, le valet jeté de donne le pouvoir".format(self.name))
        print("d'écahnger deux cartes!")
        players_names = [player.name.lower() for player in list_of_players]
        while True:
            print("\nEntre les noms des joueurs qui vont écahnger des cartes")
            print("Ca peut etre entre toi et un autre joueur")
            print("ou entre deux adversaires")
            print("Entre des noms parmis ceux-là : ", players_names)
            print("Entre le nom d'un joueur! (Ça peut être toi!)")
            player_a = input().lower()
            print("Entre le nom du deuxième joueur")
            player_b = input().lower()
            if (player_a and player_b in players_names and player_a != player_b):
                player_a_index = players_names.index(player_a)
                player_a = list_of_players[player_a_index]

                player_b_index = players_names.index(player_b)
                player_b = list_of_players[player_b_index]

                print("\nTu dois chosir quelle care de {} tu veux bouger".format(player_a.name))
                position_a = player_a.choose_position()

                print("\nTu dois chosir quelle care de {} tu veux bouger".format(player_b.name))
                position_b = player_b.choose_position()

                player_a.cards[position_a - 1], player_b.cards[position_b - 1] = player_b.cards[position_b - 1], player_a.cards[position_a - 1]
                print("La carte  #{} de {} et la carte #{} de {} ont été échangées!".format(position_a, player_a.name, position_b, player_b.name))
                break
            print("Ces noms ne sont pas corrects")

    def queen_power(self, list_of_players):
        """Queen gives the power to see a card from an opponent"""
        print("{}, la reine que tu as jeté te donne le pouvoir de".format(self.name))
        print("de voir une carte d'un adversaire")
        players_names = [player.name.lower() for player in list_of_players]
        players_names_secure = players_names.copy()
        players_names_secure.remove(self.name.lower())#ATTENTION AUX INDEX!
        while True:
            print("Entre le nom de ta victime")
            print("parmi ces noms : ", players_names_secure)
            victim = input().lower()
            if victim in players_names_secure: #On ne peut pas regarder son jeu!
                victim_index = players_names.index(victim) #mais il faut recuperer l'index dans la liste original
                victim = list_of_players[victim_index]
                position = victim.choose_position()
                spied_card = victim.cards[position - 1]
                print("{} a {} en position {}".format(victim.name, spied_card.name, position))
                break
            print("Ce nom n'est pas correct")

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
        path = "deck_fr.json"
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
            print("La pioche est vide! On en fait une nouvelle avec les cartes jetées")
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
        self.dataframe = pd.DataFrame(index=["Manche 1"], data=zeros, columns=players_names)

    def update_scores(self, rounds, list_of_players):
        """Adds scores from last round in the score chart"""
        scores = [player.score() for player in list_of_players]
        scores = np.array([scores])
        # score_chart = self.dataframe
        if rounds == 1:
            self.dataframe.iloc[0] = scores
            self.compute_totals_scores()
        else:
            new_row_scores = pd.DataFrame(index=["Manche {}".format(rounds)], data=scores, columns=self.dataframe.columns)
            self.dataframe = self.dataframe.drop(index="Totals")
            self.dataframe = pd.concat([self.dataframe, new_row_scores])
            self.compute_totals_scores()

    def compute_totals_scores(self):
        """sums up the scores of everyplayer an stores it in the final line"""
        final_scores = [sum(self.dataframe[player]) for player in self.dataframe.columns]
        final_scores = np.array([final_scores])
        total_row = pd.DataFrame(index=["Totals"], data=final_scores, columns=self.dataframe.columns)
        self.dataframe = pd.concat([self.dataframe, total_row])
        print("Voici la feuille de score !!!")
        print(self.dataframe)

    def determine_winner(self):
        """Determines the winner using
        score chart's last line"""
        final_scores = self.dataframe.loc["Totals"]
        winner = final_scores.idxmin()
        print("\nLe gagnant est : {} !!!".format(winner.upper()))

def initialize_players():
    """This fucntion creates the players
    the list_of_players that is going to be
    used to iterate for next functions.
    list_of_players contains Player objects"""
    while True:
        nb_of_players = input("\nEntrez le nombre de joueurs : ")
        if not nb_of_players.isdigit():
            print("Il faut entrer un nombre!")
        else:
            nb_of_players = int(nb_of_players)
            if nb_of_players < 2:
                print("Il faut être au moins deux pour jouer!")
            else:
                break
    nb_of_players = int(nb_of_players)
    list_of_players = [] #This list is going to be returned
    names_secure = [] #stores player's names in lower mode for security
    for index in range(1, nb_of_players+1):
        while True:
            player_name = input("Entrer le nom du joueur {} ".format(index))
            if (player_name.lower() == 'end' or player_name.lower() in names_secure):
                print("Nom incorrect")
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
        input("Appuie sur entrée pour passer ton tour")
        print()

def loop_until_thalom(list_of_players):
    """Main loop that stops before the game
    goes back to the player who said thalom"""
    player_that_said_thalom = 0
    check = True
    while check: #makes the loop re-read list_of_players
        for player in list_of_players:
            if player == player_that_said_thalom:
                check = False
                break
            player.launch_turn()
            player.power(list_of_players)
            player.say_thalom()
            throwing_proposition(list_of_players)
            Card.shuffle_new_deck() #happens only if the deck's empty
            if player.thalom:
                player_that_said_thalom = player

def throwing_proposition(list_of_players):
    """Players can tell if they want to throw cards"""
    list_of_players_name = [player.name.lower() for player in list_of_players]
    while True:
        print("\nSi tu veux défausser une carte sur {},".format(Card.rejected_cards[-1].name))
        print("écris ton nom et appuie sur entrée ")
        print("Si tout le monde est prêt, entrez 'end'")
        user_entry = input().lower()
        if user_entry == 'end':
            break
        if user_entry in list_of_players_name:
            get_player_index = list_of_players_name.index(user_entry)
            player = list_of_players[get_player_index]
            player.throw()
            print("Quelqu'un d'autre?")
        else:
            print("Nom incorrect")

def give_round_scores(list_of_players):
    """Informs enveryone about the round's scores
    and the cards of the players"""
    print("\nLa manche est terminée !\nVoyons voir les cartes et les scores!")

    for player in list_of_players:
        cards = [card.name for card in player.cards]
        print("\n{} a ces cartes: ".format(player.name), cards)
        print("{} a un score de {}".format(player.name, player.score()))
    final_scores = [player.score() for player in list_of_players]
    min_score = min(final_scores)
    winners_index = [i for i, x in enumerate(final_scores) if x == min_score]
    if len(winners_index) == 1:
        index_winner = winners_index[0]
        winner = list_of_players[index_winner]
        print(winner.name, "a gagné la manche avec un score de {}".format(winner.score()))
    if len(winners_index) > 1:
        print("Égalité!")
        winners_names = ""
        winners = [list_of_players[i] for i in winners_index]
        for winner in winners:
            winners_names += winner.name
        print(winners_names, "ont gagné la manche avec un score de ", str(min_score))

def continue_playing():
    """ends the round loop or launches a new round"""
    while True:
        print("\nVoulez vous jouer une autre manche? o/n")
        choice = input().lower()
        if choice == 'o':
            return True
        if choice == 'n':
            return False
        print("Commande incorrecte")

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
