# Reflection — Music Recommender Evaluation

This file includes both the assignment reflection prompts and technical evaluation notes.

## Reflection And Ethics Prompts

### What are the limitations or biases in this system?

The model is deterministic and heavily dependent on exact string matches for genre and mood. That means related moods (for example, `uplifting` vs. `happy`) can be treated as unrelated unless explicitly mapped. Even with a larger catalog, sparse combinations and fixed weights can bias recommendations toward whichever labels are over-represented.

### Could this AI be misused, and how would you prevent that?

Yes. A user could over-trust recommendations in sensitive situations (for example emotional support contexts) where this project is not designed to provide expert guidance. Mitigations in this repo include confidence scoring, guardrail warnings, and `requires_human_review` for low-confidence or weak-signal prompts. The UI and docs should continue framing outputs as suggestions, not authoritative advice.

### What surprised you while testing reliability?

Small constant changes in scoring weights produced large ranking shifts on edge prompts. This was most visible in contradictory prompts (like classical + very high energy), where the system can switch between genre-anchored and energy-anchored behavior with a single weight adjustment.

### Describe your collaboration with AI (one helpful + one flawed suggestion).

Helpful: AI suggested structuring the backend as a stepwise pipeline (parse -> retrieve -> score -> explain -> confidence -> guardrails), which made debugging and test coverage much easier.

Flawed: one AI draft recommendation over-prioritized genre matches and underweighted contradictory cues. Edge-case tests exposed this, and the fix was to rebalance behavior with confidence + guardrail checks and stronger evaluation coverage.

---

Below are the technical evaluation notes (profile-by-profile comparisons).

---

## Profile-by-Profile Comparisons

### High-Energy Pop vs. Chill Lofi

These two profiles are almost opposites — one wants upbeat pop at 0.85 energy, the other wants mellow lofi at 0.38. As expected, their top recommendations share almost no overlap. The pop profile surfaces songs like *Sunrise City* and *Gym Hero*, while the lofi profile favors *Library Rain* and *Midnight Coding*. This makes sense because the genre and energy targets point in completely different directions, and it shows the system can clearly separate two very different listener types.

### Deep Intense Rock vs. High-Energy Pop

Both profiles want high energy (0.90 and 0.85), but they differ on genre (rock vs. pop) and mood (intense vs. happy). The interesting thing is that both profiles pull in *Gym Hero* (pop, intense, 0.93) — it ranks high for the rock listener purely on energy even though the genre doesn't match. This tells us that when energy values are close, the energy similarity score alone can push a song into the top 5, even without a genre or mood match.

### EDGE: Classical + High Energy

This profile asks for classical music but with an energy target of 0.95 — a deliberate contradiction, since the only classical song (*Riverbend Sonata*) has an energy of 0.18. In the baseline weights the classical song still dominates because the genre bonus (2.0 points) is so large it overwhelms the terrible energy fit. After the weight-shift experiment (genre halved, energy doubled), high-energy songs from other genres like metal and house start to outrank it. This reveals that the original weighting was too genre-heavy — it would rather give you the "right" genre with the completely wrong vibe than a different genre that actually matches your energy preference.

### EDGE: Hip-Hop Melancholic

No song in the catalog is both hip-hop and melancholic, so the system has to fall back on partial signals. The lone hip-hop track (*Corner Cipher*, confident mood, energy 0.72) gets the genre bonus, but a folk or blues song with closer energy and a melancholic mood might arguably be a better emotional fit. The system can't see that because mood matching is binary — "melancholic" and "soulful" are treated as entirely different. This is probably the clearest example of where the recommender feels simplistic: it can't reason about emotional similarity, only exact string equality.

## Overall Takeaway

The recommender is valid for straightforward cases where a listener's preferences match a well-represented genre in the catalog. It becomes simplistic — and sometimes misleading — for edge cases, mixed tastes, or under-represented genres. The weight-shift experiment showed that rebalancing a single constant can meaningfully change which songs surface, which is both powerful and a little concerning: small tuning decisions have outsized effects when the dataset is tiny and the feature set is narrow.
