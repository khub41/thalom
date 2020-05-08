    window = App()
    error = False
    list_of_players = []
    while not error:
        setup = SetupFrame(window)
        names = setup.list_of_players
        names_secure = []
        for name in names:
            if (name.lower() == 'end' or name.lower() in names_secure):
                error = True
            else:
                new_player = Player(name)
                names_secure.append(name.lower())
                list_of_players.append(new_player)
    return list_of_players
