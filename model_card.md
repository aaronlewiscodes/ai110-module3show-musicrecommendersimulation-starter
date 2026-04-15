# Model Card — LewisMusicRecs

## Model Name
LewisMusicRecs

## Goal / Task
Given a user's preferred genre, mood, energy level, and acoustic taste, the system suggests the five songs from the catalog most likely to match that profile.

## Data Used
The dataset is a hand-crafted CSV of 20 songs spanning genres like pop, lofi, EDM, classical, and hip-hop; the four attributes actively used in scoring are genre, mood, energy, and acousticness, while tempo, valence, and danceability are present in the data but ignored by the model. The intended purpose is classroom demonstration — it does not reflect real-world listening history, streaming data, or any actual user behavior.

## Algorithm Summary
Each song receives a weighted score built from four components: a binary genre match (35%), a binary mood match (30%), how close the song's energy is to the user's target (25%), and whether the song's acoustic level aligns with the user's acoustic preference (10%).

## Limitations and Biases
The catalog of only 20 songs is far too small for real use, and genre imbalance means niche genres like EDM have just one representative track, so after that song scores perfectly the remaining results are chosen almost entirely on energy proximity rather than genuine taste alignment. The model also has no popularity or novelty signal — it treats a song heard a thousand times the same as one never played — and its fixed weights were chosen by hand rather than learned from data, meaning they may quietly favor the developer's own taste over the user's.

## Evaluation Process
The system was tested against four distinct user profiles (high-energy pop fan, mellow acoustic listener, late-night EDM raver, and lo-fi studier) and the top-5 outputs were inspected manually to verify that scores and explanations matched the expected preference logic.

## Intended Use and Non-Intended Use
This system is intended for classroom exploration of how content-based filtering works and should not be used as a real music discovery product, deployed to actual users, or treated as a proxy for any person's musical taste.

## Ideas for Improvement
Replacing binary genre/mood matching with similarity scores (e.g., "indie pop" being partially similar to "pop") would reduce the cliff-drop in scores for near-miss preferences. Adding a diversity mechanism that penalizes recommending the same artist or genre twice in a single result set would improve variety. Incorporating unused features like tempo and valence into the scoring function would give the model more signal to differentiate songs that currently receive identical scores.

## Personal Reflection
This project was a valuable learning experience, and the biggest takeaway was discovering how powerful LLMs can be as a coding and learning tool — I used AI to help me understand the existing codebase, which made it much easier to build on top of it confidently. What surprised me most was how a simple weighted scoring function could produce results that genuinely felt like personalized recommendations, even without any machine learning. If I extended this project, I'd experiment with learned weights trained on real listening data to see how much that changes the quality of results.
