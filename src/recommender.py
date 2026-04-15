from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _user_prefs(self, user: UserProfile) -> Dict:
        return {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "energy":         user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = self._user_prefs(user)
        scored = sorted(self.songs, key=lambda s: score_song(vars(s), prefs)[0], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, explanation = score_song(vars(song), self._user_prefs(user))
        return explanation

def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """
    Scores a single song against a user taste profile.

    Categorical features (genre, mood) use binary match: 1.0 or 0.0.
    Numerical features use proximity scoring: 1 - |song_value - user_target|
    so songs closest to the user's preference rank highest regardless of direction.

    Returns (score, explanation).
    """
    # --- Categorical: binary match ---
    genre_match = 1.0 if song["genre"] == user_prefs.get("genre") else 0.0
    mood_match  = 1.0 if song["mood"]  == user_prefs.get("mood")  else 0.0

    # --- Numerical: proximity (1 - |difference|) ---
    energy_proximity = 1.0 - abs(song["energy"] - user_prefs.get("energy", 0.5))

    # Acoustic: reward high acousticness if user likes acoustic, low if not
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_score = song["acousticness"] if likes_acoustic else (1.0 - song["acousticness"])

    # --- Weighted sum ---
    score = (
        0.35 * genre_match      +
        0.30 * mood_match       +
        0.25 * energy_proximity +
        0.10 * acoustic_score
    )

    # --- Explanation ---
    reasons = []
    if genre_match:
        reasons.append(f"matches your favorite genre ({song['genre']})")
    if mood_match:
        reasons.append(f"fits your preferred mood ({song['mood']})")
    energy_diff = abs(song["energy"] - user_prefs.get("energy", 0.5))
    if energy_diff <= 0.10:
        reasons.append(f"energy ({song['energy']}) is very close to your target ({user_prefs.get('energy')})")
    elif energy_diff <= 0.25:
        reasons.append(f"energy ({song['energy']}) is near your target ({user_prefs.get('energy')})")
    if likes_acoustic and song["acousticness"] >= 0.6:
        reasons.append("acoustic texture matches your taste")
    elif not likes_acoustic and song["acousticness"] <= 0.3:
        reasons.append("produced sound matches your taste")

    explanation = ("Great match: " + ", ".join(reasons)) if reasons else "Partial match based on available features"
    return score, explanation


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(song, user_prefs)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
