# Case Study 05 — YouTube Trending: One-Hit or Repeat?

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-181717?style=for-the-badge&logo=github&logoColor=white)](https://j-amores.github.io/data-analyst-portfolio/CS05-Youtube-Statistic-Study/)

**[View the live report →](https://j-amores.github.io/data-analyst-portfolio/CS05-Youtube-Statistic-Study/)** · **[Open the analysis notebook →](analysis.ipynb)** *(78 cells, executed)*

## Summary

### Problem Statement
> *One-hit or repeat — what separates a small channel that trends twice?*

End-to-end analysis of 205 days of the US YouTube trending board (Kaggle `datasnaek/youtube-new`, November 2017 – June 2018), written for an independent creator who owns the content slate and the upload calendar, with a sponsor reading over their shoulder. The creator had already decided trending was luck, so the study is built to be losable: if it were luck, channels that went on to trend again would have looked no different beforehand. The analysis follows a **Size → Rank → Compare → Explain → Compare → Recommend** framework, and the answer is a real measurable difference that is also, deliberately, not a to-do list.

**Smaller channels** here means channels whose median trending video draws under 354,264 views: 3,489 of 6,250 videos (55.8%) and 1,385 of 2,099 channels (66.0%). **Engagement rate** is likes plus comments per hundred views, taken video by video at each video's first day on the board and reported as the median, never pooled.

---

### Q1 — Size: What does a typical trending video score, and how wide is the spread?

![Smaller-channel engagement sits at 3.53% on 119,028 views, but the middle 80% of videos runs from 0.88% to 9.12%](charts/f1_engagement_spread.png)

A smaller channel's typical trending video draws **119,028 views** and converts **3.53%** of them into a like or a comment, against 3.73% on 279,895 views for every trending video on the board including the giants. Being small is not the penalty most creators assume. The spread is the story: the middle 80% runs **0.88% to 9.12%**, a 10.4-fold range worth about 9,810 reactions an upload, and 78.6% of it survives inside a single category. The baseline is a location, not a norm.

---

### Q2 — Rank: Which categories lead and lag, and how far is that from the reach ranking?

![Only Music holds a fixed place in the category ranking; 7 of 14 rankable categories could sit four or more places higher or lower](charts/f2_category_rank_unreadable.png)

Category accounts for about **21.0%** of the video-to-video spread among smaller channels, roughly six times what all three owned settings account for together — the largest measured effect in the study. Music leads at **7.09%** (CI 6.53–7.60) and Sports trails at **1.48%** (CI 1.26–1.80). The ranking is still not a table to work down: Music is the only category holding a fixed position across the bootstrap, 7 of the 14 rankable categories have rank intervals four or more places wide, and the bottom two cannot be told apart. Reach is a different ranking again (Spearman 0.367, CI −0.015–0.547, p = 0.20).

---

### Q3 — Compare: Does that ranking hold among smaller channels, or flip?

![The category ranking holds at smaller-channel scale: the two boards rank alike at 0.88 and exactly one category differs](charts/f3_scale_holds.png)

Ranked separately, the smaller-channel and larger-channel boards line up at **Spearman ρ = 0.882** (CI 0.464–0.927) across the 11 categories with enough videos on both sides, and the smaller-channel anchor sits 0.198pp below the all-videos figure, a gap indistinguishable from zero (CI −0.458 to +0.125). After multiplicity control, exactly one category out of eleven really differs by scale: **Music, 2.19pp lower** on smaller channels. It was on nobody's list in advance. Board-wide evidence is not somebody else's game.

---

### Q4 — Explain: Which owned dial moves engagement, and how much spread is left over?

![All three settings a creator owns account for at most 3.67% of the spread between videos; at least 96.33% is not explained by them](charts/f4_dial_audit.png)

Publish slot, tag count and comments-on are the three things a creator sets on every upload. Together they account for **at most 3.67%** (CI 2.56–6.63) of the between-video spread, leaving **at least 96.33%** outside them — a lower bound, because 3.67% is a ceiling. Of the ~9,810 reactions separating the bottom tenth of videos from the top, all three account for about **161**. Two look real between videos and both collapse within channel: on the 84 channels publishing in both blocks, the publish-slot gap falls from 1.47pp to **0.08pp** (CI −0.11 to +0.52), a 94.5% shrinkage, though those same channels show the full 1.17pp unpaired.

---

### Q5 — Compare: Which calendar moves are associated with higher engagement, and what do they cost?

![We looked in 6 categories, 71.3% of smaller-channel videos, and found a publish-slot gap in 2 of them, 30.6%](charts/f5_coverage_and_priced_moves.png)

A move is priced only where both the afternoon (14:00–18:59 ET) and evening (19:00–23:59 ET) blocks hold at least 30 smaller-channel videos. Coverage: **looked in 2,488 of 3,489 videos** (71.3%, 6 categories), **found a gap in 1,066** (30.6%, 2 categories), **not priced 1,001** (28.7%, 10 categories). Entertainment's afternoon block runs 0.99pp higher while giving up 20.7% of views, pricing the trade at **22,797 views per point** against the creator's own 25,000 ceiling. People & Blogs runs higher on engagement *and* 69.1% higher on views, so nothing is traded. On Monday-to-Friday publishes alone both gaps shrink and both ranges cover zero, so the effect may be about weekends, not afternoons.

---

### Q6 — Recommend: What separates the channels that trended twice, and what can be copied?

![Channels that trended more than once were already ahead on their very first trending video: 4.84% against 3.05%](charts/f6_first_video_gap.png)

Each repeat channel enters on its **first** trending video, taken before any repeating had happened, matched against the one-hit channels' only video — one per channel on both sides, so the circular version of this comparison is not the one made. On that footing repeat channels ran **4.84% against 3.05%**, **+1.79pp** (CI 1.32–2.20, n = 445 vs 899), about **2,135 likes and comments an upload** (1,567–2,624). It survives the checks that usually kill such findings: holding category mix common leaves 74.4% of the gap, 16 of 16 sensitivity cuts agree and 11 exclude zero alone, and dropping the 116 videos already trending on day one widens it to 1.93pp.

Then the recommendation set empties on the study's own standing rule — a true finding you cannot act on does not get to masquerade as an action. Description presence (99.56% vs 94.76%) and comments-on (98.89% vs 96.79%) are ceilings with 49 and 30 videos of headroom. Category mix separates hardest and separates in *both* directions, so there is not even a category to tilt toward. Publish slot's only separating level is publishing outside both priced blocks. And tag count, 17 against 11, does not show up once a channel is compared against itself (0.04pp, CI −0.16 to +0.29, on 111 channels). *(Associative, not causal.)*

## Project Structure

```
CS05-Youtube-Statistic-Study/
├── README.md
├── index.html                          # Self-contained editorial report, served as the GitHub Page
├── analysis.ipynb                      # 78 executed cells, 18 code, one section per sub-question
├── charts/
│   ├── chart-specs.json                # One chart authority: the report renders these specs inline
│   ├── f1_engagement_spread.png        # Q1: baseline and the 10.4x spread
│   ├── f2_category_rank_unreadable.png # Q2: rank intervals, not a leaderboard
│   ├── f3_scale_holds.png              # Q3: the two boards rank alike
│   ├── f4_dial_audit.png               # Q4: the owned dials and the unexplained share
│   ├── f5_coverage_and_priced_moves.png # Q5: coverage statement and priced trades
│   └── f6_first_video_gap.png          # Q6: the first-video gap
├── data/raw/
│   └── US_category_id.json             # Category lookup, 32 codes defined, 16 present
└── assets/fonts/                       # DM Sans TTFs, shared by the charts and the report
```

> **Note:** the raw video table is not redistributed here. It is a 60 MB CSV, and this repo ships the report and the executed notebook rather than the pipeline, so nothing in it reads the file. Fetch it from [Kaggle `datasnaek/youtube-new`](https://www.kaggle.com/datasets/datasnaek/youtube-new) and take the US slice to reproduce from source.

## Dataset

| Property | Detail |
|----------|--------|
| **Source** | Kaggle `datasnaek/youtube-new`, US slice (`USvideos.csv` + `US_category_id.json`) |
| **Period** | 2017-11-14 → 2018-06-14, 205 of 213 calendar days |
| **Raw Size** | 40,949 rows × 16 columns |
| **Grain** | One video on one trending day, cumulative to that day |
| **Analysis Basis** | One row per video at its **first** trending snapshot: 6,250 of 6,351 videos, 101 back-catalogue videos excluded (1.59%) |
| **Channels** | 2,099 ruled channels; 1,385 of them smaller-channel (66.0%) |
| **Categories** | 32 codes defined, 16 present |

**Key fields:** `video_id`, `trending_date`, `title`, `channel_title`, `category_id`, `publish_time`, `tags`, `views`, `likes`, `dislikes`, `comment_count`, `comments_disabled`, `ratings_disabled`, `video_error_or_removed`, `description`.

**Not in this file, and it matters:** no subscriber count, no watch time, no click-through rate, no video duration. Every question that needed one was reframed or refused rather than estimated.

## Data Processing

- **Sentinel-safe read:** `tags == '[none]'` is a category on 258 videos, not a null; a default CSV read also swallows 570 blank descriptions (1.39% of rows).
- **Date parsing:** `trending_date` is `YY.DD.MM`, not ISO, so it is parsed explicitly. Zero unparsed.
- **Timezone conversion:** `publish_time` is stored UTC and converted to US Eastern, which moves 12.51% of rows to a different calendar date.
- **Deduplication:** 50 video-day groups carried duplicate rows; kept the row with max views, ties broken on max likes (0.122% of rows removed).
- **Basis exclusion:** back-catalogue videos taking over 30 days to reach the board are excluded (101 videos, 1.59%) — a basis decision, not a data fix.
- **Rate eligibility:** comments- or ratings-disabled videos carry no engagement rate (109 ruled videos) and are reported on their own line rather than imputed.
- **Left alone and disclosed:** 8 missing calendar days (3.76% of the span), metadata churn on up to 9.9% of videos, 400 censored runs (6.3%), and 4 removed videos. A removed video still trended.
- **Derived fields:** engagement rate, like ratio, run days with censoring flags, days-to-trend, channel median views, scale group, publish hour/day/block in ET, and tag count.

## Project Includes

- Engagement baseline with its full distribution, not just a median, at a fixed video maturity
- Category ranking reported as rank **intervals**, so an unreadable middle reads as unreadable
- A scale-holds test that establishes whether board-wide evidence is admissible at the reader's own size
- Variance decomposition of the three settings a creator actually owns, with the unexplained share as a stated lower bound
- Within-channel paired comparisons that separate "which channel posted" from "what was set on the upload"
- A two-tier coverage statement on page one: looked in, found something, not priced
- Priced trades in views given up per point of engagement gained, each judged against the reader's declared ceiling
- A non-circular repeat-versus-one-hit comparison measured before any repeating had happened, with 16 sensitivity cuts
- Channel-clustered bootstrap intervals everywhere the same channel can contribute more than one video

## Caveats

- **The direction of the headline association is unresolvable here.** A channel may trend again because of how it packages, or package that way because it already had an audience. Separating those needs a subscriber count or a pre-trending baseline, and neither exists in this data at any framing.
- **One window, one country.** 205 of 213 days, US only, and both ends of the window are partial.
- **The headline gap is a shift between heavily overlapping distributions**, not two separated groups. Cliff's delta is 0.225 (CI 0.164–0.288).
- **Videos from one channel are not independent draws.** Intra-channel correlation on ranked engagement is 0.78, so a naive video-level interval is roughly three times too narrow. Q6 is exempt by construction: one video per channel on both sides, 450 of 450 first videos verified strictly earliest with zero ties.
- **All observational.** "Associated with", never "causes". Four asks were refused rather than answered badly: predicting whether a video trends (every row here already trended and no control group exists), watch time, click-through rate and subscriber growth.

## Technologies Used

- **Python 3.14** — pandas, numpy, scipy
- **Matplotlib** — static charts, DM Sans registered from the repo's own font files
- **Jupyter** — reproducible analytical pipeline, executed via `jupyter_client`
- **HTML/CSS** — self-contained editorial report, charts rendered as inline SVG from a baked `#DATA` island, no network dependency

## How to Run

```bash
# 1. Read the report: it is one self-contained file, offline-safe, no build step
open index.html

# 2. Read the notebook: it ships executed, with outputs intact
jupyter notebook analysis.ipynb

# 3. To reproduce from source, install the stack
pip install pandas numpy scipy matplotlib jupyter

# 4. Fetch the raw US slice from Kaggle and place it here
#    https://www.kaggle.com/datasets/datasnaek/youtube-new
#    -> data/raw/USvideos.csv (40,949 rows x 16 columns)
```

## Conclusion

Channels that trend more than once were **already different on their very first trending video**, before any repeating had happened, by a margin worth roughly 2,135 reactions an upload. The difference is real, it survives every check run against it, and it sits with the channel rather than with the upload: of the five things a creator owns that could be tested against it, two are at ceilings above 94%, one is barred as out of scope, and the last two vanish once a channel is compared against itself. So the honest deliverable is a **subtraction plus two rules** — stop tuning slots and tag counts, quote a position rather than an average when a sponsor asks, and price every trade in views given up per point gained. The biggest thing this study never priced is the majority slot: **2,216 of 3,489 smaller-channel videos (63.5%)** publish in neither block, and that is also the only publish-slot level that told the two groups apart. That is the next piece of work.

## Author

- **John Amores**
- [GitHub](https://github.com/J-Amores)
