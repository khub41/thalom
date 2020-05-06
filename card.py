import random
import json

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