# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — a CLI-first music recommender simulation.

---

## 2. Intended Use

This recommender suggests 3–5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration of content-based recommendation systems, not for real production use.

**Not intended for:** real music streaming platforms, commercial use, or any context where recommendations influence what real listeners hear. The catalog is too small (19 songs) and the scoring too simplistic to serve as a production system.

---

## 3. How the Model Works

For every song in the catalog the system checks three things:

1. **Genre match** — if the song's genre equals the user's favorite genre, it earns **2.0 points**.
2. **Mood match** — if the song's mood equals the user's favorite mood, it earns **1.0 point**.
3. **Energy similarity** — the closer the song's energy value is to the user's target, the more points it receives (up to **1.0 point**). This is a continuous score, not a yes/no check.

These three scores are added together (max possible: 4.0). Songs are ranked from highest to lowest total score, and the top 5 are returned as recommendations.

---

## 4. Data

The catalog is `data/songs.csv` containing **19 songs** with 10 columns: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. It spans **16 genres** (pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, metal, folk, house, classical, hip-hop, blues, reggae, r&b) and **13 moods** (happy, chill, intense, relaxed, moody, focused, nostalgic, melancholic, euphoric, peaceful, confident, soulful, romantic). Most genres have only one representative song, so the dataset is small and not balanced — some listening styles have very few or no matching songs. No songs were added or removed from the starter dataset.

---

## 5. Strengths

- Works well for "mainstream" profiles where both genre and mood exist in the catalog (e.g., a happy-pop listener gets Sunrise City at the top, which is intuitive).
- The scoring is fully transparent — reasons are returned alongside every recommendation, making it easy to explain *why* a song was suggested.
- Energy similarity adds a continuous signal that differentiates songs within the same genre/mood bucket.

---

## 6. Limitations and Bias

The system has several concrete weaknesses uncovered during evaluation. First, **genre is heavily weighted** in the baseline (2.0 points): a song that matches genre but is a poor energy fit can still outrank a song with perfect energy and mood alignment but a different genre. This means the recommender implicitly favors users whose taste aligns with well-represented genres in the catalog.

Second, the **small catalog size (19 songs)** means many genre/mood combinations simply don't exist — the "hip-hop melancholic" adversarial profile, for example, has zero exact matches, so rankings fall back to partial and sometimes unintuitive suggestions.

Third, the system **ignores features it already stores** (tempo, valence, danceability, acousticness), leaving them unused. A user who cares about acoustic music or danceable tracks gets no benefit from those preferences.

Finally, mood and genre are treated as exact string matches — "happy" and "euphoric" are scored as completely different even though they are emotionally similar. This binary matching is simplistic and can produce surprising gaps in the results.

---

## 7. Evaluation

### Process

The recommender was tested against **5 user profiles** defined in `src/main.py`: three standard archetypes (High-Energy Pop, Chill Lofi, Deep Intense Rock) and two adversarial edge cases (EDGE: Classical + High Energy, EDGE: Hip-Hop Melancholic). For each profile the top 5 songs, scores, and scoring reasons were inspected.

### Observed Behavior

- **Standard profiles** produced intuitive results — the pop listener got pop songs, the lofi listener got lofi songs.
- **Genre dominance**: in the baseline weights (genre=2.0), a genre match almost always placed a song in the top 5 regardless of mood or energy fit.
- **Adversarial profile "Classical + High Energy"** showed the lone classical song (Riverbend Sonata, energy 0.18) still ranked first despite an energy gap of 0.77, because the genre bonus alone outweighed every other song's energy score.
- **Weight-shift experiment** (genre halved to 1.0, energy doubled to 2.0) partially fixed the above: songs with close energy fits rose in rank even without a genre match, producing more diverse recommendations.

### Surprise Finding

After the weight shift, the Chill Lofi profile began surfacing ambient and folk songs alongside lofi tracks, suggesting that **energy similarity is a stronger cross-genre signal** than the baseline weights implied.

---

## 8. Future Work

- Use **partial / fuzzy matching** for mood (e.g., treat "happy" and "euphoric" as related).
- Incorporate unused features (valence, danceability, acousticness) with learnable or tunable weights.
- Expand the catalog to at least 50–100 songs for better genre coverage.
- Add a **diversity penalty** so the top-5 list doesn't contain only one genre.

---

## 9. Personal Reflection

Building this recommender showed how much a single weight choice (genre = 2.0) can silently dominate an entire ranking, echoing how real-world recommendation systems can develop hidden biases that are hard to spot without adversarial testing. The exercise also highlighted that a small dataset makes any bias worse — with only one classical song, the system literally cannot diversify within that genre.
