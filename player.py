from card import *

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