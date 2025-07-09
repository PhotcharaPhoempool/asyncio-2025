import time
from datetime import timedelta

speed = 1000  # Speed
Judit_time = 5/speed  # Time for Judit to move
Opponent_time = 55/speed  # Time for opponent to move
opponent = 24  # Number of opponent
move_pairs = 30 # Number of move pairs

def play_game(x):
    board_start_time = time.perf_counter()
    calc_board_start_time = 0

    for i in range(move_pairs):
        time.sleep(Judit_time)
        calc_board_start_time += Judit_time
        print(f"Board-{x + 1} {i + 1} Judit made move with {int(Judit_time*speed):.1f} sec.")

        time.sleep(Opponent_time)
        print(f"Board-{x + 1} {i + 1} Opponent made move with {int(Opponent_time*speed):.1f} sec.")
        calc_board_start_time += Opponent_time

    print(f"BOARD-{x + 1} - >>>>>>>>>>>>>>>> Finished move in {(time.perf_counter() - board_start_time)*speed:.1f} secs")
    print(f"BOARD-{x + 1} - >>>>>>>>>>>>>>>> Finished move in {calc_board_start_time*speed:.1f} secs (calculated)\n")
    return[(time.perf_counter() - board_start_time), calc_board_start_time]

if __name__ == "__main__":
    print(f"Number of games: {opponent} games.")
    print(f"Number of move: {move_pairs} pairs.\n")
    start_time = time.perf_counter()
    board_time = 0
    calc_board_time = 0
    for board in range(opponent):
        board_time += play_game(board)[0]
        calc_board_time += play_game(board)[1]

    print(f"\nBoard exhibition finished for {opponent} in {timedelta(seconds=round(board_time*speed))} hr.")
    print(f"\nBoard exhibition finished for {opponent} in {timedelta(seconds=round(calc_board_time*speed))} hr. (calculated)")
    print(f"Finished in {round(time.perf_counter() - start_time)} sec.")