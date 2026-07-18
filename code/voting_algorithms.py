"""
voting_algorithms.py

Functions for counting votes under different voting systems.
"""

import csv
import os


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


def load_riding_votes(
        path: str,
        riding: str) -> list[list[str]]:
    """Return all voter preference rankings for one riding."""

    votes = []

    with open(path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["riding"] == riding:
                ranking = row["preference_ranking"].split(";")
                votes.append(ranking)

    return votes


def count_first_choices(
        votes: list[list[str]]) -> dict[str, int]:
    """Return the number of first-choice votes for each party."""

    counts = {}

    for party in PARTIES:
        counts[party] = 0

    for ranking in votes:
        first_choice = ranking[0]
        counts[first_choice] += 1

    return counts


def run_fptp(votes: list[list[str]]) -> str:
    """Return the FPTP winner."""

    counts = count_first_choices(votes)

    winner = max(
        PARTIES,
        key=lambda party: counts[party]
    )

    return winner


def print_first_choice_results(
        counts: dict[str, int]) -> None:
    """Print first-choice vote counts."""

    print("First-choice vote counts:")

    for party in PARTIES:
        print(f"{party}: {counts[party]}")


def save_fptp_results(
        file_name: str,
        riding: str,
        counts: dict[str, int],
        winner: str) -> None:
    """Save Toronto FPTP results to a CSV file."""

    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Riding",
            "PC",
            "Liberal",
            "NDP",
            "Green",
            "Winner"
        ])

        writer.writerow([
            riding,
            counts["PC"],
            counts["Liberal"],
            counts["NDP"],
            counts["Green"],
            winner
        ])


def count_active_choices(
        votes: list[list[str]],
        active_parties: list[str]) -> dict[str, int]:
    """Count each voter's highest-ranked active party."""

    counts = {}

    for party in active_parties:
        counts[party] = 0

    for ranking in votes:
        for party in ranking:
            if party in active_parties:
                counts[party] += 1
                break

    return counts


def run_av(
        votes: list[list[str]]
        ) -> tuple[str, list[dict[str, int]]]:
    """Return the AV winner and vote counts from every round."""

    active_parties = PARTIES.copy()
    round_results = []

    while len(active_parties) > 1:
        counts = count_active_choices(
            votes,
            active_parties
        )

        round_results.append(counts.copy())

        total_votes = sum(counts.values())

        for party in active_parties:
            if counts[party] > total_votes / 2:
                return party, round_results

        lowest_party = min(
            active_parties,
            key=lambda party: counts[party]
        )

        active_parties.remove(lowest_party)

    return active_parties[0], round_results


def print_av_results(
        round_results: list[dict[str, int]]) -> None:
    """Print vote counts for every AV round."""

    for round_number in range(len(round_results)):
        counts = round_results[round_number]

        print(f"AV Round {round_number + 1}:")

        for party in counts:
            print(f"{party}: {counts[party]}")

        print()


def save_av_results(
        file_name: str,
        riding: str,
        round_results: list[dict[str, int]],
        winner: str) -> None:
    """Save Toronto AV results to a CSV file."""

    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Riding",
            "Round",
            "PC",
            "Liberal",
            "NDP",
            "Green",
            "AV Winner"
        ])

        for round_number in range(len(round_results)):
            counts = round_results[round_number]

            winner_value = ""

            if round_number == len(round_results) - 1:
                winner_value = winner

            writer.writerow([
                riding,
                round_number + 1,
                counts.get("PC", ""),
                counts.get("Liberal", ""),
                counts.get("NDP", ""),
                counts.get("Green", ""),
                winner_value
            ])


def main() -> None:
    """Compare FPTP and AV results for Toronto only."""

    current_folder = os.path.dirname(__file__)
    project_folder = os.path.dirname(current_folder)

    csv_path = os.path.join(
        project_folder,
        "data",
        "voter_preferences.csv"
    )

    results_folder = os.path.join(
        project_folder,
        "results"
    )

    os.makedirs(results_folder, exist_ok=True)

    fptp_results_path = os.path.join(
        results_folder,
        "fptp_results.csv"
    )

    av_results_path = os.path.join(
        results_folder,
        "av_results.csv"
    )

    riding = "Toronto"

    votes = load_riding_votes(
        csv_path,
        riding
    )

    print("Riding:", riding)
    print("Number of voters:", len(votes))
    print()

    first_choice_counts = count_first_choices(votes)

    print_first_choice_results(first_choice_counts)
    print()

    fptp_winner = run_fptp(votes)

    print("FPTP Winner:", fptp_winner)
    print()

    av_winner, av_rounds = run_av(votes)

    print_av_results(av_rounds)

    print("AV Winner:", av_winner)
    print()

    save_fptp_results(
        fptp_results_path,
        riding,
        first_choice_counts,
        fptp_winner
    )

    save_av_results(
        av_results_path,
        riding,
        av_rounds,
        av_winner
    )

    print("FPTP results saved to:")
    print(fptp_results_path)
    print()

    print("AV results saved to:")
    print(av_results_path)


def save_all_fptp_results(
        file_name: str,
        results: list[dict]) -> None:
    """Save FPTP results for all ridings."""

    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Riding",
            "PC",
            "Liberal",
            "NDP",
            "Green",
            "FPTP Winner"
        ])

        for result in results:
            counts = result["counts"]

            writer.writerow([
                result["riding"],
                counts["PC"],
                counts["Liberal"],
                counts["NDP"],
                counts["Green"],
                result["winner"]
            ])


def save_all_av_results(
        file_name: str,
        results: list[dict]) -> None:
    """Save every AV round for all ridings."""

    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Riding",
            "Round",
            "PC",
            "Liberal",
            "NDP",
            "Green",
            "AV Winner"
        ])

        for result in results:
            riding = result["riding"]
            round_results = result["rounds"]
            winner = result["winner"]

            for round_number in range(len(round_results)):
                counts = round_results[round_number]

                winner_value = ""

                if round_number == len(round_results) - 1:
                    winner_value = winner

                writer.writerow([
                    riding,
                    round_number + 1,
                    counts.get("PC", ""),
                    counts.get("Liberal", ""),
                    counts.get("NDP", ""),
                    counts.get("Green", ""),
                    winner_value
                ])


def save_seat_summary(
        file_name: str,
        fptp_seats: dict[str, int],
        av_seats: dict[str, int]) -> None:
    """Save seat totals under FPTP and AV."""

    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Party",
            "FPTP Seats",
            "AV Seats"
        ])

        for party in PARTIES:
            writer.writerow([
                party,
                fptp_seats[party],
                av_seats[party]
            ])


def run_all_ridings() -> None:
    """Run FPTP and AV for all ridings."""

    current_folder = os.path.dirname(__file__)
    project_folder = os.path.dirname(current_folder)

    csv_path = os.path.join(
        project_folder,
        "data",
        "voter_preferences.csv"
    )

    results_folder = os.path.join(
        project_folder,
        "results"
    )

    os.makedirs(results_folder, exist_ok=True)

    all_fptp_path = os.path.join(
        results_folder,
        "all_ridings_fptp_results.csv"
    )

    all_av_path = os.path.join(
        results_folder,
        "all_ridings_av_results.csv"
    )

    seat_summary_path = os.path.join(
        results_folder,
        "seat_summary.csv"
    )

    all_fptp_results = []
    all_av_results = []

    fptp_seats = {}
    av_seats = {}

    for party in PARTIES:
        fptp_seats[party] = 0
        av_seats[party] = 0

    changed_ridings = []

    for riding in RIDINGS:
        votes = load_riding_votes(
            csv_path,
            riding
        )

        first_choice_counts = count_first_choices(votes)

        fptp_winner = run_fptp(votes)

        av_winner, av_rounds = run_av(votes)

        all_fptp_results.append({
            "riding": riding,
            "counts": first_choice_counts,
            "winner": fptp_winner
        })

        all_av_results.append({
            "riding": riding,
            "rounds": av_rounds,
            "winner": av_winner
        })

        fptp_seats[fptp_winner] += 1
        av_seats[av_winner] += 1

        if fptp_winner != av_winner:
            changed_ridings.append({
                "riding": riding,
                "fptp_winner": fptp_winner,
                "av_winner": av_winner
            })

        print("Riding:", riding)
        print("Number of voters:", len(votes))
        print("FPTP Winner:", fptp_winner)
        print("AV Winner:", av_winner)
        print()

    save_all_fptp_results(
        all_fptp_path,
        all_fptp_results
    )

    save_all_av_results(
        all_av_path,
        all_av_results
    )

    save_seat_summary(
        seat_summary_path,
        fptp_seats,
        av_seats
    )

    print("=" * 40)
    print("SEAT SUMMARY")
    print()

    for party in PARTIES:
        print(
            f"{party}: "
            f"FPTP = {fptp_seats[party]}, "
            f"AV = {av_seats[party]}"
        )

    print()
    print("Ridings with different winners:")

    if len(changed_ridings) == 0:
        print("None")

    else:
        for result in changed_ridings:
            print(
                f'{result["riding"]}: '
                f'{result["fptp_winner"]} under FPTP, '
                f'{result["av_winner"]} under AV'
            )

    print()
    print("New results saved to:")
    print(all_fptp_path)
    print(all_av_path)
    print(seat_summary_path)


if __name__ == "__main__":
    run_all_ridings()