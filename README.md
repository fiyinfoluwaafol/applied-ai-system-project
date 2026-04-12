# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world music apps often blend several ideas. **Collaborative filtering** learns from what many users play, skip, or like—*people who liked X also liked Y*—without needing to know why a song “fits.” **Content-based** methods look at the songs themselves: genre, mood, energy, and other tags or audio features, then match them to what this user says they want. This project is **content-based**: each recommendation is driven by how well a song’s **features** align with **your user profile**, not by crowd behavior from millions of listeners.

The simulation **prioritizes** three signals, in order of importance you can tune with weights: **genre** (broad musical category), **mood** (emotional vibe), and **energy similarity** (how close the song’s energy is to the user’s target, not simply “high” or “low” energy). Songs get a **numeric score** from these pieces; the **highest-scoring** songs surface as top recommendations.

### System Flow Diagram

```mermaid
flowchart TD
    A[User Profile] --> C[Score Each Song]
    B[Song Dataset (CSV)] --> C
    C --> D[Rank Songs]
    D --> E[Top K Recommendations]
```

### Song Features

- genre
- mood
- energy
- tempo_bpm (optional; include if your scoring uses it)

### User Profile Features

- favorite_genre
- favorite_mood
- target_energy

**In simple terms:** for every song, the recommender adds points when the genre and mood match the profile, and adds a **similarity** score for energy (closer to `target_energy` means more points). It then **ranks** all songs by that total score and returns the best matches—usually the top few—for the user to see.

### User Taste Profile

The user profile that drives this recommender is:

```python
user_profile = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80
}
```

This profile represents a **high-energy happy pop** listener — someone who reaches for upbeat, feel-good pop tracks that keep the energy up, like workout playlists or sunny-day driving music. The three features work together to capture that vibe:

- **Genre (`"pop"`)** anchors the listener's broad musical taste and filters out unrelated categories like rock, lofi, or classical right away.
- **Mood (`"happy"`)** narrows within pop to the optimistic, feel-good end of the spectrum, ruling out pop songs that might be moody or melancholic.
- **Energy (`0.80`)** pins down the intensity level — high enough to feel lively and uplifting, but not maxed-out like a metal track. Because energy is a continuous value (0.0–1.0), the system can measure *how close* any song is to this target rather than making a simple yes/no decision.

**Why this profile differentiates well.** Consider two contrasting styles from the catalog. A *chill lofi* track like "Library Rain" (genre: lofi, mood: chill, energy: 0.35) mismatches on all three dimensions — wrong genre, wrong mood, and its energy sits 0.45 away from the target. An *intense rock* track like "Storm Runner" (genre: rock, mood: intense, energy: 0.91) also mismatches on genre and mood, but its energy is only 0.11 away. Even though rock is closer in energy, the genre and mood mismatches keep it well below a true pop/happy match. This means the scoring system can clearly separate the user's preferred vibe from very different listening experiences, which is exactly what a useful recommender needs to do.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

