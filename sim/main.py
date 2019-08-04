from othello import Game 



def play_start():
    global game

    black_player = 1
    white_player = 1

    game.start(black_player, white_player)


    game.proc_com_turn()



game = Game()

for i in range(10000):
    play_start()




