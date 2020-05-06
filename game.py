"""Welcome to the game 'Thalom'!"""

from player import *
from scorechart import *


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
                new_player = Player(player_name)
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
        print("If everyone's done enter 'END' to continue the round")
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
        print("\n{} has these cards: ".format(player.name), cards)
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
