"""
data_generator.py

Generate simulated voter preference rankings for Ontario ridings.
"""

import csv
import random

PARTIES = ["PC", "Liberal", "NDP", "Green"]

RIDINGS = [
    "Toronto",
    "Ottawa",
    "Niagara Falls",
    "Mississauga",
    "Hamilton",
    "London",
    "Markham",
    "Waterloo",
    "Scarborough",
    "Vaughan"
]

VOTERS_PER_RIDING = 250


# Political lean for each riding.
RIDING_LEANS = {
    "Toronto": {
        "PC": 0.15,
        "Liberal": 0.35,
        "NDP": 0.40,
        "Green": 0.10
    },
    "Ottawa": {
        "PC": 0.18,
        "Liberal": 0.42,
        "NDP": 0.30,
        "Green": 0.10
    },
    "Niagara Falls": {
        "PC": 0.50,
        "Liberal": 0.25,
        "NDP": 0.20,
        "Green": 0.05
    },
    "Mississauga": {
        "PC": 0.35,
        "Liberal": 0.40,
        "NDP": 0.20,
        "Green": 0.05
    },
    "Hamilton": {
        "PC": 0.15,
        "Liberal": 0.25,
        "NDP": 0.50,
        "Green": 0.10
    },
    "London": {
        "PC": 0.28,
        "Liberal": 0.35,
        "NDP": 0.27,
        "Green": 0.10
    },
    "Markham": {
        "PC": 0.48,
        "Liberal": 0.32,
        "NDP": 0.15,
        "Green": 0.05
    },
    "Waterloo": {
        "PC": 0.22,
        "Liberal": 0.33,
        "NDP": 0.30,
        "Green": 0.15
    },
    "Scarborough": {
        "PC": 0.30,
        "Liberal": 0.45,
        "NDP": 0.20,
        "Green": 0.05
    },
    "Vaughan": {
        "PC": 0.20,
        "Liberal": 0.30,
        "NDP": 0.25,
        "Green": 0.25
    }
}


def generate_preference_ranking(lean: dict[str, float]) -> list[str]:
    """Return one simulated voter's complete party ranking."""

    first_choice = random.choices(
        PARTIES,
        weights=[lean[p] for p in PARTIES],
        k=1
    )[0]

    remaining = []

    for party in PARTIES:
        if party != first_choice:
            remaining.append(party)

    random.shuffle(remaining)

    return [first_choice] + remaining


def write_voter_preferences(path: str) -> None:
    """Generate simulated voter preferences and write them to a CSV."""

    with open(path, "w", newline="", encoding="utf-8") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "riding",
            "voter_id",
            "preference_ranking"
        ])

        voter_id = 1

        for riding in RIDINGS:

            lean = RIDING_LEANS[riding]

            for _ in range(VOTERS_PER_RIDING):

                ranking = generate_preference_ranking(lean)

                writer.writerow([
                    riding,
                    voter_id,
                    ";".join(ranking)
                ])

                voter_id += 1

    print(f"Generated {voter_id - 1} voters.")


def main() -> None:
    """Generate one simulated election dataset."""

    random.seed(302)

    write_voter_preferences("voter_preferences.csv")


if __name__ == "__main__":
    main()