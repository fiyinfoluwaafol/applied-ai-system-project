# Model Card: Music Recommender Simulation

## Model Name

**VibeFinder 1.0** — a CLI-first music recommender simulation.

---

## Goal / Task

Suggest a small list of songs (top 5 by default) from a fixed catalog that best match a user’s stated genre, mood, and target energy. The task is to turn simple song tags and numbers into a ranked list people can read and reason about.

---

## Intended Use and Non-Intended Use

**Intended use:** Learning and demos. Anyone can run the CLI with different taste profiles to see how a transparent, rule-based recommender behaves.

**Not intended for:** Real music streaming, commercial products, or anything that affects what real listeners hear. The catalog is still small and the rules are too simple for production.

---

## Data Used

The catalog is `backend/app/data/songs.csv`: **200 songs**, **10 columns** (`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`). There are **22 genres** and **16 moods** in the file. Coverage is broader than the starter catalog, but the feature set and ranking rules are still intentionally simple.

---

## Algorithm Summary

For each song, the program adds points and then sorts by total score (highest first).

1. **Genre match:** If the song’s genre equals the user’s favorite genre, add **2.0** points.
2. **Mood match:** If the song’s mood equals the user’s favorite mood, add **1.0** point.
3. **Energy similarity:** Add up to **1.0** point using `max(0, 1.0 − |song energy − target energy|)`. Closer energy means more points.

The highest possible total is **4.0**. The top five songs are returned. Genre and mood must match **exactly** (same string). Tempo, valence, danceability, and acousticness are loaded from the CSV but **not** used in the score.

---

## Observed Behavior / Biases

**What works:** When genre and mood exist in the catalog, results are often easy to explain (e.g. happy pop → *Sunrise City* near the top). Printed score reasons make the system transparent. Energy similarity helps separate songs inside the same genre/mood bucket.

**What we saw:** For normal profiles (e.g. happy pop, chill lofi), the top songs often looked sensible. For tricky profiles, problems showed up clearly.

**Genre weight:** With baseline weights, a genre match (2.0) can beat a much better energy fit from another genre. The classical + high-energy test showed the only classical track staying on top mainly because of genre points, even when energy was a bad match.

**Data limits:** Some genre + mood pairs do not exist in the data (e.g. hip-hop + melancholic). The system then relies on partial matches, which can feel wrong.

**Unused columns:** Extra audio-style fields in the CSV are ignored, so the model cannot reward danceability or acoustic taste.

**String matching:** “Happy” and “euphoric” are different moods with no fuzzy link, so the score can miss what a human would consider similar.

---

## Evaluation Process

**Profiles:** Five profiles in `backend/app/cli.py` — **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, plus **EDGE: Classical + High Energy (conflict)** and **EDGE: Hip-Hop Melancholic (no exact match)**. For each one we ran the CLI and read the top 5 scores and reason strings.

**Experiment:** A **weight-shift** run changed constants from baseline (`genre=2.0`, `mood=1.0`, `energy=1.0`) to `genre=1.0`, `mood=1.0`, `energy=2.0` to see if genre was too strong. After the shift, high-energy non-classical songs could rank above the low-energy classical track for the edge profile, and the lofi profile sometimes mixed in ambient or folk when energy aligned.

**Automated tests:** `pytest` runs recommender and backend pipeline tests in `backend/tests/`. The CLI path uses `recommend_songs()` / `score_song()` in the same module for the real rankings printed by `backend/app/cli.py`.

---

## Ideas for Improvement

- Fuzzy or grouped moods (e.g. treat related moods as partly matching).
- Use valence, danceability, or acousticness with small weights if the profile asks for them.
- More songs per genre so lists are not repetitive.
- A diversity rule so the top 5 is not almost all one genre.
- Optional: learn weights from feedback (not in this classroom version).

---

## Personal Reflection

**Biggest learning moment:** Rerunning the same profiles after the weight-shift experiment. One constant change moved whole top-5 lists. That made it obvious how much “the model” here is really a few numbers we chose, not magic.

**AI tools:** I used AI to help explain errors, sketch doc sections, and sanity-check wording. I still had to verify everything against `recommender.py`, `main.py`, and the CSV. The code is the source of truth — the model card and README had to match real weights and profile names.

**Surprise:** A few if-statements and one sort still produce lists that *feel* like recommendations when the data lines up. It is almost too easy to trust the output until an edge profile breaks it.

**What I would try next:** Bigger catalog, mood families instead of exact strings, and maybe one extra signal (like valence) with a weight users can slide. I would also log runs so comparing baseline vs experiment is automatic instead of by hand.
