#---------main.py----------

import game_file

import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "main":
        game_file.main()
    elif sys.argv[1] == "src over time":
        game_file.record_src_over_time()
    elif sys.argv[1] == "src avg":
        print(game_file.SRCS_avg())
    elif sys.argv[1] == "record":
        game_file.record()
    elif sys.argv[1] == "watch":
        game_file.watch()
    elif sys.argv[1] == "compute_speed":
        game_file.hundred_games()


