from tkinter import *
from player import *
from card import *

class App(Tk):

    def __init__(self):
        super().__init__()
        self.title("Thalom - the game")
        self.config(background='#c3d8eb')
        self.geometry("720x480")

class SetupFrame(Frame):
    names = []

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.label = Label(self, text="Enter players names")
        self.label.grid(row=0, column=0)

        self.name_entry_one = Entry(self)
        self.name_entry_two = Entry(self)
        self.name_entry_one.grid(row=1, column=0)
        self.name_entry_two.grid(row=1, column=1)
        
        self.content_one = StringVar()
        self.content_two = StringVar()
        self.content_one.set("Name Player 1")
        self.content_two.set("Name Player 2")


        self.name_entry_one["textvariable"] = self.content_one
        self.name_entry_two["textvariable"] = self.content_two

        self.setup_button = Button(self, text="Submit")
        self.setup_button["command"] = self.submit
        self.setup_button.grid(row=2, column=0)
        self.pack(expand=YES)
        window.mainloop()

    def submit(self):

        self.names.append(self.content_one.get())
        self.names.append(self.content_two.get())
        self.forget()
        Card.initialize_deck_from_json()
        position = TOP
        for name in self.names:
            new_player = PlayerFrame(name, self.window, position)
            new_player.update_cards()
            position = BOTTOM
        init_playing_zone(self.window, 63, 86)
        ready = ReadyButton(self.window)
        ready.pack(expand=YES)


class CardButton(Button):
    def __init__(self, window, player_name, root_card, index):
        super().__init__(window)
        self.player_name = player_name
        self.root_card = root_card
        self.value = root_card.value
        self.index = index

    def show_value(self):
        # print("My value is {}".format(self.value))
        self["text"] = str(self.value)

class DeckButton(Button):
    def __init__(self, window):
        super().__init__(window)
        self.command = None
        self["text"] = "I'm the deck"

    def activate_pick_button(self, player):
        self["command"] = player.pick
        self["command"] = None


class DefausseButton(Button):
    """docstring for DefausseButton"""
    def __init__(self, window):
        super().__init__(window)
        self.command = None
        self["text"] = "throw your card here"
    
    def update_display(self):
        self["text"] = str(Card.rejected_cards[-1].value)

    def activate_steal_button(self, player):
        self["command"] = player.steal
        self["command"] = None
        self.update_display

class IdButton(Button):
    
    def __init__(window, player):
        super().__init__(window)
        self["text"] = "Select {}".format(player.name)

class ReadyButton(Button):
    def __init__(self, window):
        super().__init__(window)
        self["text"] = "We're ready to play ! "
        self["command"] = lambda: launch_showing_card_round(SetupFrame.names)

# class PlayerFrame(Player):

#     def __init__(self, name, playground, position):
#         super().__init__(name)

#         #creating the frame
#         frame_player_a = Frame(playground, bg='#c3d8eb')

#         #the frame has a label
#         name_player_a = Label(frame_player_a, text=self.name, font=("Helvetica", 20), bg='#c3d8eb', fg='black')

#         #the frame has cards (canvases)
#         cards_player_a = Frame(frame_player_a)
#         self.initialize_cards()
#         width_card = 63
#         height_card = 86
#         blank_card_image = PhotoImage(file="images/blank.png")
#         for i in range(len(self.cards)):
#             card_a = Button(cards_player_a, width=width_card, 
#                             height=height_card, bg='#c3d8eb',
#                             image=blank_card_image,
#                             bd=0, highlightthickness=0)
#             # card_a.create_image(width_card/2, height_card/2, image=blank_card_image)
#             card_a.grid(row=0, column=i)

#         if position == TOP:
#             name_player_a.pack() #name is at the TOP
#             cards_player_a.pack(side=BOTTOM) #cards are under the name
#         if position == BOTTOM:
#             name_player_a.pack(side=BOTTOM)
#             cards_player_a.pack()
#         self.frame = frame_player_a
#         #We pack player's A frame at the Top
#         frame_player_a.pack(side=position)

class PlayerFrame(Player):

    def __init__(self, name, playground, position):
        super().__init__(name)

        #creating the frame
        frame_player_a = Frame(playground, bg='#c3d8eb')

        #the frame has a label
        name_player_a = Label(frame_player_a, text=self.name, font=("Helvetica", 20), bg='#c3d8eb', fg='black')

        #the frame has cards (canvases)
        cards_player_a = Frame(frame_player_a)

        self.frame_cards = cards_player_a

        if position == TOP:
            name_player_a.pack() #name is at the TOP
            cards_player_a.pack(side=BOTTOM) #cards are under the name
        if position == BOTTOM:
            name_player_a.pack(side=BOTTOM)
            cards_player_a.pack()
        pass_button = Button(frame_player_a, text="Pass", command=self.end_show)
        pass_button.pack(side=RIGHT)
        self.frame = frame_player_a
        self.button_cards = []
        #We pack player's A frame at the Top
        frame_player_a.pack(side=position)
        
    def show_cards_beginning(self):
        self.button_cards[0]["text"] = str(self.button_cards[0].root_card.value)
        self.button_cards[1]["text"] = str(self.button_cards[1].root_card.value)


    def end_show(self):
        self.button_cards[0]["text"] = "I'm a card"
        self.button_cards[1]["text"] = "I'm a card"

    def update_cards(self):
        self.initialize_cards()
        width_card = 63
        height_card = 86
        # blank_card_image = PhotoImage(file="images/blank.png")
        i = 0 # ATTENTION AUX INDEX DES CARTES
        button_cards = []
        for card in self.cards:
            card_button = CardButton(self.frame_cards, self.name, card, i)
            card_button["text"] = "I'm a card"
            card_button["command"] = card_button.show_value
            # card_a.create_image(width_card/2, height_card/2, image=blank_card_image)
            card_button.grid(row=0, column=i)
            button_cards.append(card_button)
            i+=1
        self.button_cards = button_cards


def init_playing_zone(window, width_card, height_card):
    #Playing zone in the middle
    playing_zone = Frame(window, bg='#0a4d1d')

    deck_image = PhotoImage(file="images/blank.png") #deck image to be created
    deck = DeckButton(playing_zone)
    # deck.create_image(width_card/2, height_card/2, image=deck_image)
    deck.grid(row=0, column=0, padx=10, pady=10)

    depot_area = DefausseButton(playing_zone)
    depot_area.grid(row=0, column=1, padx=10, pady=10)

    playing_zone.pack(expand=YES)
    # window.update()
def launch_showing_card_round(names):


def main():
    window = Tk()
    window.title("Thalom - the game")
    window.config(background='#c3d8eb')
    window.geometry("720x480")
    launch = SetupFrame(window)
    # Card.initialize_deck_from_json()
    # player_a = PlayerFrame("Hugo", window, TOP)
    # player_b = PlayerFrame("Cami", window, BOTTOM)
    # player_a.update_cards()
    # player_b.update_cards()
    # width_card = 63
    # height_card = 86
    # init_playing_zone(window, width_card, height_card)
    # # player_a.show_cards_beginning()
    # # player_b.show_cards_beginning()
    # window.mainloop()

if __name__ == "__main__":
    main()
