"""
Run reproducible Random Baseline experiments
for Tic-Tac-Toe.
                            (توسعه دهنده علی احمدی)
"""

import argparse
from pathlib import Path

import pandas as pd

from tictactoe_env import TicTacToeEnv
from baseline_agent import RandomBaselineAgent


def classify_first_move(action):

    if action == 4:
        return "Center"

    if action in (0, 2, 6, 8):
        return "Corner"

    if action in (1, 3, 5, 7):
        return "Edge"

    raise ValueError(f"Invalid first move: {action}")


def run_baseline_benchmark(n_games=1000, seed=42):

    if n_games <= 0:
        raise ValueError("n_games must be positive.")

    env = TicTacToeEnv()

    agent_x = RandomBaselineAgent(
        player=1,
        seed=seed
    )

    agent_o = RandomBaselineAgent(
        player=-1,
        seed=seed + 100
    )

    records = []

    for game_id in range(n_games):

        env.reset()

        moves = 0
        first_move_x = None

        while not env.done:

            if env.current_player == 1:
                current_agent = agent_x
            else:
                current_agent = agent_o

            action = current_agent.select_action(env)

            # Check whether the selected move is legal
            if action is None or action not in env.get_legal_actions():
                raise RuntimeError(
                    f"Illegal action: {action}"
                )

            if env.current_player == 1 and first_move_x is None:
                first_move_x = action

            env.step(action)

            moves += 1

        records.append({
            "game_id": game_id,
            "winner": int(env.winner),
            "moves": moves,
            "first_move_x": first_move_x,
            "pos_type": classify_first_move(first_move_x)
        })

    return pd.DataFrame(
        records,
        columns=[
            "game_id",
            "winner",
            "moves",
            "first_move_x",
            "pos_type"
        ]
    )


def print_summary(results):

    winner_map = {
        1: "Player X Win",
        -1: "Player O Win",
        0: "Draw"
    }

    labels = results["winner"].map(winner_map)

    counts = labels.value_counts().reindex(
        ["Player X Win", "Player O Win", "Draw"],
        fill_value=0
    )

    percentages = (
        counts / len(results) * 100
    ).round(2)

    print("\n=== Random Baseline Results ===")

    print(f"Games played: {len(results)}")

    print("\nOutcome summary:")

    for label in counts.index:
        print(
            f"{label:15s}: "
            f"{counts[label]:4d} "
            f"({percentages[label]:6.2f}%)"
        )

    print(
        "\nAverage number of moves:",
        round(results["moves"].mean(), 2)
    )


def main():

    parser = argparse.ArgumentParser(
        description="Run Random Baseline Tic-Tac-Toe experiments."
    )

    parser.add_argument(
        "--games",
        type=int,
        default=1000,
        help="Number of games to simulate."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed."
    )

    parser.add_argument(
        "--output",
        type=str,
        default="baseline_results.csv",
        help="CSV output path."
    )

    args = parser.parse_args()

    results = run_baseline_benchmark(
        n_games=args.games,
        seed=args.seed
    )

    output_path = Path(args.output)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print_summary(results)

    print(
        f"\nCSV saved to: {output_path.resolve()}"
    )


if __name__ == "__main__":
    main()