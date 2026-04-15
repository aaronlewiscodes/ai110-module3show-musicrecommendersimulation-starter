"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print(f"\n{'='*50}")
    print(f"Profile: {label}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print("\nTop recommendations:\n")
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Profile 1: high-energy pop listener who likes upbeat moods and produced sound
    pop_fan = {
        "genre":          "pop",
        "mood":           "happy",
        "energy":         0.8,
        "likes_acoustic": False,
    }

    # Profile 2: mellow acoustic listener who unwinds with quiet, peaceful music
    acoustic_listener = {
        "genre":          "classical",
        "mood":           "peaceful",
        "energy":         0.25,
        "likes_acoustic": True,
    }

    # Profile 3: late-night EDM fan who wants maximum energy and euphoric drops
    edm_raver = {
        "genre":          "edm",
        "mood":           "euphoric",
        "energy":         0.95,
        "likes_acoustic": False,
    }

    # Profile 4: chill lo-fi listener who studies or works to focused, low-key beats
    lofi_studier = {
        "genre":          "lofi",
        "mood":           "focused",
        "energy":         0.40,
        "likes_acoustic": True,
    }

    print_recommendations("High-Energy Pop Fan", pop_fan, songs)
    print_recommendations("Mellow Acoustic Listener", acoustic_listener, songs)
    print_recommendations("Late-Night EDM Raver", edm_raver, songs)
    print_recommendations("Chill Lo-Fi Studier", lofi_studier, songs)


if __name__ == "__main__":
    main()
