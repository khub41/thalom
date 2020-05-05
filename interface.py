from tkinter import *

window = Tk()
window.title("Thalom - the game")
window.config(background='#c3d8eb')
window.geometry("720x480")

width_card = 63
height_card = 86

blank_card_image = PhotoImage(file="images/blank.png")

def button_action():
    print("yo")

#PLAYER A

#Player A has a frame
frame_player_a = Frame(window, bg='#c3d8eb')

#the frame has a label
name_player_a = Label(frame_player_a, text="Hugo", font=("Helvetica", 20), bg='#c3d8eb', fg='black')

#the frame has cards (canvases)
cards_player_a = Frame(frame_player_a)

for i in range(4):
    card_a = Button(cards_player_a, width=width_card, 
                    height=height_card, bg='#c3d8eb',
                    image=blank_card_image, command=button_action, 
                    bd=0, highlightthickness=0)
    # card_a.image(width_card/2, height_card/2, image=blank_card_image)
    card_a.grid(row=0, column=i)


name_player_a.pack() #name is at the TOP
cards_player_a.pack(side=BOTTOM) #cards are under the name

#We pack player's A frame at the Top
frame_player_a.pack()
#########END INIT DECK FOR A################


#PLAYER B
frame_player_b = Frame(window, bg='#c3d8eb')

name_player_b = Label(frame_player_b, text="Léopold", font=("Helvetica", 20), bg='#c3d8eb', fg='black')

cards_player_b = Frame(frame_player_b)

for i in range(4):
    card_b = Canvas(cards_player_b, width=width_card, height=height_card, bg='#c3d8eb', bd=0, highlightthickness=0)
    card_b.create_image(width_card/2, height_card/2, image=blank_card_image)
    card_b.grid(row=0, column=i)

name_player_b.pack(side=BOTTOM)
cards_player_b.pack()

frame_player_b.pack(side=BOTTOM)
#########END INIT DECK FOR B################

#Playing zone in the middle
playing_zone = Frame(window, bg='#0a4d1d')

deck_image = PhotoImage(file="images/blank.png") #deck image to be created
deck = Canvas(playing_zone, width=width_card, height=height_card, bg='#0a4d1d', bd=0, highlightthickness=0)
deck.create_image(width_card/2, height_card/2, image=blank_card_image)
deck.grid(row=0, column=0, padx=10, pady=10)

depot_area = Canvas(playing_zone, width=width_card, height=height_card, bg='#383838', bd=0, highlightthickness=0)
depot_area.grid(row=0, column=1, padx=10, pady=10)

playing_zone.pack(expand=YES)

window.mainloop()
