import asyncio
import time
from datetime import timedelta

speed = 1000
Judit_time = 5 / speed
Opponent_time = 55 / speed
opponent = 24
move_pairs = 30

async def play_game(board_id):
    board_start_time = time.perf_counter()
    calc_board_time = 0

    for i in range(move_pairs):
        await asyncio.sleep(Judit_time)
        calc_board_time += Judit_time
        print(f"Board-{board_id + 1} {i + 1} Judit made move with {int(Judit_time * speed):.1f} sec.")

        await asyncio.sleep(Opponent_time)
        print(f"Board-{board_id + 1} {i + 1} Opponent made move with {int(Opponent_time * speed):.1f} sec.")
        calc_board_time += Opponent_time

    real_duration = (time.perf_counter() - board_start_time)
    print(f"BOARD-{board_id + 1} - >>>>>>>>>>>>>>>> Finished move in {real_duration * speed:.1f} secs")
    print(f"BOARD-{board_id + 1} - >>>>>>>>>>>>>>>> Finished move in {calc_board_time * speed:.1f} secs (calculated)\n")
    return real_duration, calc_board_time

async def main():
    print(f"Number of games: {opponent} games.")
    print(f"Number of move: {move_pairs} pairs.\n")

    start_time = time.perf_counter()

    results = await asyncio.gather(*(play_game(i) for i in range(opponent)))

    total_real_time = sum(r[0] for r in results)
    total_calc_time = sum(r[1] for r in results)

    print(f"\nBoard exhibition finished for {opponent} in {timedelta(seconds=round(total_real_time * speed))} hr.")
    print(f"Board exhibition finished for {opponent} in {timedelta(seconds=round(total_calc_time * speed))} hr. (calculated)")
    print(f"Finished in {round(time.perf_counter() - start_time)} sec.")

if __name__ == "__main__":
    asyncio.run(main())
