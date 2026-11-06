
# Four-Pile Nim 

def nim_sum(piles):
    result = 0
    for pile in piles:
        result ^= pile
    return result


def best_move(piles):
    x = nim_sum(piles)

    if x == 0:
        # No guaranteed winning move
        for i, n in enumerate(piles):
            if n > 0:
                new_piles = piles.copy()
                new_piles[i] -= 1
                return new_piles
        return piles

    for i, n in enumerate(piles):
        target = n ^ x

        if target < n:
            new_piles = piles.copy()
            new_piles[i] = target
            return new_piles

    return piles


def show_game(piles):
    print("Starting piles:", piles)
    print("Initial Nim-Sum:", nim_sum(piles))

    player = "A"

    while sum(piles) > 0:
        old = piles.copy()
        piles = best_move(piles)

        changed = next(
            i for i in range(len(piles))
            if piles[i] != old[i]
        )

        taken = old[changed] - piles[changed]

        print(
            f"Player {player}: takes {taken} "
            f"from pile {changed + 1}"
        )
        print("Piles:", piles)
        print("Nim-Sum:", nim_sum(piles))

        player = "B" if player == "A" else "A"

    winner = "B" if player == "A" else "A"
    print("\nWinner:", winner)


# Four piles
START = [3, 4, 5, 1]

show_game(START)
